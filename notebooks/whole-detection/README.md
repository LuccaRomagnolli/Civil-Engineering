<div align="center">

<br/>

<img src="../../images/Logo_unb-removebg-preview.png" alt="Universidade de Brasília" width="180"/>

<br/><br/>

# Detecção de Buracos em Pavimento
### com Redes Neurais Convolucionais e Transfer Learning

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Keras](https://img.shields.io/badge/Keras-API-D00000?style=flat-square&logo=keras&logoColor=white)](https://keras.io)
[![License](https://img.shields.io/badge/Licença-Acadêmica-4B8BBE?style=flat-square)](#)

<br/>

> **Trabalho de Conclusão / Projeto de Pesquisa**  
> Universidade de Brasília — Departamento de Ciência da Computação

| | |
|---|---|
| **Autor** | Lucca Maximus Romagnolli |
| **Instituição** | Universidade de Brasília (UnB) |
| **Data de Execução** | 01 de abril de 2026 |

<br/>

</div>

---

## Resumo

Este projeto investiga a **classificação automática de imagens de pavimento** em duas classes (`normal` e `buracos`) por meio de técnicas de visão computacional e aprendizado profundo. A proposta combina uma CNN _baseline_ treinada do zero com uma abordagem de _transfer learning_, visando maior desempenho e melhor generalização em cenário real de inspeção visual de vias urbanas.

---

## 1. Contexto e Motivação

A detecção automática de patologias superficiais no pavimento é um problema de alta relevância para a engenharia civil e para a gestão urbana, pois permite acelerar diagnósticos e apoiar estratégias de manutenção preditiva. Soluções baseadas em visão computacional viabilizam a inspeção sistemática de vias em escala, reduzindo custos operacionais e riscos associados a avaliações manuais.

Neste trabalho, foi estruturado um **pipeline experimental reprodutível**, com:

- organização padronizada de dados e scripts de execução;
- controle de sementes aleatórias para garantia de reprodutibilidade;
- comparação objetiva entre modelo _baseline_ e modelo com pesos pré-treinados (ImageNet);
- avaliação quantitativa por múltiplas métricas de classificação.

O notebook principal `deteccao-buracos-cnn-baseline.ipynb` documenta o fluxo experimental completo, da exploração inicial dos dados até a inferência em imagem externa de campo.

---

## 2. Metodologia

### 2.1 Base de Dados e Rotulação

| Parâmetro | Valor |
|---|---|
| Fonte | `datasets/whole-detection/archive/` |
| Classes | `normal` e `buracos` (com compatibilidade para pasta legada `potholes`) |
| Volume — classe `normal` | 352 imagens |
| Volume — classe `buracos` | 329 imagens |
| **Total** | **681 imagens** |

### 2.2 Pré-processamento

- Redimensionamento para **128 × 128** pixels;
- Conversão de espaço de cor BGR → RGB;
- Normalização para o intervalo `[0, 1]`;
- Divisão treino–validação estratificada na proporção **80/20** (`random_state = 42`).

### 2.3 Modelo Baseline — CNN Treinada do Zero

Arquitetura sequencial composta por blocos `Conv2D + MaxPooling2D`, seguidos de camadas densas com saída sigmoide para classificação binária. Otimizador `Adam` com função de perda `binary_crossentropy`. Esta etapa tem por objetivo estabelecer uma **referência inicial de desempenho** para comparação com abordagens mais avançadas.

### 2.4 Modelo Avançado — Transfer Learning

**Backbones suportados:** `MobileNetV2` e `EfficientNetB0`, ambos inicializados com pesos ImageNet.

**Cabeça classificadora:**

```
GlobalAveragePooling2D → Dropout → Dense (ReLU) → Dense (Softmax)
```

**Treinamento em duas fases:**

| Fase | Descrição |
|---|---|
| **Fase A** | Backbone congelado — treinamento exclusivo da cabeça classificadora |
| **Fase B** | _Fine-tuning_ — descongelamento parcial das camadas finais do backbone com taxa de aprendizado reduzida |

### 2.5 Regularização e Robustez

- **Data augmentation** no conjunto de treino: `flip`, `rotation`, `zoom`, `contrast`;
- `class_weight` para mitigação de desbalanceamento residual entre classes;
- Callbacks: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`.

### 2.6 Avaliação

**Métricas principais:**

- Acurácia, F1-macro, AUC-ROC;
- Matriz de confusão e relatório detalhado por classe.

**Visualizações:**

- Curvas de treino/validação ao longo das épocas;
- Exemplos de acerto e erro de classificação;
- Mapas de atenção **Grad-CAM** (quando aplicável).

---

## 3. Resultados Experimentais

> Resultados obtidos a partir de `outputs/results.csv` — execução registrada em **01/04/2026**.

<div align="center">

| Métrica | Melhor Valor |
|---|:---:|
| `val_accuracy` | **0.9781** |
| `val_f1` (macro) | **0.9781** |
| `val_auc` | **0.9989** |
| `val_loss` | **0.0475** |

</div>

Os resultados indicam **alto potencial de discriminação entre classes** no conjunto de validação, com desempenho consistente ao longo das fases de treinamento. O valor de AUC próximo a 1,0 evidencia que o modelo aprendeu representações altamente separáveis entre as categorias `normal` e `buracos`.

---

## 4. Estrutura do Projeto

```
.
├── notebooks/
│   └── whole-detection/
│       └── deteccao-buracos-cnn-baseline.ipynb   # Experimento completo documentado
├── src/
│   ├── deteccao_buracos.py                        # Pipeline baseline
│   └── deteccao_buracos_transfer.py               # Pipeline transfer learning
├── scripts/
│   └── smoke_test_whole_detection.py              # Validação rápida de integridade
├── datasets/
│   └── whole-detection/archive/                   # Base de dados local
└── outputs/
    └── results.csv                                # Métricas registradas por execução
```

---

## 5. Considerações Finais

O projeto apresenta uma abordagem tecnicamente fundamentada para apoio a inspeções de pavimento com inteligência artificial, com ênfase em **reprodutibilidade** e **interpretabilidade dos resultados**. A metodologia adotada é modular e extensível, permitindo evoluções futuras como:

- validação cruzada estratificada (_k-fold_);
- ampliação da base de dados com imagens de diferentes regiões e condições climáticas;
- avaliação sob variação de iluminação, resolução e ângulo de captura;
- integração com sistemas embarcados para inspeção em tempo real.

---

<div align="center">

<br/>

**Universidade de Brasília — UnB**  
Departamento de Engenharia Civil - ENC

<sub>Este documento é parte integrante do projeto acadêmico e deve ser referenciado de acordo com as normas institucionais vigentes.</sub>

<br/>

</div>
