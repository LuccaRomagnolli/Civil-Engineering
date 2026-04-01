"""Transfer learning (MobileNetV2 / EfficientNetB0) para classificação de buracos em pavimento."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, roc_auc_score
from sklearn.utils import class_weight as sk_class_weight
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0, MobileNetV2
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess_input
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_v2_preprocess_input

def obter_preprocess_input(nome_backbone: str) -> Callable[[tf.Tensor], tf.Tensor]:
    """Retorna função de pré-processamento compatível com o backbone (pesos ImageNet)."""

    def _wrap_mobilenet(x: tf.Tensor) -> tf.Tensor:
        return mobilenet_v2_preprocess_input(x)

    def _wrap_efficientnet(x: tf.Tensor) -> tf.Tensor:
        return efficientnet_preprocess_input(x)

    n = nome_backbone.lower()
    if "mobilenet" in n:
        return _wrap_mobilenet
    if "efficientnet" in n:
        return _wrap_efficientnet
    raise ValueError(f"Backbone não suportado: {nome_backbone}")


def construir_backbone(
    nome_backbone: str,
    forma_entrada: tuple[int, int, int],
    pesos: str = "imagenet",
) -> tf.keras.Model:
    """Carrega backbone CNN pré-treinado sem topo."""
    h, w, c = forma_entrada
    if c != 3:
        raise ValueError("Esperado 3 canais RGB.")

    n = nome_backbone.lower()
    if "mobilenet" in n:
        return MobileNetV2(
            include_top=False,
            weights=pesos,
            input_shape=(h, w, c),
        )
    if "efficientnet" in n:
        return EfficientNetB0(
            include_top=False,
            weights=pesos,
            input_shape=(h, w, c),
        )
    raise ValueError(f"Backbone não suportado: {nome_backbone}")


def construir_head_transfer(
    backbone: tf.keras.Model,
    n_classes: int = 2,
    dropout: float = 0.3,
    unidades_dense: int = 128,
) -> tf.keras.Model:
    """GlobalAveragePooling2D → Dropout → Dense(relu) → Dense(softmax)."""
    entrada = tf.keras.Input(shape=backbone.input_shape[1:])
    x = backbone(entrada, training=False)
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dropout(dropout, name="dropout_head")(x)
    x = layers.Dense(unidades_dense, activation="relu", name="dense_128")(x)
    saida = layers.Dense(n_classes, activation="softmax", name="saida_softmax")(x)
    return tf.keras.Model(entrada, saida, name=f"{backbone.name}_head")


def construir_modelo_transfer_completo(
    nome_backbone: str,
    forma_entrada: tuple[int, int, int],
    n_classes: int = 2,
    dropout: float = 0.3,
    pesos: str = "imagenet",
) -> tuple[tf.keras.Model, tf.keras.Model]:
    """Monta backbone + head. Retorna `(modelo, backbone)` para congelar/descongelar."""
    backbone = construir_backbone(nome_backbone, forma_entrada, pesos=pesos)
    modelo = construir_head_transfer(backbone, n_classes=n_classes, dropout=dropout)
    return modelo, backbone


def congelar_backbone(backbone: tf.keras.Model) -> None:
    """Congela o backbone pré-treinado."""
    backbone.trainable = False


def descongelar_ultimas_camadas_backbone(backbone: tf.keras.Model, n_camadas: int) -> None:
    """Descongela as últimas `n_camadas` do backbone (ordem topológica)."""
    backbone.trainable = True
    camadas_backbone = list(backbone.layers)
    for camada in camadas_backbone[:-n_camadas]:
        camada.trainable = False
    for camada in camadas_backbone[-n_camadas:]:
        camada.trainable = True


def preprocess_numpy_rgb_01(
    X01: np.ndarray,
    nome_backbone: str,
) -> np.ndarray:
    """Converte imagens [0,1] RGB para tensor pré-processado (ImageNet) com NumPy."""
    x = np.asarray(X01 * 255.0, dtype=np.float32)
    n = nome_backbone.lower()
    if "mobilenet" in n:
        return mobilenet_v2_preprocess_input(x.copy())
    if "efficientnet" in n:
        return efficientnet_preprocess_input(x.copy())
    raise ValueError(f"Backbone não suportado: {nome_backbone}")


def calcular_class_weight_dict(y: np.ndarray) -> dict[int, float]:
    """Pesos de classe balanceados (sklearn) para `sparse_categorical_crossentropy`."""
    classes = np.unique(y)
    pesos = sk_class_weight.compute_class_weight("balanced", classes=classes, y=y)
    return {int(c): float(w) for c, w in zip(classes, pesos)}


def _criar_camadas_augmentacao(seed: int | None) -> tf.keras.Sequential:
    """Camadas de aumento adequadas a pavimento (aplicadas em treino)."""
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal", seed=seed),
            layers.RandomRotation(0.087, seed=seed),  # ~±15°
            layers.RandomZoom((-0.15, 0.15), seed=seed),
            layers.RandomContrast(0.15, seed=seed),
        ],
        name="augmentacao_pavimento",
    )


def montar_tf_dataset_treino(
    X_treino: np.ndarray,
    y_treino: np.ndarray,
    batch_size: int,
    preprocess_fn: Callable[[tf.Tensor], tf.Tensor],
    seed: int,
    shuffle_buffer: int | None = None,
) -> tf.data.Dataset:
    """
    Dataset de treino com augmentation e normalização ImageNet.
    `X_treino` está em [0, 1] float32 RGB (mesmo formato que `carregar_imagens_rotuladas`).
    """
    if shuffle_buffer is None:
        shuffle_buffer = min(len(X_treino), 1024)

    aug = _criar_camadas_augmentacao(seed)

    def _map_treino(x: tf.Tensor, y: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        # Escala para [0, 255] para augment e para preprocess_input das applications
        x = x * 255.0
        x = tf.expand_dims(x, 0)
        x = aug(x, training=True)
        x = tf.squeeze(x, 0)
        x = tf.clip_by_value(x, 0.0, 255.0)
        x = preprocess_fn(x)
        return x, y

    ds = tf.data.Dataset.from_tensor_slices((X_treino, y_treino))
    ds = ds.shuffle(shuffle_buffer, seed=seed, reshuffle_each_iteration=True)
    ds = ds.map(_map_treino, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds


def montar_tf_dataset_validacao(
    X_valid: np.ndarray,
    y_valid: np.ndarray,
    batch_size: int,
    preprocess_fn: Callable[[tf.Tensor], tf.Tensor],
) -> tf.data.Dataset:
    """Validação: apenas normalização ImageNet (sem augmentation)."""

    def _map_val(x: tf.Tensor, y: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        x = x * 255.0
        x = preprocess_fn(x)
        return x, y

    ds = tf.data.Dataset.from_tensor_slices((X_valid, y_valid))
    ds = ds.map(_map_val, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds


def avaliar_modelo_softmax(
    modelo: tf.keras.Model,
    X_valid: np.ndarray,
    y_valid: np.ndarray,
    nome_backbone: str,
    batch_size: int = 32,
) -> dict[str, object]:
    """Avalia modelo com saída softmax (2 classes). Inclui AUC, F1 macro e probabilidade da classe positiva."""
    x = preprocess_numpy_rgb_01(X_valid, nome_backbone)
    probs = modelo.predict(x, batch_size=batch_size, verbose=0)
    preds = np.argmax(probs, axis=1)
    prob_positivo = probs[:, 1]

    matriz = confusion_matrix(y_valid, preds)
    relatorio = classification_report(
        y_valid,
        preds,
        target_names=["normal", "buracos"],
        output_dict=True,
        zero_division=0,
    )
    acuracia = accuracy_score(y_valid, preds)
    f1_macro = f1_score(y_valid, preds, average="macro", zero_division=0)
    try:
        auc = roc_auc_score(y_valid, prob_positivo)
    except ValueError:
        auc = float("nan")

    return {
        "acuracia": float(acuracia),
        "f1_macro": float(f1_macro),
        "auc": float(auc),
        "matriz_confusao": matriz,
        "relatorio_classificacao": relatorio,
        "predicoes": preds,
        "probabilidades_positivo": prob_positivo,
        "probabilidades": probs,
    }


class MetricasValidacaoCallback(tf.keras.callbacks.Callback):
    """
    Ao fim de cada época, calcula F1 e AUC no conjunto de validação (arrays originais [0,1]).
    Acrescenta `val_f1` e `val_auc` a `logs` e armazena linhas para export CSV.
    """

    def __init__(
        self,
        X_valid: np.ndarray,
        y_valid: np.ndarray,
        fase: str,
        nome_backbone: str,
        batch_size: int = 32,
    ) -> None:
        super().__init__()
        self.X_valid = X_valid
        self.y_valid = y_valid
        self.fase = fase
        self.nome_backbone = nome_backbone
        self.batch_size = batch_size
        self.linhas: list[dict[str, object]] = []

    def on_epoch_end(self, epoch: int, logs: dict | None = None) -> None:
        logs = logs or {}
        x = preprocess_numpy_rgb_01(self.X_valid, self.nome_backbone)
        probs = self.model.predict(x, batch_size=self.batch_size, verbose=0)
        preds = np.argmax(probs, axis=1)
        prob_pos = probs[:, 1]
        f1 = f1_score(self.y_valid, preds, average="macro", zero_division=0)
        try:
            auc = roc_auc_score(self.y_valid, prob_pos)
        except ValueError:
            auc = float("nan")

        logs["val_f1"] = float(f1)
        logs["val_auc"] = float(auc)

        self.linhas.append(
            {
                "epoch": epoch + 1,
                "phase": self.fase,
                "train_loss": float(logs.get("loss", float("nan"))),
                "val_loss": float(logs.get("val_loss", float("nan"))),
                "val_accuracy": float(logs.get("val_accuracy", float("nan"))),
                "val_f1": float(f1),
                "val_auc": float(auc),
            }
        )


def anexar_historico_csv(
    caminho_csv: Path | str,
    linhas: list[dict[str, object]],
    modo: str = "a",
) -> None:
    """Grava ou anexa linhas de métricas ao CSV de resultados."""
    caminho = Path(caminho_csv)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if not linhas:
        return
    df = pd.DataFrame(linhas)
    escrever_header = modo == "w" or not caminho.exists()
    df.to_csv(caminho, mode=modo, header=escrever_header, index=False)


def grad_cam_mobilenet(
    modelo: tf.keras.Model,
    img_preprocessed: np.ndarray,
    classe_idx: int = 1,
) -> np.ndarray:
    """
    Grad-CAM simplificado para modelos com backbone MobileNetV2 como subgrafo.
    `img_preprocessed` deve já estar no formato após preprocess_input (batch 1 ou H,W,C).
    Retorna mapa de calor 2D normalizado para [0,1].
    """
    if img_preprocessed.ndim == 3:
        x = np.expand_dims(img_preprocessed, 0)
    else:
        x = img_preprocessed

    backbone_layer = None
    for layer in modelo.layers:
        if isinstance(layer, tf.keras.Model) and len(getattr(layer, "layers", [])) > 0:
            if "mobilenet" in layer.name.lower():
                backbone_layer = layer
                break
    if backbone_layer is None:
        raise ValueError("Backbone MobileNetV2 não encontrado no modelo.")

    ultima_conv = None
    for layer in backbone_layer.layers[::-1]:
        if len(layer.output_shape) == 4:
            ultima_conv = layer
            break
    if ultima_conv is None:
        raise ValueError("Não foi possível localizar camada convolucional no backbone.")

    grad_model = tf.keras.Model(
        inputs=[modelo.inputs],
        outputs=[ultima_conv.output, modelo.output],
    )

    with tf.GradientTape() as tape:
        conv_out, preds = grad_model(x, training=False)
        classe = preds[:, classe_idx]

    grads = tape.gradient(classe, conv_out)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_out[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_out), axis=-1)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()
