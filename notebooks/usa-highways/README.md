<div align="center">

<br/>

<img src="../../images/Logo_unb-removebg-preview.png" alt="Universidade de Brasília" width="160"/>

<br/><br/>

# Análise Exploratória da Malha Rodoviária dos EUA
## National Highway Planning Network (NHPN)

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualização-11557C?style=flat-square)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-Estatística-2E6F95?style=flat-square)](https://seaborn.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![License](https://img.shields.io/badge/Licença-Acadêmica-4B8BBE?style=flat-square)](#licença)

<br/>

> Projeto de pesquisa desenvolvido no âmbito do **Departamento de Engenharia Civil**  
> da Universidade de Brasília (UnB), com foco em planejamento de infraestrutura viária.

| Campo | Detalhe |
|---|---|
| **Autor** | Lucca Maximus Romagnolli Soares |
| **Instituição** | Universidade de Brasília (UnB) |
| **Departamento** | Engenharia Civil — ENC |
| **Data de execução** | 06 de abril de 2026 |

</div>

---

## Visão Geral

Este projeto realiza uma **análise exploratória de dados (EDA)** completa sobre a base *National Highway Planning Network (NHPN)*, que reúne mais de **626 mil segmentos** da malha rodoviária norte-americana. O trabalho cobre desde a auditoria de qualidade dos dados até a extração de insights estratégicos para planejamento de transportes.

Os principais eixos da análise são:

- **Distribuição funcional** da malha por classe de via (`F_SYSTEM`)
- **Cobertura territorial** por estado (extensão em km)
- **Corredores estratégicos**: NHS, STRAHNET e sinalização interestadual
- **Consistência métrica** entre os campos `MILES`, `KM` e `Shape__Length`
- **Continuidade topológica** por rota (segmentos, gaps e sobreposições)

---

## Contexto e Motivação

Bases nacionais de rodovias são fundamentais para estudos de mobilidade, logística e manutenção da infraestrutura civil. Sua utilização prática, porém, exige três condições: interpretação correta de códigos técnicos, visão territorial por estado e validação rigorosa da consistência métrica dos trechos.

Este trabalho estrutura um pipeline de EDA orientado a três perfis de uso:

| Perfil | Aplicação |
|---|---|
| Engenharia de transportes | Priorização de investimentos por classe funcional |
| Planejamento territorial | Cobertura por estado e rede estratégica |
| Controle de qualidade | Auditoria de consistência e topologia da rede |

---

## Dados

| Parâmetro | Valor |
|---|---|
| **Fonte** | NTAD — National Highway Planning Network |
| **Arquivo** | `NTAD_National_Highway_Planning_Network_-129350642200434263.csv` |
| **Unidade de análise** | Trecho viário (segmento) |
| **Escala geográfica** | Estados Unidos (agrupamento por `STFIPS`) |
| **Total de linhas** | 626.366 |
| **Total de colunas** | 46 |
| **Metadata Updated** | July 17, 2025 |
| **Compilação da base** | May 01, 2014 |
| **Cobertura territorial** | 48 estados contíguos + District of Columbia, Alaska, Hawaii e Puerto Rico |
| **Escala nominal** | 1:100,000 |
| **Erro posicional máximo** | 80 metros |

### Fonte oficial e links

- Catálogo Data.gov: https://catalog.data.gov/dataset/national-highway-planning-network1
- Dicionário de dados (DOI): https://doi.org/10.21949/1529044

### Qualidade dos dados

- Dados faltantes em nível muito baixo (destaque: `Shape__Length` ausente em 0,002% dos registros)
- Campos de chave únicos verificados: `OBJECTID`, `ROUTE_ID`, `RECID`, `FAC_ID`, `LRSKEY`
- Códigos FIPS traduzidos para nome completo de cada estado
- Categorias padronizadas para viabilizar análises comparativas

---

## Metodologia

O notebook `eda-nhpn.ipynb` organiza oito eixos analíticos sequenciais:

```
1. Extensão da malha por classe funcional (F_SYSTEM)
2. Extensão total por estado (km)
3. Corredores principais por sinalização (SIGNT1 / SIGN1)
4. Cobertura do NHS (National Highway System)
5. Consistência entre MILES, KM e Shape__Length
6. Comparativo rural vs. urbano (URBAN_CODE / RUCODE)
7. Cobertura estratégica militar (STRAHNET) por estado
8. Auditoria de continuidade linear por rota (ROUTE_ID, BEGMP, ENDMP)
```

---

## Resultados

### Indicadores gerais

| Indicador | Resultado |
|---|:---:|
| Classe funcional com maior extensão | **Minor Arterial — 32,87% da malha (milhas)** |
| Estado com maior extensão total | **Texas — 54.760 km** |
| Participação de corredores I/US (trechos) | **15,47%** |
| Participação de corredores I/US (extensão) | **10,68%** |
| Participação do NHS = 1 na extensão total | **10,69%** |
| Mediana da razão KM/MILES | **1,609354** *(esperado: 1,60934)* |
| P99 do erro absoluto MILES ↔ KM | **0,001174 km** |

### Continuidade topológica da rede

| Métrica | Valor |
|---|:---:|
| Rotas analisadas | 34.219 |
| Segmentos analisados | 626.366 |
| Segmentos órfãos | 370.727 **(59,19%)** |
| Gaps entre segmentos | 10.004 |
| Sobreposições entre segmentos | 405.354 |

> O alto índice de segmentos órfãos e sobreposições não invalida a base para análise estratégica, mas evidencia a necessidade de rotinas de controle topológico antes de qualquer aplicação em roteamento ou modelagem de rede.

---

## Estrutura do Projeto

```
.
├── notebooks/
│   └── usa-highways/
│       ├── eda-nhpn.ipynb      # Notebook principal da análise
│       └── README.md           # Este documento
└── datasets/
    └── NTAD_National_Highway_Planning_Network_-129350642200434263.csv
```

---

## Como Executar

**Pré-requisitos:** Python 3.9+ e Jupyter instalados.

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd <pasta-do-projeto>

# 2. Instale as dependências
pip install pandas matplotlib seaborn jupyter

# 3. Abra o notebook
jupyter notebook notebooks/usa-highways/eda-nhpn.ipynb
```

> Certifique-se de que o arquivo `.csv` está em `datasets/` antes de executar as células.

---

## Próximos Passos

- [ ] Integrar geometria vetorial (shapefile/GeoJSON) para análise espacial de conectividade
- [ ] Calcular densidade real por área territorial (km/km²) por estado
- [ ] Desenvolver indicadores compostos de criticidade para priorização de manutenção
- [ ] Construir dashboard interativo para monitoramento contínuo da rede

---

## Licença

Projeto de caráter acadêmico vinculado à Universidade de Brasília. Cite de acordo com as normas institucionais vigentes.

---

<div align="center">

**Universidade de Brasília — UnB**  
Departamento de Engenharia Civil — ENC

</div>

