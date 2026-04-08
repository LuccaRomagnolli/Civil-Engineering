diff --git a/c:\Users\luccasoares\Desktop\Civil-Engineering\notebooks\usa-highways\README1.md b/c:\Users\luccasoares\Desktop\Civil-Engineering\notebooks\usa-highways\README1.md
new file mode 100644
--- /dev/null
+++ b/c:\Users\luccasoares\Desktop\Civil-Engineering\notebooks\usa-highways\README1.md
@@ -0,0 +1,300 @@
+# EDA Completa - National Highway Planning Network (NHPN)
+
+**Autor:** Lucca Maximus Romagnolli Soares - Universidade de Brasilia  
+**Fonte:** FHWA / USDOT-BTS - National Transportation Atlas Database (NTAD)  
+**Metadata Updated:** July 17, 2025  
+**Compilacao da base:** 01 maio 2014  
+**Escala nominal:** 1:100.000  
+**Erro posicional maximo:** 80 m
+
+---
+
+## Objetivo
+
+Consolidar, em formato de relatorio, os principais resultados obtidos no notebook `eda-nhpn.ipynb` sobre a base `NTAD_National_Highway_Planning_Network_-129350642200434263.csv`, com foco em:
+
+- extensao da malha por classe funcional (`F_SYSTEM`)
+- extensao total por estado (`STFIPS`)
+- sinalizacao e corredores principais (`SIGN1`, `SIGNT1`)
+- participacao do National Highway System (`NHS`)
+- consistencia entre `MILES`, `KM` e `Shape__Length`
+- contraste rural x urbano (`URBAN_CODE`)
+- cobertura estrategica da rede (`STRAHNET`)
+- continuidade linear aproximada por rota (`ROUTE_ID`, `BEGMP`, `ENDMP`)
+
+---
+
+## 1. Datacard do Dataset
+
+O NHPN descreve a malha rodoviaria principal dos Estados Unidos e cobre os 48 estados contiguos, o District of Columbia, Alaska, Hawaii e Puerto Rico. Cada linha representa um segmento viario com atributos funcionais, administrativos e metricos.
+
+| Atributo | Valor |
+|---|---|
+| Arquivo analisado | `NTAD_National_Highway_Planning_Network_-129350642200434263.csv` |
+| Total de segmentos | 626.366 |
+| Total de colunas | 46 |
+| Extensao total | 436.891,494 mi |
+| Extensao total | 703.109,679 km |
+| Valores nulos em `MILES` | 0 |
+| Valores nulos em `KM` | 0 |
+| Valores nulos em `Shape__Length` | 10 registros |
+| Valores nulos em `SIGN1` | 7 registros |
+| Valores nulos em `SIGNN1` | 8 registros |
+| Escala nominal | 1:100.000 |
+| Erro posicional maximo | 80 m |
+
+Em termos de completude, a base e muito consistente: os campos metricos principais estao completos e os poucos nulos concentram-se em campos de sinalizacao e comprimento geometrico.
+
+---
+
+## 2. Painel Executivo
+
+| Dimensao | Resultado principal |
+|---|---|
+| Escala da rede | 626.366 segmentos e 703.109,679 km |
+| Classe funcional dominante | `Minor Arterial` com 32,865% das milhas |
+| Estado com maior extensao | Texas com 54.760,398 km |
+| Participacao do recorte `I/US` salvo no notebook | 15,469% dos trechos e 10,678% das milhas |
+| Participacao do `NHS = 1` | 10,688% da extensao |
+| Participacao total do `NHS > 0` | 37,582% da extensao |
+| Predominio territorial | malha rural responde por 70,642% das milhas |
+| Cobertura STRAHNET | 62.628,113 mi, equivalentes a 14,335% da rede |
+| Consistencia metrica | mediana `KM/MILES = 1,609354` |
+| Qualidade de conversao | `P99` do erro absoluto `KM <-> MILES = 0,001174 km` |
+| Continuidade linear | 59,187% de segmentos orfaos, 10.004 gaps e 405.354 overlaps |
+
+Esse painel resume a leitura gerencial do notebook: a base e metrico-funcionalmente confiavel para diagnostico e priorizacao, mas exige cuidado topologico antes de ser usada em roteamento ou simulacao de rede.
+
+---
+
+## 3. Extensao por Categoria Funcional (`F_SYSTEM`)
+
+| Codigo | Classe | Milhas | % das milhas |
+|---|---|---:|---:|
+| 4 | Minor Arterial | 143.585,040 | 32,865% |
+| 3 | Other Principal Arterial | 139.540,869 | 31,939% |
+| 5 | Major Collector | 66.523,284 | 15,227% |
+| 1 | Interstate | 45.878,900 | 10,501% |
+| 0 | Indefinido | 25.852,455 | 5,917% |
+| 2 | Other Freeways & Expressways | 14.413,731 | 3,299% |
+| 6 | Minor Collector | 762,326 | 0,174% |
+| 7 | Local | 334,889 | 0,077% |
+
+As duas classes arteriais centrais, `Minor Arterial` e `Other Principal Arterial`, concentram juntas 64,804% de toda a extensao em milhas. Isso confirma que a base e fortemente dominada por corredores arteriais, e nao apenas por interestaduais.
+
+As `Interstate`, embora sejam o recorte mais conhecido da rede americana, representam 10,501% da extensao total. Isso reforca a hierarquia funcional observada no notebook: alta relevancia logistica, mas menor cobertura absoluta que as arteriais.
+
+---
+
+## 4. Extensao por Estado
+
+O notebook calcula extensao absoluta por estado, e nao densidade real por area. Ainda assim, os resultados revelam forte concentracao territorial da malha.
+
+| Posicao | Estado | Quilometros | Milhas | Segmentos |
+|---|---|---:|---:|---:|
+| 1 | Texas | 54.760,398 | 34.026,488 | 35.270 |
+| 2 | California | 39.114,527 | 24.304,446 | 63.131 |
+| 3 | New York | 27.502,380 | 17.089,208 | 26.072 |
+| 4 | Georgia | 26.288,268 | 16.334,777 | 16.320 |
+| 5 | Pennsylvania | 22.319,938 | 13.868,941 | 17.838 |
+| 6 | Illinois | 21.700,666 | 13.484,150 | 15.911 |
+| 7 | Minnesota | 21.302,162 | 13.236,558 | 7.665 |
+| 8 | Florida | 21.244,318 | 13.200,553 | 15.433 |
+| 9 | Wisconsin | 19.479,617 | 12.104,066 | 4.411 |
+| 10 | Michigan | 18.404,721 | 11.436,147 | 15.060 |
+
+Destaques adicionais da base:
+
+- Texas lidera com folga em extensao total.
+- California aparece em segundo, mas com volume muito alto de segmentos.
+- New Mexico nao aparece no top 10 em extensao, mas registra o maior numero de segmentos da base: 82.783.
+
+Esse contraste sugere que comprimento total e granularidade de segmentacao nao caminham necessariamente juntos.
+
+---
+
+## 5. Sinalizacao e Corredores Principais (`SIGNT1`, `SIGN1`)
+
+### 5.1 Distribuicao geral por tipo de sinalizacao
+
+| Codigo `SIGNT1` | Tipo | Trechos | Milhas | % trechos | % milhas |
+|---|---|---:|---:|---:|---:|
+| `S` | State Highway | 250.111 | 212.938,115 | 39,930% | 48,739% |
+| `U` | U.S. Highway | 182.889 | 133.002,212 | 29,198% | 30,443% |
+| `I` | Interstate | 96.892 | 46.652,531 | 15,469% | 10,678% |
+| vazio | Sem sinalizacao explicita | 87.797 | 35.962,427 | 14,017% | 8,231% |
+| `C` | County Road | 6.231 | 7.630,405 | 0,995% | 1,747% |
+| `O` | Other | 1.893 | 391,157 | 0,302% | 0,090% |
+
+As rodovias estaduais (`S`) dominam a malha em extensao e em numero de trechos. As `U.S. Highways` (`U`) aparecem como a segunda categoria mais relevante, enquanto as `Interstate` respondem por uma fatia menor em extensao, apesar da importancia estrutural.
+
+### 5.2 Observacao metodologica importante
+
+No notebook, a celula de corredores principais usa o filtro `SIGNT1 in {'I', 'US'}`. Na base, o codigo observado para `U.S. Highway` e `U`, e nao `US`. Por isso, o indicador salvo no notebook para `I/US`:
+
+- 15,469% dos trechos
+- 10,678% das milhas
+
+na pratica coincide com os segmentos `Interstate`, e nao com a soma `Interstate + U.S. Highway`.
+
+### 5.3 Top 15 rotas por extensao no recorte salvo no notebook
+
+| Posicao | Rota | Tipo | Milhas | Trechos |
+|---|---|---|---:|---:|
+| 1 | I80 | Interstate | 2.788,708 | 4.118 |
+| 2 | I90 | Interstate | 2.713,600 | 4.469 |
+| 3 | I40 | Interstate | 2.468,539 | 7.352 |
+| 4 | I10 | Interstate | 2.392,978 | 5.217 |
+| 5 | I70 | Interstate | 2.069,717 | 2.862 |
+| 6 | I95 | Interstate | 1.914,104 | 4.204 |
+| 7 | I75 | Interstate | 1.792,130 | 3.169 |
+| 8 | I20 | Interstate | 1.488,328 | 2.083 |
+| 9 | I15 | Interstate | 1.470,942 | 2.685 |
+| 10 | I35 | Interstate | 1.468,640 | 1.896 |
+| 11 | I94 | Interstate | 1.441,820 | 2.104 |
+| 12 | I5 | Interstate | 1.429,101 | 6.162 |
+| 13 | I25 | Interstate | 1.092,940 | 6.007 |
+| 14 | I55 | Interstate | 957,361 | 1.139 |
+| 15 | I84 | Interstate | 945,926 | 1.441 |
+
+---
+
+## 6. Participacao do National Highway System (`NHS`)
+
+| Codigo NHS | Trechos | Milhas | % das milhas |
+|---|---:|---:|---:|
+| 0 | 344.513 | 272.697,879 | 62,418% |
+| 7 | 147.511 | 98.772,084 | 22,608% |
+| 1 | 96.938 | 46.694,114 | 10,688% |
+| 3 | 24.557 | 14.315,787 | 3,277% |
+| 8 | 8.388 | 2.366,657 | 0,542% |
+| 4 | 3.676 | 1.974,945 | 0,452% |
+| 10 | 666 | 45,023 | 0,010% |
+| 9 | 117 | 25,005 | 0,006% |
+
+Somando todas as categorias com `NHS > 0`, a rede federalizada responde por 164.193,615 milhas, equivalentes a 37,582% da extensao total. O codigo `1` sozinho representa 10,688% da malha.
+
+Esse resultado e importante para planejamento de funding e governanca, porque separa claramente a parcela da rede com maior aderencia a programas e criterios federais.
+
+---
+
+## 7. Contraste Rural x Urbano
+
+O notebook considera `URBAN_CODE == 99999` como rural e os demais registros como urbanos.
+
+| Area | Segmentos | Milhas | % segmentos | % milhas |
+|---|---:|---:|---:|---:|
+| Rural | 277.123 | 308.628,170 | 44,243% | 70,642% |
+| Urbano | 349.243 | 128.263,324 | 55,757% | 29,358% |
+
+O resultado e bastante expressivo: a rede urbana concentra mais segmentos, mas a rede rural concentra muito mais extensao total. Isso sugere segmentacao mais fragmentada em ambiente urbano e trechos mais longos no territorio rural.
+
+### Classes dominantes em cada contexto
+
+| Area | Classe lider | Milhas | % da area |
+|---|---|---:|---:|
+| Rural | Minor Arterial | 123.078,711 | 39,879% |
+| Urbano | Other Principal Arterial | 53.679,632 | 41,851% |
+
+No rural, a combinacao `Minor Arterial + Other Principal Arterial + Major Collector` responde pela maior parte da malha. No urbano, `Other Principal Arterial` assume a lideranca com folga, seguida por categorias mais fragmentadas e por uma presenca relevante de segmentos `Indefinido`.
+
+---
+
+## 8. Cobertura STRAHNET
+
+O recorte `STRAHNET` destaca corredores de relevancia estrategica para mobilidade militar e logistica nacional.
+
+| Posicao | Estado | % da extensao estadual em STRAHNET | Milhas STRAHNET | Milhas totais |
+|---|---|---:|---:|---:|
+| 1 | Alaska | 32,970% | 1.378,718 | 4.181,728 |
+| 2 | Utah | 24,944% | 1.259,788 | 5.050,510 |
+| 3 | Delaware | 21,786% | 154,483 | 709,106 |
+| 4 | Arizona | 19,769% | 1.453,168 | 7.350,714 |
+| 5 | Alabama | 19,542% | 1.884,143 | 9.641,433 |
+| 6 | North Carolina | 18,740% | 2.095,549 | 11.182,471 |
+| 7 | Maryland | 18,727% | 651,628 | 3.479,553 |
+| 8 | California | 18,532% | 4.503,993 | 24.304,446 |
+| 9 | Virginia | 18,332% | 1.652,887 | 9.016,420 |
+| 10 | New Mexico | 18,222% | 1.456,617 | 7.993,712 |
+
+Na escala da base inteira, o STRAHNET soma 62.628,113 milhas, ou 14,335% da rede. Isso mostra que o componente estrategico nao e marginal: ele representa uma parcela substantiva da malha e pode orientar priorizacao de corredores criticos.
+
+---
+
+## 9. Consistencia entre `MILES`, `KM` e `Shape__Length`
+
+### 9.1 Conversao `MILES <-> KM`
+
+| Verificacao | Valor |
+|---|---:|
+| Mediana de `KM / MILES` | 1,609354 |
+| Erro absoluto medio | 0,000453 km |
+| Erro absoluto maximo | 0,001525 km |
+| Percentil 99 do erro absoluto | 0,001174 km |
+
+Os campos `MILES` e `KM` estao altamente coerentes. A diferenca observada e compativel com arredondamento numerico e nao representa problema pratico para analise exploratoria ou indicadores executivos.
+
+### 9.2 Interpretacao de `Shape__Length`
+
+| Medida | Valor |
+|---|---:|
+| Media de `KM / Shape__Length` | 98,550 |
+| Mediana de `KM / Shape__Length` | 97,711 |
+
+Essa razao confirma que `Shape__Length` nao esta em quilometros. A leitura e consistente com geometria em graus decimais, o que exige reprojecao para um CRS metrico antes de qualquer uso espacial quantitativo mais rigoroso.
+
+---
+
+## 10. Continuidade Topologica Aproximada
+
+A analise de continuidade do notebook usa `ROUTE_ID`, `BEGMP` e `ENDMP` para aproximar conexoes lineares por rota, com tolerancia de 0,01 milha entre segmentos consecutivos.
+
+| Indicador | Valor |
+|---|---:|
+| Rotas analisadas | 34.219 |
+| Segmentos analisados | 626.366 |
+| Segmentos orfaos | 370.727 |
+| % de segmentos orfaos | 59,187% |
+| Gaps entre segmentos | 10.004 |
+| Overlaps entre segmentos | 405.354 |
+| Mediana de `delta_next` | -1,118 |
+
+O resultado sinaliza uma rede util para leitura estrutural e agregada, mas ainda com forte ruido topologico para fins de roteamento. O volume de overlaps e particularmente alto, o que sugere segmentacao sobreposta, inconsistencias em mileposts ou coexistencia de geometrias lineares com logicas de cadastro distintas.
+
+---
+
+## 11. Leitura Gerencial
+
+Com base nos resultados do notebook, as principais implicacoes para engenharia e planejamento sao:
+
+- a rede possui escala suficiente para priorizacao nacional, estadual e por corredor
+- a estrutura funcional e liderada por arteriais, e nao apenas por interestaduais
+- a cobertura federal (`NHS`) e estrategica (`STRAHNET`) permite separar carteiras por criticidade e funding
+- a consistencia metrica e alta, o que favorece dashboards, comparacoes e indicadores
+- a continuidade topologica ainda exige saneamento antes de estudos de conectividade operacional
+
+### Agenda sugerida de curto prazo
+
+1. Implantar rotina de QA topologico por estado e por rota.
+2. Estruturar carteira de investimento cruzando `F_SYSTEM`, `NHS`, `STRAHNET` e extensao estadual.
+3. Publicar painel executivo com KPIs padronizados por estado, corredor e risco de continuidade.
+
+---
+
+## 12. Fonte Oficial e Links
+
+- Catalogo Data.gov: https://catalog.data.gov/dataset/national-highway-planning-network1
+- Dicionario de dados (DOI): https://doi.org/10.21949/1529044
+- Notebook da analise: `notebooks/usa-highways/eda-nhpn.ipynb`
+
+---
+
+## Referencias
+
+- Federal Highway Administration (FHWA). *National Highway Planning Network*.
+- Bureau of Transportation Statistics (BTS). *National Transportation Atlas Database (NTAD)*.
+- U.S. Department of Transportation (USDOT). Documentacao oficial do NHPN / NTAD.
+
+---
+
+*Relatorio consolidado a partir das saidas do notebook `eda-nhpn.ipynb` e da base `NTAD_National_Highway_Planning_Network_-129350642200434263.csv`.*
