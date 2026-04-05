<div align="center">

<br/>

<img src="../../images/Logo_unb-removebg-preview.png" alt="Universidade de Brasília" width="180"/>

<br/><br/>

# Detecção de Fissuras Superficiais em Concreto
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
| **Data de Execução** | 05 de abril de 2026 |

<br/>

</div>

---

## Resumo

Este projeto investiga a **classificação automática de imagens de superfícies de concreto** em duas classes (`sem_fissura` e `com_fissura`) por meio de técnicas de visão computacional e aprendizado profundo. A proposta combina uma CNN _baseline_ treinada do zero com uma abordagem de _transfer learning_, visando maior desempenho e melhor generalização em cenários reais de inspeção visual.

---

## 1. Contexto e Motivação

A detecção automática de fissuras superficiais em concreto é um problema de alta relevância para a engenharia civil, pois permite acelerar diagnósticos, priorizar intervenções e apoiar estratégias de manutenção preditiva. Soluções baseadas em visão computacional viabilizam inspeções em escala, reduzindo subjetividade e custos operacionais.

Neste trabalho, foi estruturado um **pipeline experimental reprodutível**, com:

- organização padronizada de dados e artefatos de execução;
- controle de sementes aleatórias para garantia de reprodutibilidade;
- comparação objetiva entre modelo _baseline_ e modelo com pesos pré-treinados (ImageNet);
- avaliação quantitativa por múltiplas métricas de classificação.

O notebook principal `fissura-concreto.ipynb` documenta o fluxo experimental completo, da exploração inicial dos dados até a inferência em imagem externa.

---

## 2. Metodologia

### 2.1 Base de Dados e Rotulação

| Parâmetro | Valor |
|---|---|
| Fonte | `datasets/surface-crack-detection/` |
| Classes | `sem_fissura` e `com_fissura` (pastas `Negative` e `Positive`) |
| Volume — classe `sem_fissura` | 20.000 imagens |
| Volume — classe `com_fissura` | 20.000 imagens |
| **Total** | **40.000 imagens** |

### 2.2 Pré-processamento

- Redimensionamento para **128 × 128** pixels;
- Conversão de espaço de cor BGR → RGB;
- Normalização para o intervalo `[0, 1]`;
- Divisão treino–validação estratificada na proporção **80/20** (`random_state = 42`);
- Suporte a subamostragem reprodutível via `MAX_IMAGENS_POR_CLASSE` para controle de memória.

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
- `class_weight` para balanceamento entre classes;
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

> Resultados obtidos a partir de `outputs/results_surface_crack.csv` — execução registrada em **03/04/2026**.

<div align="center">

| Métrica | Melhor Valor |
|---|:---:|
| `val_accuracy` | **0.9994** |
| `val_f1` (macro) | **0.9994** |
| `val_auc` | **1.0000** |
| `val_loss` | **0.0039** |

</div>

Os resultados indicam **excelente capacidade de discriminação entre classes** no conjunto de validação, com desempenho estável ao longo das fases de treinamento. O valor de AUC próximo de 1,0 sugere que o modelo aprendeu representações altamente separáveis entre superfícies íntegras e com fissura.

---

## 4. Estrutura do Projeto

```
.
├── notebooks/
│   └── surface-crack-detection/
│       └── fissura-concreto.ipynb                # Experimento completo documentado
├── src/
│   ├── deteccao_fissuras.py                      # Pipeline baseline para fissuras
│   └── deteccao_buracos_transfer.py              # Utilitários de transfer learning reutilizados
├── datasets/
│   └── surface-crack-detection/                  # Base de dados local (Negative/Positive)
├── models/
│   ├── surface_crack_transfer_phase1_best.keras  # Melhor checkpoint da fase A
│   └── surface_crack_transfer_phase2_best.keras  # Melhor checkpoint da fase B
└── outputs/
    └── results_surface_crack.csv                 # Métricas registradas por execução
```

---

## 5. Considerações Finais

O projeto apresenta uma abordagem tecnicamente fundamentada para apoio à inspeção de estruturas de concreto com inteligência artificial, com ênfase em **reprodutibilidade** e **interpretabilidade dos resultados**. A metodologia adotada é modular e extensível, permitindo evoluções futuras como:

- validação cruzada estratificada (_k-fold_);
- ampliação do conjunto com imagens de campo sob diferentes condições de iluminação e captura;
- avaliação de robustez para variações de câmera, resolução e ruído;
- integração com aplicativos de inspeção assistida em tempo real.

---

<div align="center">

<br/>

**Universidade de Brasília — UnB**  
Departamento de Engenharia Civil - ENC

<sub>Este documento é parte integrante do projeto acadêmico e deve ser referenciado de acordo com as normas institucionais vigentes.</sub>

<br/>

</div>
