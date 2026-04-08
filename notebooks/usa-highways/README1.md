# EDA Completa — National Highway Planning Network (NHPN)

**Autor:** Lucca Maximus Romagnolli Soares — Universidade de Brasília  
**Fonte:** FHWA / USDOT-BTS · National Transportation Atlas Database (NTAD)  
**Compilação:** 01 maio 2014 · Escala nominal 1:100.000 · Erro posicional máx. 80 m

---

## Objetivo

Realizar uma análise exploratória completa do dataset `NTAD_National_Highway_Planning_Network.csv`, com foco em:

- Extensão por categoria funcional (`F_SYSTEM`)
- Densidade da malha por estado (nomes dos estados)
- Corredores principais (`SIGN1` / `SIGNT1`)
- Participação do NHS (`NHS`)
- Consistência entre `MILES`, `KM` e `Shape__Length`
- Sugestões de aplicações práticas para engenharia e planejamento

---

## 1. Visão Geral do Dataset

O NHPN descreve a malha rodoviária principal dos Estados Unidos, cobrindo os 48 estados contíguos, o Distrito de Columbia, Alasca, Havaí e Porto Rico. Cada linha representa um segmento viário com atributos geométricos, funcionais e de classificação de sistema.

| Atributo | Valor |
|---|---|
| Total de segmentos | 626.366 linhas |
| Total de colunas | 46 atributos |
| Extensão total | 436.891 mi (≈ 703.110 km) |
| Dados faltantes | < 0,003% (SIGN1, SIGNN1, Shape__Length) |
| Escala nominal | 1:100.000 |
| Erro posicional máximo | 80 metros |

O dataset apresenta qualidade de dados excelente: nenhum valor nulo em `MILES` ou `KM`, e menos de 25 registros com campos de sinalização ou geometria ausentes em um universo de mais de 600 mil linhas.

---

## 2. Extensão por Categoria Funcional (F_SYSTEM)

O campo `F_SYSTEM` classifica cada segmento pelo nível hierárquico funcional da via, seguindo a taxonomia do Federal Highway Administration.

| Código | Descrição | Milhas | % do total |
|---|---|---|---|
| 4 | Arterial Urbana Menor | 143.585 | 32,9% |
| 3 | Arterial Rural Principal | 139.541 | 31,9% |
| 5 | Coletora Rural | 66.523 | 15,2% |
| 1 | Interestatal | 45.879 | 10,5% |
| 0 | Não classificada | 25.852 | 5,9% |
| 2 | Arterial Urbana Principal | 14.414 | 3,3% |
| 6 | Ferry / Balsa | 762 | 0,2% |
| 7 | Estrada não pavimentada | 335 | 0,1% |

As arteriais rurais e urbanas menores (F=3 e F=4) dominam em extensão, respondendo juntas por **64,8% da malha total**. As Interestatais (F=1), apesar de concentrarem o maior volume de tráfego do país, correspondem a apenas **10,5% da extensão** — evidência clara da hierarquia funcional da rede: alta capacidade com extensão contida.

As categorias 6 (ferries) e 7 (não pavimentadas) totalizam menos de 0,3% da extensão e funcionam primordialmente como conectores de continuidade topológica da rede, garantindo cobertura em regiões insulares e de fronteira.

---

## 3. Densidade da Malha por Estado

A distribuição da extensão viária por estado reflete tanto as dimensões territoriais quanto a densidade populacional e a estrutura econômica regional.

| Posição | Estado | Milhas |
|---|---|---|
| 1 | Texas | 34.027 |
| 2 | California | 24.304 |
| 3 | New York | 17.089 |
| 4 | Georgia | 16.335 |
| 5 | Pennsylvania | 13.869 |
| 6 | Illinois | 13.484 |
| 7 | Minnesota | 13.237 |
| 8 | Florida | 13.201 |
| 9 | Wisconsin | 12.104 |
| 10 | Michigan | 11.436 |
| 11 | Ohio | 11.204 |
| 12 | North Carolina | 11.183 |
| 13 | Kansas | 10.966 |
| 14 | Missouri | 10.485 |
| 15 | Iowa | 10.089 |

Texas e California lideram em extensão absoluta, reflexo direto de suas dimensões territoriais. **Nova York** destaca-se ao ocupar o 3º lugar apesar de área relativamente modesta, indicando alta densidade da rede urbana e suburbana. **Novo México** registra o maior número de segmentos individuais (82.783 linhas), possivelmente por maior granularidade na segmentação das arteriais rurais nos dados estaduais.

---

## 4. Participação do Sistema Nacional de Rodovias (NHS)

O campo `NHS` indica se o segmento integra o National Highway System, o principal instrumento de priorização de investimentos federais em infraestrutura rodoviária nos EUA.

| Código NHS | Descrição | Milhas |
|---|---|---|
| 0 | Não pertence ao NHS | 272.698 |
| 7 | NHS — outras categorias | 98.772 |
| 1 | Interestatal NHS | 46.694 |
| 3 | Outras rodovias NHS | 14.316 |
| 8 | NHS Estratégico | 2.367 |
| 4 | Conector NHS | 1.975 |
| 9 | NHS Militar | 25 |
| 10 | NHS de Emergência | 45 |

Do total da rede, **164.194 mi (≈ 37,6%)** integram alguma categoria NHS. As Interestatais (NHS=1) respondem por 46.694 mi — praticamente a totalidade da malha Interestatal do país. Os segmentos NHS militares (código 9) e de emergência (código 10) somam apenas 70 mi, refletindo sua natureza altamente especializada.

---

## 5. Corredores Principais (SIGN1 / SIGNT1)

