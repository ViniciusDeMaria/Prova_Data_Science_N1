# -*- coding: utf-8 -*-
"""Prova_Data_Science_N1.ipynb

# Vinicius Henrique Bonazzoli Fogaça de Maria
# Prova Data Science N1

## <font color='red'>Importante: a prova é individual.</font>

**Instruções:**

1. Faça download deste notebook e carregue o mesmo na sua conta do Google Colab.
2. Responda às questões propostas.
3. Crie um repositório para o notebook, "commite" o notebook neste repositório.
4. Na tarefa de avaliação do Teams, envie o link do repositório. Arquivos enviados diretamente no Teams não serão considerados.
5. Commits no repositório após a data de entrega (combinada em sala de aula) serão desconsiderados.

# Objeto da avaliação

Você irá fazer o download do arquivo de dados matches.csv do [repositório do Github](https://raw.githubusercontent.com/mdietterle/repositorio_dados/main/matches.csv)

Todas as questões/atividades serão realizadas com base neste arquivo. É importante que você responda aos questionamentos propostos o mais completo possível, com a maior quantidade de detalhes que você conseguir incluir.

Não se contente com o básico, seja criativo nas respostas, indo além do tradicional.

## **Importante!!**

Antes de começar a responder, abra o arquivo de dados e entenda o dataset. Não será fornecido um dicionário de dados, é sua tarefa analisar o dataset e "inferir" o que são as colunas e a sua organização.

## Instalação de bibliotecas necessárias

Instale neste local todas as bibliotecas necessárias para resolução da avaliação.
"""



# Instalação de bibliotecas básicas
!pip install dash
!pip install dash-ag-grid

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import plotly.express as px
from dash import Dash, html
import dash_ag_grid as dag
import os

"""## Estatísticas básicas do dataset


Carregue o arquivo de dados no notebook e exiba as características básicas do arquivo (shape, tipo de dados, dados ausentes, estatísticas básicas dos dados, etc)
"""

# Responda aqui a primeira etapa

#Carregamento do arquivo em csv
file_path = 'matches.csv'

#leitura do arquivo csv
matches_data = pd.read_csv(file_path)

#Aqui vejo o cabeçario das informações contidas no dataset
matches_data.head()

#Informações do dataset como nome da coluna, valores nulos,
#contidos e tipagem do dado
matches_data.info()

#Verificação dos valores nulos em cada uma das colunas.
matches_data.isnull().sum()

#Tratamento dos dados para que os Nan sejá considerado no dataset
matches_data_clean = matches_data.fillna(0, inplace= False)
matches_data_clean.isnull().sum()

#Verifico a quantidade de times contidos no data set.
matches_data_clean['team'].unique()

#Aqui consigo ver as informações de quantos registros possui o data set para cada um das colunas, media, min, max, etc..
matches_data_clean.describe()

#Aqui consigo ver a quantidade de vezes que o time aparece repetido no dataset.
matches_data_clean['team'].value_counts()



"""## Dia da semana com placares mais altos

Crie um gráfico que responda em qual dia da semana os placares foram mais altos. O conceito de "placar mais alto" é a soma dos gols feitos no jogo.

Como a quantidade de jogos não é a mesma em todos os dias da semana (finais de semana tendem a ter mais jogos que em dias da semana - o que resultaria em placares mais altos nestes dias), você deverá encontrar uma forma de equalizar esta diferença na quantidade de jogos.

A resposta deverá ser um gráfico que demonstre claramente o comparativo dos dias.
"""

# Criando uma nova coluna com a soma dos gols
matches_data_clean['total_de_gols'] = matches_data_clean['gf'] + matches_data_clean['ga']

# Calculando a média de gols por dia da semana - para equalizar gero a media dos gols pelos dias da semana.
media_dos_gols_dia = matches_data_clean.groupby('day')['total_goals'].mean()

# Ordenando os dias da semana para melhor visualização
days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
media_dos_gols_dia = media_dos_gols_dia.reindex(days_order)

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.bar(media_dos_gols_dia.index, media_dos_gols_dia.values)
plt.xlabel('Dia da Semana')
plt.ylabel('Média de Gols')
plt.title('Média de Gols por Dia da Semana')
plt.xticks(rotation=45)
plt.show()

"""## Capitães

Quantos capitães diferentes cada equipe teve durante a temporada?

Responda em forma de um gráfico comparativo, apresentando os dados o mais claramente possível.
"""

