from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJETO_RAIZ = Path(__file__).resolve().parents[1]
if str(PROJETO_RAIZ) not in sys.path:
    sys.path.insert(0, str(PROJETO_RAIZ))

from src.deteccao_buracos import (
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Treina a CNN baseline para deteccao de buracos.")
    parser.add_argument("--epocas", type=int, default=5, help="Numero de epocas de treino.")
    parser.add_argument("--batch-size", type=int, default=32, help="Tamanho do batch.")
    parser.add_argument(
        "--saida-json",
        type=Path,
        default=PROJETO_RAIZ / "outputs" / "whole-detection" / "metricas_baseline.json",
        help="Caminho para salvar as metricas em JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    caminhos = obter_caminhos_dataset()

    X, y = carregar_imagens_rotuladas(caminhos["base"], TAMANHO_IMAGEM_PADRAO)
    X_treino, X_valid, y_treino, y_valid = separar_treino_validacao(
        X, y, PROPORCAO_VALIDACAO_PADRAO, SEMENTE_PADRAO
    )

    modelo = construir_cnn_baseline((TAMANHO_IMAGEM_PADRAO[0], TAMANHO_IMAGEM_PADRAO[1], 3))
    historico = treinar_modelo(
        modelo,
        X_treino,
        y_treino,
        X_valid,
        y_valid,
        epocas=args.epocas,
        batch_size=args.batch_size,
    )
    resultados = avaliar_modelo(modelo, X_valid, y_valid)

    print(f"Acuracia validacao: {resultados['acuracia']:.4f}")
    print("Matriz de confusao:")
    print(resultados["matriz_confusao"])

    args.saida_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "acuracia_validacao": resultados["acuracia"],
        "historico": {
            "loss": [float(x) for x in historico.history.get("loss", [])],
            "val_loss": [float(x) for x in historico.history.get("val_loss", [])],
            "accuracy": [float(x) for x in historico.history.get("accuracy", [])],
            "val_accuracy": [float(x) for x in historico.history.get("val_accuracy", [])],
        },
        "matriz_confusao": resultados["matriz_confusao"].tolist(),
        "relatorio_classificacao": resultados["relatorio_classificacao"],
    }
    args.saida_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Metricas salvas em: {args.saida_json}")


if __name__ == "__main__":
    main()
