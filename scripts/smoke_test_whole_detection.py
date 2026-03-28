from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

PROJETO_RAIZ = Path(__file__).resolve().parents[1]
if str(PROJETO_RAIZ) not in sys.path:
    sys.path.insert(0, str(PROJETO_RAIZ))

from src.deteccao_buracos import (
    MAPA_CLASSES,
    PROPORCAO_VALIDACAO_PADRAO,
    SEMENTE_PADRAO,
    TAMANHO_IMAGEM_PADRAO,
    avaliar_modelo,
    carregar_imagens_rotuladas,
    construir_cnn_baseline,
    obter_caminhos_dataset,
    separar_treino_validacao,
    treinar_modelo,
)


def _assert(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise AssertionError(mensagem)


def main() -> None:
    caminhos = obter_caminhos_dataset()
    X, y = carregar_imagens_rotuladas(caminhos["base"], TAMANHO_IMAGEM_PADRAO)

    _assert(X.ndim == 4, "X deve ser um tensor 4D.")
    _assert(y.ndim == 1, "y deve ser um vetor 1D.")
    _assert(X.shape[1:3] == TAMANHO_IMAGEM_PADRAO, "Formato de imagem invalido.")
    _assert(float(X.min()) >= 0.0 and float(X.max()) <= 1.0, "Imagens fora da normalizacao [0,1].")

    classes_unicas, contagens = np.unique(y, return_counts=True)
    contagem_classes = {int(classe): int(total) for classe, total in zip(classes_unicas, contagens)}
    _assert(MAPA_CLASSES["normal"] in contagem_classes, "Classe normal ausente.")
    _assert(MAPA_CLASSES["buracos"] in contagem_classes, "Classe buracos ausente.")

    X_treino, X_valid, y_treino, y_valid = separar_treino_validacao(
        X, y, PROPORCAO_VALIDACAO_PADRAO, SEMENTE_PADRAO
    )

    modelo = construir_cnn_baseline((TAMANHO_IMAGEM_PADRAO[0], TAMANHO_IMAGEM_PADRAO[1], 3))
    _ = treinar_modelo(
        modelo,
        X_treino,
        y_treino,
        X_valid,
        y_valid,
        epocas=1,
        batch_size=32,
    )

    resultados = avaliar_modelo(modelo, X_valid, y_valid)
    matriz = resultados["matriz_confusao"]
    relatorio = resultados["relatorio_classificacao"]

    _assert(matriz.shape == (2, 2), "Matriz de confusao deve ser 2x2.")
    _assert("normal" in relatorio and "buracos" in relatorio, "Relatorio incompleto.")
    _assert("precision" in relatorio["normal"], "Metricas de precisao ausentes.")
    _assert(0.0 <= resultados["acuracia"] <= 1.0, "Acuracia fora do intervalo esperado.")

    print("Smoke test concluido com sucesso.")
    print(f"Amostras carregadas: {X.shape[0]}")
    print(f"Distribuicao de classes: {contagem_classes}")
    print(f"Acuracia de validacao: {resultados['acuracia']:.4f}")
    print("Matriz de confusao:")
    print(matriz)


if __name__ == "__main__":
    main()
