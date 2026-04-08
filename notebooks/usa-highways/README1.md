<div align="center">

<br/>

<img src="../../images/Logo_unb-removebg-preview.png" alt="Universidade de Brasília" width="160"/>

<br/><br/>

# EDA Completa — National Highway Planning Network (NHPN)
## Relatório Consolidado de Resultados

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualização-11557C?style=flat-square)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-Estatística-2E6F95?style=flat-square)](https://seaborn.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![License](https://img.shields.io/badge/Licença-Acadêmica-4B8BBE?style=flat-square)](#licença)

<br/>

> Relatório consolidado a partir das saídas do notebook `eda-nhpn.ipynb`  
> desenvolvido no âmbito do **Departamento de Engenharia Civil**  
> da Universidade de Brasília (UnB), com foco em planejamento de infraestrutura viária.

| Campo | Detalhe |
|---|---|
| **Autor** | Lucca Maximus Romagnolli Soares |
| **Instituição** | Universidade de Brasília (UnB) |
| **Departamento** | Engenharia Civil — ENC |
| **Fonte** | FHWA / USDOT-BTS — National Transportation Atlas Database (NTAD) |
| **Metadata Updated** | July 17, 2025 |
| **Compilação da base** | 01 de maio de 2014 |

</div>

---

## Visão Geral

Este documento consolida, em formato de relatório, os principais resultados obtidos no notebook `eda-nhpn.ipynb` sobre a base `NTAD_National_Highway_Planning_Network_-129350642200434263.csv`, que reúne mais de **626 mil segmentos** da malha rodoviária norte-americana.

Os principais eixos da análise são:

- **Distribuição funcional** da malha por classe de via (`F_SYSTEM`)
- **Cobertura territorial** por estado (`STFIPS`) — extensão em km e milhas
- **Sinalização e corredores principais** (`SIGN1`, `SIGNT1`)
- **Participação do National Highway System** (`NHS`)
- **Consistência métrica** entre `MILES`, `KM` e `Shape__Length`
- **Contraste rural vs. urbano** (`URBAN_CODE`)
- **Cobertura estratégica militar** (`STRAHNET`) por estado
- **Continuidade topológica** por rota (`ROUTE_ID`, `BEGMP`, `ENDMP`)

---

## Contexto e Motivação

Bases nacionais de rodovias são fundamentais para estudos de mobilidade, logística e manutenção da infraestrutura civil. Sua utilização prática, porém, exige três condições: interpretação correta de códigos técnicos, visão territorial por estado e validação rigorosa da consistência métrica dos trechos.

Este relatório estrutura os resultados do pipeline de EDA orientado a três perfis de uso:

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
| **Total de segmentos** | 626.366 |
| **Total de colunas** | 46 |
| **Extensão total** | 436.891,494 mi — 703.109,679 km |
| **Valores nulos em `MILES`** | 0 |
| **Valores nulos em `KM`** | 0 |
| **Valores nulos em `Shape__Length`** | 10 registros (0,002%) |
| **Valores nulos em `SIGN1`** | 7 registros |
| **Valores nulos em `SIGNN1`** | 8 registros |
| **Escala nominal** | 1:100.000 |
| **Erro posicional máximo** | 80 metros |
| **Cobertura territorial** | 48 estados contíguos + DC, Alaska, Hawaii e Puerto Rico |

### Fonte oficial e links

- Catálogo Data.gov: https://catalog.data.gov/dataset/national-highway-planning-network1
- Dicionário de dados (DOI): https://doi.org/10.21949/1529044

### Qualidade dos dados

Em termos de completude, a base é muito consistente: os campos métricos principais estão completos e os poucos nulos concentram-se em campos de sinalização e comprimento geométrico. Campos de chave únicos verificados: `OBJECTID`, `ROUTE_ID`, `RECID`, `FAC_ID` e `LRSKEY`.

---

## Painel Executivo

| Dimensão | Resultado principal |
|---|---|
| **Escala da rede** | 626.366 segmentos — 703.109,679 km |
| **Classe funcional dominante** | `Minor Arterial` — 32,865% das milhas |
| **Estado com maior extensão** | Texas — 54.760,398 km |
| **Participação recorte `I/US`** | 15,469% dos trechos e 10,678% das milhas |
| **Participação `NHS = 1`** | 10,688% da extensão |
| **Participação total `NHS > 0`** | 37,582% da extensão |
| **Predomínio territorial** | Malha rural — 70,642% das milhas |
| **Cobertura STRAHNET** | 62.628,113 mi — 14,335% da rede |
| **Consistência métrica** | Mediana `KM/MILES = 1,609354` |
| **Qualidade de conversão** | P99 do erro absoluto `KM ↔ MILES = 0,001174 km` |
| **Continuidade linear** | 59,187% de segmentos órfãos — 10.004 gaps — 405.354 overlaps |

> A base é métrico-funcionalmente confiável para diagnóstico e priorização, mas exige cuidado topológico antes de ser usada em roteamento ou simulação de rede.

---

## Resultados

### 1. Extensão por Categoria Funcional (`F_SYSTEM`)

| Código | Classe | Milhas | % das milhas |
|---|---|---:|---:|
| 4 | Minor Arterial | 143.585,040 | 32,865% |
| 3 | Other Principal Arterial | 139.540,869 | 31,939% |
| 5 | Major Collector | 66.523,284 | 15,227% |
| 1 | Interstate | 45.878,900 | 10,501% |
| 0 | Indefinido | 25.852,455 | 5,917% |
| 2 | Other Freeways & Expressways | 14.413,731 | 3,299% |
| 6 | Minor Collector | 762,326 | 0,174% |
| 7 | Local | 334,889 | 0,077% |

As duas classes arteriais centrais — `Minor Arterial` e `Other Principal Arterial` — concentram juntas **64,804%** de toda a extensão em milhas. As `Interstate`, embora sejam o recorte mais conhecido da rede americana, representam apenas **10,501%** da extensão total, reforçando a hierarquia funcional observada: alta relevância logística, mas menor cobertura absoluta que as arteriais.

---

### Extensão por Estado

| Posição | Estado | Quilômetros | Milhas | Segmentos |
|---|---|---:|---:|---:|
| 1 | Texas | 54.760,398 | 34.026,488 | 35.270 |
| 2 | California | 39.114,527 | 24.304,446 | 63.131 |
| 3 | New York | 27.502,380 | 17.089,208 | 26.072 |
| 4 | Georgia | 26.288,268 | 16.334,777 | 16.320 |
| 5 | Pennsylvania | 22.319,938 | 13.868,941 | 17.838 |
| 6 | Illinois | 21.700,666 | 13.484,150 | 15.911 |
| 7 | Minnesota | 21.302,162 | 13.236,558 | 7.665 |
| 8 | Florida | 21.244,318 | 13.200,553 | 15.433 |
| 9 | Wisconsin | 19.479,617 | 12.104,066 | 4.411 |
| 10 | Michigan | 18.404,721 | 11.436,147 | 15.060 |

> **Destaque:** Texas lidera com folga em extensão total. California aparece em segundo, com volume alto de segmentos. New Mexico não figura no top 10 em extensão, mas registra o maior número de segmentos da base: **82.783** — evidenciando que comprimento total e granularidade de segmentação não caminham necessariamente juntos.

---

### Sinalização e Corredores Principais (`SIGNT1`, `SIGN1`)

#### Distribuição geral por tipo de sinalização

| Código `SIGNT1` | Tipo | Trechos | Milhas | % trechos | % milhas |
|---|---|---:|---:|---:|---:|
| `S` | State Highway | 250.111 | 212.938,115 | 39,930% | 48,739% |
| `U` | U.S. Highway | 182.889 | 133.002,212 | 29,198% | 30,443% |
| `I` | Interstate | 96.892 | 46.652,531 | 15,469% | 10,678% |
| vazio | Sem sinalização explícita | 87.797 | 35.962,427 | 14,017% | 8,231% |
| `C` | County Road | 6.231 | 7.630,405 | 0,995% | 1,747% |
| `O` | Other | 1.893 | 391,157 | 0,302% | 0,090% |

As rodovias estaduais (`S`) dominam a malha em extensão e em número de trechos. As `U.S. Highways` (`U`) aparecem como a segunda categoria mais relevante, enquanto as `Interstate` respondem por uma fatia menor em extensão, apesar da importância estrutural.

#### Observação metodológica

No notebook, a célula de corredores principais usa o filtro `SIGNT1 in {'I', 'US'}`. Na base, o código observado para `U.S. Highway` é `U`, e não `US`. Por isso, o indicador salvo no notebook para `I/US` — **15,469% dos trechos** e **10,678% das milhas** — na prática coincide com os segmentos `Interstate`, e não com a soma `Interstate + U.S. Highway`.

#### Top 15 rotas por extensão

| Posição | Rota | Tipo | Milhas | Trechos |
|---|---|---|---:|---:|
| 1 | I80 | Interstate | 2.788,708 | 4.118 |
| 2 | I90 | Interstate | 2.713,600 | 4.469 |
| 3 | I40 | Interstate | 2.468,539 | 7.352 |
| 4 | I10 | Interstate | 2.392,978 | 5.217 |
| 5 | I70 | Interstate | 2.069,717 | 2.862 |
| 6 | I95 | Interstate | 1.914,104 | 4.204 |
| 7 | I75 | Interstate | 1.792,130 | 3.169 |
| 8 | I20 | Interstate | 1.488,328 | 2.083 |
| 9 | I15 | Interstate | 1.470,942 | 2.685 |
| 10 | I35 | Interstate | 1.468,640 | 1.896 |
| 11 | I94 | Interstate | 1.441,820 | 2.104 |
| 12 | I5 | Interstate | 1.429,101 | 6.162 |
| 13 | I25 | Interstate | 1.092,940 | 6.007 |
| 14 | I55 | Interstate | 957,361 | 1.139 |
| 15 | I84 | Interstate | 945,926 | 1.441 |

---

### Participação do National Highway System (`NHS`)

| Código NHS | Trechos | Milhas | % das milhas |
|---|---:|---:|---:|
| 0 | 344.513 | 272.697,879 | 62,418% |
| 7 | 147.511 | 98.772,084 | 22,608% |
| 1 | 96.938 | 46.694,114 | 10,688% |
| 3 | 24.557 | 14.315,787 | 3,277% |
| 8 | 8.388 | 2.366,657 | 0,542% |
| 4 | 3.676 | 1.974,945 | 0,452% |
| 10 | 666 | 45,023 | 0,010% |
| 9 | 117 | 25,005 | 0,006% |

Somando todas as categorias com `NHS > 0`, a rede federalizada responde por **164.193,615 milhas** — equivalentes a **37,582%** da extensão total. O código `1` sozinho representa **10,688%** da malha. Esse resultado é importante para planejamento de funding e governança, separando claramente a parcela da rede com maior aderência a programas e critérios federais.

---

### Contraste Rural vs. Urbano

| Área | Segmentos | Milhas | % segmentos | % milhas |
|---|---:|---:|---:|---:|
| Rural | 277.123 | 308.628,170 | 44,243% | 70,642% |
| Urbano | 349.243 | 128.263,324 | 55,757% | 29,358% |

A rede urbana concentra mais segmentos, mas a rede rural concentra muito mais extensão total — sugerindo segmentação mais fragmentada em ambiente urbano e trechos mais longos no território rural.

#### Classes dominantes por contexto

| Área | Classe líder | Milhas | % da área |
|---|---|---:|---:|
| Rural | Minor Arterial | 123.078,711 | 39,879% |
| Urbano | Other Principal Arterial | 53.679,632 | 41,851% |

---

### Cobertura STRAHNET

O recorte `STRAHNET` destaca corredores de relevância estratégica para mobilidade militar e logística nacional. Na escala da base inteira, o STRAHNET soma **62.628,113 milhas** — equivalentes a **14,335%** da rede.

| Posição | Estado | % da extensão estadual em STRAHNET | Milhas STRAHNET | Milhas totais |
|---|---|---:|---:|---:|
| 1 | Alaska | 32,970% | 1.378,718 | 4.181,728 |
| 2 | Utah | 24,944% | 1.259,788 | 5.050,510 |
| 3 | Delaware | 21,786% | 154,483 | 709,106 |
| 4 | Arizona | 19,769% | 1.453,168 | 7.350,714 |
| 5 | Alabama | 19,542% | 1.884,143 | 9.641,433 |
| 6 | North Carolina | 18,740% | 2.095,549 | 11.182,471 |
| 7 | Maryland | 18,727% | 651,628 | 3.479,553 |
| 8 | California | 18,532% | 4.503,993 | 24.304,446 |
| 9 | Virginia | 18,332% | 1.652,887 | 9.016,420 |
| 10 | New Mexico | 18,222% | 1.456,617 | 7.993,712 |

---

### Consistência entre `MILES`, `KM` e `Shape__Length`

#### Conversão `MILES ↔ KM`

| Verificação | Valor |
|---|---:|
| Mediana de `KM / MILES` | 1,609354 |
| Erro absoluto médio | 0,000453 km |
| Erro absoluto máximo | 0,001525 km |
| Percentil 99 do erro absoluto | 0,001174 km |

Os campos `MILES` e `KM` estão altamente coerentes. A diferença observada é compatível com arredondamento numérico e não representa problema prático para análise exploratória ou indicadores executivos.

#### Interpretação de `Shape__Length`

| Medida | Valor |
|---|---:|
| Média de `KM / Shape__Length` | 98,550 |
| Mediana de `KM / Shape__Length` | 97,711 |

Essa razão confirma que `Shape__Length` não está em quilômetros — a leitura é consistente com geometria em graus decimais, o que exige reprojeção para um CRS métrico antes de qualquer uso espacial quantitativo rigoroso.

---

### Continuidade Topológica da Rede

A análise de continuidade usa `ROUTE_ID`, `BEGMP` e `ENDMP` para aproximar conexões lineares por rota, com tolerância de 0,01 milha entre segmentos consecutivos.

| Indicador | Valor |
|---|---:|
| Rotas analisadas | 34.219 |
| Segmentos analisados | 626.366 |
| Segmentos órfãos | 370.727 **(59,187%)** |
| Gaps entre segmentos | 10.004 |
| Overlaps entre segmentos | 405.354 |
| Mediana de `delta_next` | −1,118 |

> O alto índice de segmentos órfãos e overlaps não invalida a base para análise estratégica, mas evidencia a necessidade de rotinas de controle topológico antes de qualquer aplicação em roteamento ou modelagem de rede. O volume de overlaps sugere segmentação sobreposta, inconsistências em mileposts ou coexistência de geometrias lineares com lógicas de cadastro distintas.

---

## Leitura Gerencial

Com base nos resultados do notebook, as principais implicações para engenharia e planejamento são:

- A rede possui escala suficiente para priorização nacional, estadual e por corredor
- A estrutura funcional é liderada por arteriais, e não apenas por interestaduais
- A cobertura federal (`NHS`) e estratégica (`STRAHNET`) permite separar carteiras por criticidade e funding
- A consistência métrica é alta, favorecendo dashboards, comparações e indicadores
- A continuidade topológica ainda exige saneamento antes de estudos de conectividade operacional

### Agenda sugerida de curto prazo

1. Implantar rotina de QA topológico por estado e por rota
2. Estruturar carteira de investimento cruzando `F_SYSTEM`, `NHS`, `STRAHNET` e extensão estadual
3. Publicar painel executivo com KPIs padronizados por estado, corredor e risco de continuidade

---

## Próximos Passos

- [ ] Integrar geometria vetorial (shapefile/GeoJSON) para análise espacial de conectividade
- [ ] Calcular densidade real por área territorial (km/km²) por estado
- [ ] Desenvolver indicadores compostos de criticidade para priorização de manutenção
- [ ] Construir dashboard interativo para monitoramento contínuo da rede

---

## Estrutura do Projeto

```
.
├── notebooks/
│   └── usa-highways/
│       ├── eda-nhpn.ipynb      # Notebook principal da análise
│       ├── README.md           # Visão geral e metodologia
│       └── README1.md          # Este relatório de resultados
└── datasets/
    └── NTAD_National_Highway_Planning_Network_-129350642200434263.csv
```

---

## Referências

- Federal Highway Administration (FHWA). *National Highway Planning Network*.
- Bureau of Transportation Statistics (BTS). *National Transportation Atlas Database (NTAD)*.
- U.S. Department of Transportation (USDOT). Documentação oficial do NHPN / NTAD.
- Catálogo Data.gov: https://catalog.data.gov/dataset/national-highway-planning-network1
- Dicionário de dados (DOI): https://doi.org/10.21949/1529044

---

## Licença

Projeto de caráter acadêmico vinculado à Universidade de Brasília. Cite de acordo com as normas institucionais vigentes.

---

<div align="center">

**Universidade de Brasília — UnB**  
Departamento de Engenharia Civil — ENC

</div>