# Agrupar por time e contar os capitães únicos
capitaes_por_time = matches_data_clean.groupby('team')['captain'].nunique()

# Criar um gráfico de barras para visualizar os dados
plt.figure(figsize=(15, 6))
plt.bar(capitaes_por_time.index, capitaes_por_time.values)
plt.xlabel('Equipe')
plt.ylabel('Número de Capitães Diferentes')
plt.title('Número de Capitães Diferentes por Equipe')
plt.xticks(rotation=90)
plt.show()

"""## Formação Tática

Qual a formação tática mais comum para cada equipe de acordo com o resultado obtido (Ex: para vitórias, a formação mais comum é X, para empates Y e para Z em derrotas).

**Importante** responda de forma que seja possível fazer comparativos entre equipes.

Responda com um gráfico.
"""

formacao_por_equipe_resultado = matches_data_clean[matches_data_clean['result'] == 'D']
formacao_por_equipe_resultado = formacao_por_equipe_resultado.groupby(['team', 'result', 'formation'])['formation'].count().reset_index(name='count')

# Encontrar a formação mais comum para cada equipe e resultado
formacao_mais_comum = formacao_por_equipe_resultado.loc[formacao_por_equipe_resultado.groupby(['team', 'result'])['count'].idxmax()]

# Criar um gráfico para visualizar a formação mais comum para cada equipe e resultado
fig = px.bar(formacao_mais_comum, x='team', y='count', color='formation',
             title='Formação Tática Mais Comum por Equipe e Resultado',
             labels={'team': 'Equipe', 'count': 'Número de Jogos', 'formation': 'Formação Tática'})

fig.show()

formacao_por_equipe_resultado = matches_data_clean[matches_data_clean['result'] == 'L']
formacao_por_equipe_resultado = formacao_por_equipe_resultado.groupby(['team', 'result', 'formation'])['formation'].count().reset_index(name='count')

# Encontrar a formação mais comum para cada equipe e resultado
formacao_mais_comum = formacao_por_equipe_resultado.loc[formacao_por_equipe_resultado.groupby(['team', 'result'])['count'].idxmax()]

# Criar um gráfico para visualizar a formação mais comum para cada equipe e resultado
fig = px.bar(formacao_mais_comum, x='team', y='count', color='formation',
             title='Formação Tática Mais Comum por Equipe e Resultado',
             labels={'team': 'Equipe', 'count': 'Número de Jogos', 'formation': 'Formação Tática'})

fig.show()


formacao_por_equipe_resultado = matches_data_clean[matches_data_clean['result'] == 'W']
formacao_por_equipe_resultado = formacao_por_equipe_resultado.groupby(['team', 'result', 'formation'])['formation'].count().reset_index(name='count')

# Encontrar a formação mais comum para cada equipe e resultado
formacao_mais_comum = formacao_por_equipe_resultado.loc[formacao_por_equipe_resultado.groupby(['team', 'result'])['count'].idxmax()]

# Criar um gráfico para visualizar a formação mais comum para cada equipe e resultado
fig = px.bar(formacao_mais_comum, x='team', y='count', color='formation',
             title='Formação Tática Mais Comum por Equipe e Resultado',
             labels={'team': 'Equipe', 'count': 'Número de Jogos', 'formation': 'Formação Tática'})

fig.show()

"""## Posse de bola

Qual a média de posse de bola da equipe mandante quando ela perdeu o jogo?

Responda em forma de gráfico para poder comparar entre todas as equipes.
"""

# Responda aqui a etapa

# Filtrar os jogos em que a equipe da casa perdeu
partidas_perdidas = matches_data_clean[matches_data_clean['gf'] < matches_data_clean['ga']]

# Calculo a média da posse de bola para cada equipe que perdeu
media_posse_perdida = partidas_perdidas.groupby('team')['poss'].mean()

