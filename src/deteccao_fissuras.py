"""Classificação binária de fissuras superficiais em concreto (Negative / Positive)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

from .config import DATA_DIR, SEED

SEMENTE_PADRAO = SEED
TAMANHO_IMAGEM_PADRAO = (128, 128)
PROPORCAO_VALIDACAO_PADRAO = 0.2
# Negative = sem fissura, Positive = com fissura (rótulo 1 = positivo para métricas AUC etc.)
MAPA_CLASSES = {"sem_fissura": 0, "com_fissura": 1}
PASTA_NEGATIVA = "Negative"
PASTA_POSITIVA = "Positive"
EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")


@lru_cache(maxsize=1)
def _cv2():
    try:
        import cv2 as opencv
    except ImportError as exc:
        raise ImportError(
            "Dependência ausente: opencv-python (módulo cv2). "
            "Instale com: pip install opencv-python"
        ) from exc
    return opencv


def obter_cv2():
    return _cv2()


def obter_caminhos_dataset(raiz_datasets: Path | str | None = None) -> dict[str, str]:
    base = Path(raiz_datasets) if raiz_datasets is not None else DATA_DIR
    caminho_base = base / "surface-crack-detection"
    return {
        "base": str(caminho_base),
        "sem_fissura": str(caminho_base / PASTA_NEGATIVA),
        "com_fissura": str(caminho_base / PASTA_POSITIVA),
    }


def _listar_caminhos_imagens(pasta: Path) -> list[Path]:
    arquivos: list[Path] = []
    for item in sorted(pasta.iterdir()):
        if item.is_file() and item.suffix in EXTENSOES_IMAGEM:
            arquivos.append(item)
    return arquivos


def _configurar_semente(semente: int) -> None:
    np.random.seed(semente)
    tf.random.set_seed(semente)


def _preprocessar_imagem(img_bgr: np.ndarray, tamanho_imagem: tuple[int, int]) -> np.ndarray:
    cv2 = _cv2()
    img_redimensionada = cv2.resize(img_bgr, tamanho_imagem)
    img_rgb = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2RGB)
    img_normalizada = img_rgb.astype(np.float32) / 255.0
    return img_normalizada


def _carregar_classe(
    pasta_classe: Path,
    rotulo: int,
    tamanho_imagem: tuple[int, int],
    max_imagens: int | None,
    semente: int,
) -> tuple[list[np.ndarray], list[int]]:
    cv2 = _cv2()
    imagens: list[np.ndarray] = []
    rotulos: list[int] = []

    caminhos = _listar_caminhos_imagens(pasta_classe)
    if max_imagens is not None and len(caminhos) > max_imagens:
        rng = np.random.default_rng(semente)
        escolhidos = rng.choice(len(caminhos), size=max_imagens, replace=False)
        caminhos = [caminhos[i] for i in sorted(escolhidos)]

    for caminho_imagem in caminhos:
        imagem = cv2.imread(str(caminho_imagem))
        if imagem is None:
            continue
        imagens.append(_preprocessar_imagem(imagem, tamanho_imagem))
        rotulos.append(rotulo)

    return imagens, rotulos


def carregar_imagens_rotuladas(
    caminho_base: str,
    tamanho_imagem: tuple[int, int],
    max_por_classe: int | None = None,
    semente_amostragem: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Carrega imagens de `Negative` e `Positive`. Se o dataset for grande (ex.: 20k/classe),
    use `max_por_classe` para subamostragem estratificada e uso de memória controlado.
    """
    raiz = Path(caminho_base)
    pasta_neg = raiz / PASTA_NEGATIVA
    pasta_pos = raiz / PASTA_POSITIVA

    if not pasta_neg.exists() or not pasta_pos.exists():
        raise FileNotFoundError(
            "Estrutura de dataset inválida. Esperado: "
            f"{pasta_neg} e {pasta_pos}"
        )

    sem = semente_amostragem if semente_amostragem is not None else SEMENTE_PADRAO
    imagens_neg, rotulos_neg = _carregar_classe(
        pasta_neg, MAPA_CLASSES["sem_fissura"], tamanho_imagem, max_por_classe, sem
    )
    imagens_pos, rotulos_pos = _carregar_classe(
        pasta_pos, MAPA_CLASSES["com_fissura"], tamanho_imagem, max_por_classe, sem
    )

    X = np.array(imagens_neg + imagens_pos, dtype=np.float32)
    y = np.array(rotulos_neg + rotulos_pos, dtype=np.int32)

    if X.size == 0 or y.size == 0:
        raise ValueError("Nenhuma imagem válida foi carregada do dataset.")

    return X, y


def separar_treino_validacao(
    X: np.ndarray, y: np.ndarray, proporcao_validacao: float, semente: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    _configurar_semente(semente)
    return train_test_split(
        X,
        y,
        test_size=proporcao_validacao,
        random_state=semente,
        stratify=y,
    )


def construir_cnn_baseline(forma_entrada: tuple[int, int, int]) -> tf.keras.Model:
    modelo = models.Sequential(
        [
            layers.Input(shape=forma_entrada),
            layers.Conv2D(32, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(1, activation="sigmoid"),
        ]
    )

    modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return modelo


def treinar_modelo(
    modelo: tf.keras.Model,
    X_treino: np.ndarray,
    y_treino: np.ndarray,
    X_valid: np.ndarray,
    y_valid: np.ndarray,
    epocas: int,
    batch_size: int,
) -> tf.keras.callbacks.History:
    return modelo.fit(
        X_treino,
        y_treino,
        epochs=epocas,
        batch_size=batch_size,
        validation_data=(X_valid, y_valid),
        verbose=1,
    )


def avaliar_modelo(
    modelo: tf.keras.Model,
    X_valid: np.ndarray,
    y_valid: np.ndarray,
    target_names: tuple[str, str] = ("sem_fissura", "com_fissura"),
) -> dict[str, object]:
    probabilidades = modelo.predict(X_valid, verbose=0).ravel()
    predicoes = (probabilidades >= 0.5).astype(np.int32)

    matriz_confusao = confusion_matrix(y_valid, predicoes)
    relatorio = classification_report(
        y_valid,
        predicoes,
        target_names=list(target_names),
        output_dict=True,
        zero_division=0,
    )
    acuracia = accuracy_score(y_valid, predicoes)

    return {
        "acuracia": float(acuracia),
        "matriz_confusao": matriz_confusao,
        "relatorio_classificacao": relatorio,
        "predicoes": predicoes,
        "probabilidades": probabilidades,
    }
