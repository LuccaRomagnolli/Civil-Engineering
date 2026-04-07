<div align="center">

<br/>

<img src="../../images/Logo_unb-removebg-preview.png" alt="Universidade de Brasília" width="180"/>

<br/><br/>

# Análise Exploratória da Malha Rodoviária dos EUA (NHPN)
### National Highway Planning Network com foco em engenharia e planejamento

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualiza%C3%A7%C3%A3o-11557C?style=flat-square)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-Estat%C3%ADstica-2E6F95?style=flat-square)](https://seaborn.pydata.org)
[![License](https://img.shields.io/badge/Licença-Acadêmica-4B8BBE?style=flat-square)](#)

<br/>

> **Projeto de Pesquisa**  
> Universidade de Brasília — Departamento de Ciência da Computação

| | |
|---|---|
| **Autor** | Lucca Maximus Romagnolli Soares |
| **Instituição** | Universidade de Brasília (UnB) |
| **Data de Execução** | 06 de abril de 2026 |

<br/>

</div>

---

## Resumo

Este projeto apresenta uma **análise exploratória completa (EDA)** da base `National Highway Planning Network (NHPN)`, com ênfase em distribuição funcional da malha, cobertura por estado, participação de corredores estratégicos e auditoria de consistência dos campos de extensão (`MILES`, `KM`, `Shape__Length`).

O notebook principal `eda-nhpn.ipynb` organiza o fluxo analítico para apoiar decisões em **planejamento de infraestrutura viária**, **priorização de investimento** e **controle de qualidade de dados de rede**.

---

## 1. Contexto e Motivação

Bases nacionais de rodovias são fundamentais para estudos de mobilidade, logística e manutenção da infraestrutura civil. No entanto, sua utilização prática depende de três fatores: interpretação correta de códigos técnicos, visão territorial por estado e validação da consistência métrica dos trechos.

Neste trabalho, foi estruturado um pipeline de EDA com foco em:

- leitura e perfilamento de uma base de grande escala (mais de 600 mil segmentos);
- tradução de códigos (`F_SYSTEM`, `STFIPS`, `NHS`, `STRAHNET`) para leitura técnica aplicada;
- identificação de padrões estruturais da rede (rural/urbano, corredores e continuidade linear);
- geração de insights operacionais para engenharia de transportes.

---

## 2. Metodologia

### 2.1 Base de Dados

| Parâmetro | Valor |
|---|---|
| Fonte | `datasets/NTAD_National_Highway_Planning_Network_-129350642200434263.csv` |
| Unidade de análise | Trecho viário (segmento) |
| Escala geográfica | Estados Unidos (agregações por `STFIPS`) |
| Total de linhas | 626.366 |
| Total de colunas | 46 |

### 2.2 Qualidade e Preparação

- Verificação de estrutura, tipos e unicidade de chaves (`OBJECTID`, `ROUTE_ID`, `RECID`, `FAC_ID`, `LRSKEY`);
- Auditoria de dados faltantes (nível muito baixo, com destaque para `Shape__Length` em 0,002%);
- Mapeamento de códigos FIPS para nome de estados;
- Padronização de categorias para análises comparativas.

### 2.3 Eixos Analíticos do Notebook

1. Extensão da malha por classe funcional (`F_SYSTEM`);
2. Extensão total por estado (km);
3. Corredores principais por sinalização (`SIGNT1`/`SIGN1`);
4. Cobertura do `NHS`;
5. Consistência entre `MILES`, `KM` e `Shape__Length`;
6. Comparativo rural vs. urbano (`URBAN_CODE` / `RUCODE`);
7. Cobertura estratégica militar (`STRAHNET`) por estado;
8. Auditoria de continuidade linear por rota (`ROUTE_ID`, `BEGMP`, `ENDMP`).

---

## 3. Principais Resultados

> Resultados obtidos diretamente da execução registrada no notebook `eda-nhpn.ipynb`.

<div align="center">

| Indicador | Resultado |
|---|:---:|
| Classe funcional com maior extensão | **Minor Arterial (32,87% da malha em milhas)** |
| Estado com maior extensão total | **Texas (54.760 km)** |
| Participação de corredores `I/US` (trechos) | **15,47%** |
| Participação de corredores `I/US` (extensão) | **10,68%** |
| Participação do código `NHS = 1` na extensão total | **10,69%** |
| Mediana da razão `KM/MILES` | **1,609354** (esperado: 1,60934) |
| P99 do erro absoluto na consistência `MILES ↔ KM` | **0,001174 km** |

</div>

### Indicadores de continuidade de rede (aproximação topológica)

- Rotas analisadas: **34.219**;
- Segmentos analisados: **626.366**;
- Segmentos órfãos: **370.727** (**59,19%**);
- Gaps entre segmentos: **10.004**;
- Sobreposições entre segmentos: **405.354**.

Esses resultados evidenciam o potencial da base para análise estratégica em escala nacional, ao mesmo tempo em que reforçam a importância de rotinas de controle topológico para aplicações de roteamento e modelagem de rede.

---

## 4. Estrutura do Projeto

```
.
├── notebooks/
│   └── usa-highways/
│       ├── eda-nhpn.ipynb                          # Notebook principal da análise exploratória
│       └── README.md                               # Documentação do projeto
└── datasets/
    └── NTAD_National_Highway_Planning_Network_-129350642200434263.csv
                                                     # Base NHPN utilizada no estudo
```

---

## 5. Considerações Finais

A EDA confirma que a base NHPN é robusta para análises de planejamento rodoviário em nível nacional, permitindo identificar concentração de extensão por classe funcional, estados prioritários e peso relativo de redes estratégicas como NHS/STRAHNET.

Como próximos avanços técnicos, recomenda-se:

- integrar geometria vetorial original (shapefile/geojson) para análises de conectividade espacial mais fiéis;
- calcular densidade real por área territorial (km/km²) por estado;
- desenvolver indicadores compostos de criticidade para priorização de manutenção;
- acoplar o pipeline a dashboards interativos para monitoramento contínuo.

---

<div align="center">

<br/>

**Universidade de Brasília — UnB**  
Departamento de Engenharia Civil - ENC

<sub>Este documento é parte integrante do projeto acadêmico e deve ser referenciado de acordo com as normas institucionais vigentes.</sub>

<br/>

</div>