# Criação do gráfico
plt.figure(figsize=(15, 6))
media_posse_perdida.plot(kind='bar')
plt.title('Média da posse da bola do time mandante quando perdeu o jogo')
plt.xlabel('Equipes')
plt.ylabel('Média de posse da bola (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""## Classificação

Qual a classificação final do campeonato?

Responda em forma de tabela, ordenada do primeiro colocado ao último.
Você deverá apresentar o brasão do time (pode ser obtido online [aqui](https://logodetimes.com/premier-league/), mas automatize a busca, não salve o logo localmente), o nome, a quantidade de pontos e a posição final no campeonato.

**OBS** Vitória vale 3 pontos, empates 1 ponto e derrota 0 pontos.
"""

# Responda a etapa aqui
pontos_dos_times = {}
for index, linha in matches_data_clean.iterrows():
    time_da_casa = linha['team']
    oponente = linha['opponent']
    gol_da_casa = int(linha['gf'])
    gol_oponente = int(linha['ga'])

    #Aqui definos os pontos por derrota caso ele tenha empatado ou ganho essa pontua e modifica abaixo
    #3 para vitorias e 1 para os empates.
    if time_da_casa not in pontos_dos_times:
        pontos_dos_times[time_da_casa] = 0
    if oponente not in pontos_dos_times:
        pontos_dos_times[oponente] = 0
    #
    if gol_da_casa > gol_oponente:
        pontos_dos_times[time_da_casa] += 3
    #
    elif gol_da_casa < gol_oponente:
        pontos_dos_times[oponente] += 3
    #
    else:
        pontos_dos_times[time_da_casa] += 1
        pontos_dos_times[oponente] += 1

times_organizados = sorted(pontos_dos_times.items(), key=lambda x: x[1], reverse=True)

ranking = []
for i, (time, pontos) in enumerate(times_organizados):
  time_formatado = time.lower().replace(' ', '-')
  logo_url = f"https://logodetimes.com/times/{time_formatado}-football-club/{time_formatado}-football-club-256.png"
  ranking.append({
        'Posição': i + 1,
        'Time': time,
        'Pontos': pontos,
        'Logo': logo_url
    })

ranking_df = pd.DataFrame(ranking)

app = Dash(__name__)
app.layout = html.Div(
    [
        dag.AgGrid(
            id="master-detail-aggregate-example",
            enableEnterpriseModules=False,
            columnDefs=[
                    {'field': 'Posição'  },
                    {'field': 'Time'  },
                    {'field': 'Pontos'  },
                    {'field': 'Logo' }],
            rowData=ranking_df.to_dict('records'),
            columnSize="sizeToFit",
            dashGridOptions={"animateRows": False},
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)

"""## Público

Crie uma visualização que apresente o público total de cada equipe, e também um detalhamento por jogos.

Apresentar os dados usando a técnica "DrillDown" será considerado um "plus". A visualização DrillDown permite que gráficos sejam detalhados com cliques em itens do gráfico.

Um exemplo com tabelas pode ser encontrado [aqui](https://dash.plotly.com/dash-ag-grid/enterprise-master-detail).

Um exemplo usando gráficos pode ser encontrado [aqui](https://community.plotly.com/t/show-and-tell-drill-down-functionality-in-dash-using-callback-context/54403?u=atharvakatre)
"""

# Responda a etapa aqui

from dash import Dash, html, dcc, Input, Output, callback, Patch

# Agrupar os dados por equipe e somar o público total
total_attendance_by_team = matches_data_clean.groupby('team')['attendance'].sum().reset_index()

# Criar o gráfico de barras com o público por jogo para cada equipe
fig_drilldown = px.bar(total_attendance_by_team, x='team', y='attendance'
                       , title='Soma do público total de cada time mandante',
                       hover_data=['attendance'])

fig_drilldown.update_layout(
    clickmode='event+select',
    xaxis_title='Equipe',
    yaxis_title='Público',
)
fig_drilldown.show()

app = Dash(__name__)
app.layout = html.Div(
    [
        html.Div('Quick Filter:'),
        dcc.Input(id="master-detail-aggregate-input", placeholder="filter..."),
        dag.AgGrid(
            id="master-detail-aggregate-simple",
            enableEnterpriseModules=False,
            columnDefs=[
                    {'field': 'team', 'headerName': 'Time da Casa', },
                    {'field': 'gf', 'headerName': 'Gols da Casa' },
                    {'field': 'opponent', 'headerName': 'Openente' },
                    {'field': 'ga', 'headerName': 'Gols openente' },
                    {'field': 'attendance', 'headerName':'Público total' },
                    {'field': 'season', 'headerName':'Temporada' }],
            rowData=matches_data_clean.to_dict('records'),
            columnSize="sizeToFit",
            dashGridOptions={"animateRows": False}
        ),
    ]
)

@callback(
    Output("master-detail-aggregate-simple", "dashGridOptions"),
    Input("master-detail-aggregate-input", "value")
)
def update_filter(filter_value):
    newFilter = Patch()
    newFilter['quickFilterText'] = filter_value
    return newFilter

if __name__ == "__main__":
    app.run(debug=True)
