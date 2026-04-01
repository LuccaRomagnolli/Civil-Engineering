# Deteccao de Buracos em Pavimento com CNN e Transfer Learning

<p align="center">
  <img src="../../images/Logo_unb-removebg-preview.png" alt="Logo UnB" width="220" />
</p>

**Autor:** Lucca Maximus Romagnolli  
**Instituicao:** Universidade de Brasilia (UnB)

## Resumo
Este projeto investiga a classificacao automatica de imagens de pavimento em duas classes (`normal` e `buracos`) com tecnicas de visao computacional e aprendizado profundo. A proposta combina uma CNN baseline treinada do zero com uma abordagem de transfer learning, visando maior desempenho e melhor generalizacao em cenario real de inspecao visual de vias.

## Apresentacao Academica do Projeto
A deteccao automatica de patologias superficiais no pavimento e um problema relevante para engenharia civil, pois permite acelerar diagnosticos e apoiar manutencao preditiva. Neste trabalho, foi estruturado um pipeline reprodutivel com:

- organizacao de dados e scripts de execucao;
- controle de sementes para reproducibilidade;
- comparacao entre modelo baseline e modelo com pesos ImageNet;
- avaliacao quantitativa por metricas de classificacao.

O notebook principal `deteccao-buracos-cnn-baseline.ipynb` documenta o fluxo experimental completo, da exploracao inicial dos dados ate a inferencia em imagem externa de campo.

## Metodologia
### 1. Base de dados e rotulacao
- Fonte local: `datasets/whole-detection/archive/`.
- Classes utilizadas: `normal` e `buracos` (com compatibilidade para pasta legada `potholes`).
- Volume identificado no experimento atual: 352 imagens `normal` e 329 imagens `buracos` (total de 681 imagens).

### 2. Pre-processamento
- Redimensionamento para `128 x 128` pixels.
- Conversao de cor BGR para RGB.
- Normalizacao para intervalo `[0, 1]`.
- Divisao treino-validacao estratificada (`80/20`, `random_state=42`).

### 3. Modelo baseline (CNN do zero)
- Arquitetura sequencial com blocos `Conv2D + MaxPooling2D`.
- Camadas densas finais com saida sigmoide (classificacao binaria).
- Otimizador `Adam` e perda `binary_crossentropy`.
- Funcao: estabelecer referencia inicial de desempenho.

### 4. Modelo avancado com transfer learning
- Backbones suportados: `MobileNetV2` e `EfficientNetB0` com pesos ImageNet.
- Cabeca classificadora: `GlobalAveragePooling -> Dropout -> Dense(ReLU) -> Dense(Softmax)`.
- Treinamento em duas fases:
1. Fase A: backbone congelado (treino da cabeca).
2. Fase B: fine-tuning com descongelamento parcial de camadas finais e taxa de aprendizado reduzida.

### 5. Regularizacao e robustez
- Data augmentation no treino (`flip`, `rotation`, `zoom`, `contrast`).
- Uso de `class_weight` para mitigar desbalanceamento residual.
- Callbacks: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`.

### 6. Avaliacao
- Metricas principais: acuracia, F1-macro, AUC-ROC, matriz de confusao e relatorio por classe.
- Visualizacoes: curvas de treino/validacao, exemplos de acerto/erro e Grad-CAM (quando aplicavel).

### 7. Evidencias experimentais registradas
Com base em `outputs/results.csv` (execucao registrada em 01/04/2026):

- Melhor `val_accuracy`: **0.9781**
- Melhor `val_f1`: **0.9781**
- Melhor `val_auc`: **0.9989**
- Melhor `val_loss`: **0.0475**

Esses resultados indicam alto potencial de discriminacao entre classes no conjunto de validacao, com desempenho consistente ao longo das fases de treino.

## Estrutura Relevante
- `notebooks/whole-detection/deteccao-buracos-cnn-baseline.ipynb`: experimento completo.
- `src/deteccao_buracos.py`: pipeline baseline (carregamento, treino e avaliacao).
- `src/deteccao_buracos_transfer.py`: pipeline transfer learning, augmentacao e metricas avancadas.
- `scripts/smoke_test_whole_detection.py`: validacao rapida de integridade do pipeline.

## Consideracoes Finais
O projeto apresenta uma abordagem tecnicamente fundamentada para apoio a inspecoes de pavimento com IA, com foco em reproducibilidade e interpretabilidade. A metodologia adotada permite evolucoes futuras, como validacao cruzada, ampliacao de base e avaliacao em diferentes condicoes de iluminacao e captura.