O campo `SIGNT1` classifica o tipo de via segundo sua sinalização oficial, enquanto `SIGN1` e `SIGNN1` armazenam o prefixo e número da rodovia, respectivamente.

| Código | Tipo | Milhas |
|---|---|---|
| S | State Route (Rodovia Estadual) | 212.938 |
| U | US Route (Rodovia Federal) | 133.002 |
| I | Interstate (Interestatal) | 46.653 |
| (vazio) | Sem sinalização explícita | 35.962 |
| C | County Road (Rodovia de County) | 7.630 |
| O | Other (Outras) | 391 |
| N | National Park Road | 215 |
| F | Forest Road | 81 |
| M | Military Road | 17 |
| T | Turnpike | 1 |

As rodovias estaduais (S) dominam em extensão total, mas as Interestatais (I) carregam incomparavelmente maior volume de tráfego por quilômetro. Aproximadamente **8,2% dos segmentos** (35.962 mi) não possuem sinalização explícita, tipicamente trechos locais, conectores internos ou rampas de acesso.

Os campos `SIGN2` e `SIGN3` permitem múltiplas designações simultâneas — padrão em trechos onde uma via carrega ao mesmo tempo numeração Interestatal e US Route (ex.: I-90 / US-20). Isso é especialmente comum no oeste dos EUA, onde o traçado histórico das US Routes foi parcialmente absorvido pela malha Interestatal.

---

## 6. Consistência entre MILES, KM e Shape__Length

### 6.1 Conversão MILES ↔ KM

A conversão entre os campos `MILES` e `KM` é altamente consistente em todo o dataset, com discrepância máxima de **0,0015 km** e média de **0,00045 km** por segmento — erro de arredondamento desprezível, dentro do esperado para armazenamento em ponto flutuante de precisão simples.

```
KM ≈ MILES × 1,60934
Discrepância máxima: 0,0015 km
Discrepância média:  0,00045 km
```

### 6.2 Shape__Length e suas unidades

O campo `Shape__Length` **não está em quilômetros** — seus valores são expressos em **graus decimais** no sistema geodésico de referência do arquivo (WGS84 ou NAD83). A razão empírica entre `KM` e `Shape__Length` confirma isso:

```
Razão KM / Shape__Length → média: 98,6  |  mediana: 97,7
```

Esse valor é coerente com a latitude média dos EUA (~38°N), onde 1° de longitude equivale a aproximadamente 88 km e 1° de latitude a 111 km — resultando numa razão de conversão de ~95–105 km/grau, dependendo da orientação e latitude do segmento.

### 6.3 Resumo de qualidade

| Verificação | Resultado | Status |
|---|---|---|
| KM = MILES × 1,60934 | Discrepância máx. 0,0015 km | ✓ consistente |
| Shape__Length (unidade) | Graus decimais — razão KM/Shape ≈ 98 | ✓ esperado |
| Dados faltantes em MILES/KM | Zero valores nulos | ✓ completo |
| Shape__Length nulos | 10 registros (0,0016%) | ⚠ negligível |
| SIGN1 / SIGNN1 nulos | 7–8 registros (< 0,002%) | ⚠ negligível |

Para modelagem de rede, recomenda-se utilizar **KM como campo métrico primário** e recalcular `Shape__Length` em metros via reprojeção para um CRS métrico adequado — por exemplo, **EPSG:5070** (Albers Equal Area Conus) — antes de qualquer análise espacial quantitativa de área ou comprimento.

---

## 7. Aplicações Práticas em Engenharia e Planejamento

### 7.1 Modelagem de redes e roteirização

Os campos `CONN_ID`, `FAC_ID` e `LRSKEY` permitem reconstruir a topologia completa da rede como grafo dirigido. Esse grafo é diretamente aplicável a algoritmos de menor caminho (Dijkstra, A*) para logística de cargas, resposta a emergências e análise de resiliência da rede frente a bloqueios ou eventos de desastre natural.

### 7.2 Análise de acessibilidade territorial

Combinando `STFIPS`, `URBAN_CODE` e `F_SYSTEM` é possível calcular índices de acessibilidade por county — identificando regiões com déficit de conectividade arterial. Esse tipo de análise é relevante para políticas de equidade de infraestrutura e priorização de investimentos via programas NHS e STRAHNET.

### 7.3 Monitoramento de desempenho (HPMS)

O NHPN é a base geoespacial do Highway Performance Monitoring System. Cruzando com dados de VMT (vehicle miles traveled) e condição do pavimento, é possível calcular índices de desempenho por segmento — suporte direto à visualização do painel HPMS do FHWA.

### 7.4 Planejamento de corredores logísticos

A combinação `STRAHNET + NHS` delimita os corredores de interesse estratégico militar e econômico nacional. Útil para planejamento de infraestrutura de cargas pesadas, identificação de gargalos de capacidade e priorização de modernização de pontes e viadutos em rotas críticas.

### 7.5 Integração com sensoriamento remoto e SIG

`Shape__Length` em graus + `STFIPS` viabilizam joins espaciais com shapefiles estaduais, dados de clima, risco de desastres naturais (FEMA) e cobertura de solo. Essa integração serve de base para análise de vulnerabilidade climática da malha e planejamento de resiliência em rodovias costeiras e de planície sujeitas a inundações.

---

## Referências

- Federal Highway Administration (FHWA). *National Highway Planning Network Documentation*. U.S. Department of Transportation, 2014.
- Bureau of Transportation Statistics (BTS). *National Transportation Atlas Database (NTAD)*. USDOT, 2014.
- FHWA. *Highway Performance Monitoring System (HPMS) Field Manual*. Washington D.C., 2014.

---

*Dataset compilado em 01 maio 2014 · Escala 1:100.000 · Erro posicional máx. 80 m · 626.366 segmentos · 46 atributos*