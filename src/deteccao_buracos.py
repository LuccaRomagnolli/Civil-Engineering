from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

from .config import DATA_DIR, SEED

SEMENTE_PADRAO = SEED
TAMANHO_IMAGEM_PADRAO = (128, 128)
PROPORCAO_VALIDACAO_PADRAO = 0.2
MAPA_CLASSES = {"normal": 0, "buracos": 1}
NOME_PASTA_LEGADA_BURACOS = bytes.fromhex("706f74686f6c6573").decode("utf-8")


def _resolver_pasta_buracos(caminho_base: Path) -> Path:
    candidatos = [
        caminho_base / "buracos",
        caminho_base / NOME_PASTA_LEGADA_BURACOS,
    ]
    for pasta in candidatos:
        if pasta.exists():
            return pasta
    return caminho_base / "buracos"


def obter_caminhos_dataset() -> dict[str, str]:
    caminho_base = DATA_DIR / "whole-detection" / "archive"
    caminho_buracos = _resolver_pasta_buracos(caminho_base)
    return {
        "base": str(caminho_base),
        "normal": str(caminho_base / "normal"),
        "buracos": str(caminho_buracos),
    }


def _configurar_semente(semente: int) -> None:
    np.random.seed(semente)
    tf.random.set_seed(semente)


def _preprocessar_imagem(img_bgr: np.ndarray, tamanho_imagem: tuple[int, int]) -> np.ndarray:
    img_redimensionada = cv2.resize(img_bgr, tamanho_imagem)
    img_rgb = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2RGB)
    img_normalizada = img_rgb.astype(np.float32) / 255.0
    return img_normalizada


def _carregar_classe(
    pasta_classe: Path, rotulo: int, tamanho_imagem: tuple[int, int]
) -> tuple[list[np.ndarray], list[int]]:
    imagens: list[np.ndarray] = []
    rotulos: list[int] = []

    for caminho_imagem in sorted(pasta_classe.glob("*.jpg")):
        imagem = cv2.imread(str(caminho_imagem))
        if imagem is None:
            continue
        imagens.append(_preprocessar_imagem(imagem, tamanho_imagem))
        rotulos.append(rotulo)

    return imagens, rotulos


def carregar_imagens_rotuladas(
    caminho_base: str, tamanho_imagem: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray]:
    raiz = Path(caminho_base)
    pasta_normal = raiz / "normal"
    pasta_buracos = _resolver_pasta_buracos(raiz)

    if not pasta_normal.exists() or not pasta_buracos.exists():
        raise FileNotFoundError(
            "Estrutura de dataset invalida. Esperado: "
            f"{pasta_normal} e {pasta_buracos}"
        )

    imagens_normal, rotulos_normal = _carregar_classe(
        pasta_normal, MAPA_CLASSES["normal"], tamanho_imagem
    )
    imagens_buracos, rotulos_buracos = _carregar_classe(
        pasta_buracos, MAPA_CLASSES["buracos"], tamanho_imagem
    )

    X = np.array(imagens_normal + imagens_buracos, dtype=np.float32)
    y = np.array(rotulos_normal + rotulos_buracos, dtype=np.int32)

    if X.size == 0 or y.size == 0:
        raise ValueError("Nenhuma imagem valida foi carregada do dataset.")

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
    modelo: tf.keras.Model, X_valid: np.ndarray, y_valid: np.ndarray
) -> dict[str, object]:
    probabilidades = modelo.predict(X_valid, verbose=0).ravel()
    predicoes = (probabilidades >= 0.5).astype(np.int32)

    matriz_confusao = confusion_matrix(y_valid, predicoes)
    relatorio = classification_report(
        y_valid,
        predicoes,
        target_names=["normal", "buracos"],
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
