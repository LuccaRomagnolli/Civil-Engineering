# Civil Engineering - Machine Learning & AI Systems

## Visao Geral
Repositorio com pipelines de aprendizado de maquina para engenharia civil, com foco em reproducibilidade, estrutura profissional e execucao local no VS Code.

## Estrutura do Repositorio
```text
Civil-Engineering/
|-- .vscode/                  # Configuracoes de execucao e debug no VS Code
|-- datasets/                 # Datasets brutos
|-- notebooks/                # Notebooks de analise e experimentacao
|-- scripts/                  # Scripts de treino e validacao rapida
|-- src/                      # Codigo reutilizavel
|-- models/                   # Modelos salvos (ignorado no git)
|-- reports/                  # Relatorios e figuras (ignorado no git)
|-- outputs/                  # Saidas temporarias (ignorado no git)
|-- requirements.txt
|-- README.md
`-- LICENSE
```

## Como Executar (VS Code)
1. Crie e ative um ambiente virtual Python.
2. Rode a task `Instalar dependencias` em `Terminal > Run Task`.
3. Rode a task `Smoke test whole-detection` para validar o pipeline com 1 epoca.
4. Abra e execute o notebook `deteccao-buracos-cnn-baseline.ipynb` do inicio ao fim.

## Autor
Lucca Romagnolli

## Licenca
Consulte o arquivo `LICENSE`.

Ultima atualizacao: Marco 2026
