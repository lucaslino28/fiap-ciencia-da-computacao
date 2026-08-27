"""
Global Solution - Modelagem Linear para Aprendizado de Máquina
Tema: Análise estatística de missões espaciais para apoio ao monitoramento operacional inteligente
Base de dados: All Space Missions from 1957 - Kaggle

Integrantes:
Bruno Riquelme Coutinho Pereira - RM: 569619
Eduardo Bigoli Portela - RM: 569897
Lucas Lino Marques da Silva - RM: 572863
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# CRIAÇÃO DAS PASTAS DE SAÍDA
os.makedirs("graficos", exist_ok=True)
os.makedirs("saidas", exist_ok=True)

# LEITURA DA BASE DE DADOS
arquivo = "dados/space_missions.csv"

df = pd.read_csv(arquivo)

# Remove espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Remove colunas de índice que não serão utilizadas na análise
df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], errors="ignore")

print("\nBase carregada com sucesso!")
print("\nPrimeiras linhas da base:")
print(df.head())

print("\nInformações da base:")
print(df.info())

print("\nColunas da base:")
print(df.columns)

# PADRONIZAÇÃO E TRATAMENTO DOS DADOS
df = df.rename(columns={"Rocket": "Custo_Missao_Milhoes_USD"})

df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce", utc=True)

df["Ano"] = df["Datum"].dt.year

df["Custo_Missao_Milhoes_USD"] = (
    df["Custo_Missao_Milhoes_USD"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Custo_Missao_Milhoes_USD"] = pd.to_numeric(
    df["Custo_Missao_Milhoes_USD"],
    errors="coerce"
)

# Removendo registros sem ano
df = df.dropna(subset=["Ano"])

# Convertendo o ano para inteiro
df["Ano"] = df["Ano"].astype(int)

# Criando uma base apenas com registros que possuem custo informado
df_custos = df.dropna(subset=["Custo_Missao_Milhoes_USD"]).copy()
print("\nQuantidade total de registros na base:", len(df))
print("Quantidade de registros com custo informado:", len(df_custos))

# TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIA - VARIÁVEL DISCRETA
# Variável: Quantidade de missões por ano
missoes_por_ano = df["Ano"].value_counts().sort_index()

freq_qtd_missoes = missoes_por_ano.value_counts().sort_index()

tabela_discreta = pd.DataFrame({
    "Quantidade_Missoes": freq_qtd_missoes.index,
    "Frequencia_Absoluta": freq_qtd_missoes.values
})

tabela_discreta["Frequencia_Relativa"] = (
    tabela_discreta["Frequencia_Absoluta"] /
    tabela_discreta["Frequencia_Absoluta"].sum()
)

tabela_discreta["Frequencia_Percentual"] = (
    tabela_discreta["Frequencia_Relativa"] * 100
)

tabela_discreta["Frequencia_Acumulada"] = (
    tabela_discreta["Frequencia_Absoluta"].cumsum()
)

tabela_discreta["Frequencia_Relativa_Acumulada"] = (
    tabela_discreta["Frequencia_Relativa"].cumsum()
)

tabela_discreta["Frequencia_Percentual_Acumulada"] = (
    tabela_discreta["Frequencia_Percentual"].cumsum()
)

tabela_discreta["Frequencia_Relativa"] = tabela_discreta["Frequencia_Relativa"].round(4)
tabela_discreta["Frequencia_Percentual"] = tabela_discreta["Frequencia_Percentual"].round(2)
tabela_discreta["Frequencia_Relativa_Acumulada"] = tabela_discreta["Frequencia_Relativa_Acumulada"].round(4)
tabela_discreta["Frequencia_Percentual_Acumulada"] = tabela_discreta["Frequencia_Percentual_Acumulada"].round(2)

print("\nTabela de frequência - variável discreta:")
print(tabela_discreta)

tabela_discreta.to_csv(
    "saidas/tabela_frequencia_discreta_missoes_por_ano.csv",
    index=False,
    encoding="utf-8-sig"
)

# TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIA - VARIÁVEL CONTÍNUA
# Variável: Custo da missão em milhões de dólares
df_custos["Faixa_Custo"] = pd.cut(
    df_custos["Custo_Missao_Milhoes_USD"],
    bins=5
)

freq_continua = df_custos["Faixa_Custo"].value_counts().sort_index()

tabela_continua = pd.DataFrame({
    "Faixa_Custo": freq_continua.index.astype(str),
    "Frequencia_Absoluta": freq_continua.values
})

tabela_continua["Frequencia_Relativa"] = (
    tabela_continua["Frequencia_Absoluta"] /
    tabela_continua["Frequencia_Absoluta"].sum()
)

tabela_continua["Frequencia_Percentual"] = (
    tabela_continua["Frequencia_Relativa"] * 100
)

tabela_continua["Frequencia_Acumulada"] = (
    tabela_continua["Frequencia_Absoluta"].cumsum()
)

tabela_continua["Frequencia_Relativa_Acumulada"] = (
    tabela_continua["Frequencia_Relativa"].cumsum()
)

tabela_continua["Frequencia_Percentual_Acumulada"] = (
    tabela_continua["Frequencia_Percentual"].cumsum()
)

tabela_continua["Frequencia_Relativa"] = tabela_continua["Frequencia_Relativa"].round(4)
tabela_continua["Frequencia_Percentual"] = tabela_continua["Frequencia_Percentual"].round(2)
tabela_continua["Frequencia_Relativa_Acumulada"] = tabela_continua["Frequencia_Relativa_Acumulada"].round(4)
tabela_continua["Frequencia_Percentual_Acumulada"] = tabela_continua["Frequencia_Percentual_Acumulada"].round(2)

print("\nTabela de frequência - variável contínua:")
print(tabela_continua)

tabela_continua.to_csv(
    "saidas/tabela_frequencia_continua_custos.csv",
    index=False,
    encoding="utf-8-sig"
)

# GRÁFICO 1 - QUANTIDADE DE MISSÕES POR ANO
plt.figure(figsize=(12, 5))
missoes_por_ano.plot(kind="bar", color="steelblue")
plt.title("Quantidade de Missões Espaciais por Ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade de Missões")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("graficos/grafico_missoes_por_ano.png")
plt.show()

# GRÁFICO 2 - HISTOGRAMA DOS CUSTOS DAS MISSÕES
plt.figure(figsize=(9, 5))
plt.hist(
    df_custos["Custo_Missao_Milhoes_USD"],
    bins=10,
    color="orange",
    edgecolor="black"
)
plt.title("Distribuição dos Custos das Missões")
plt.xlabel("Custo da Missão em Milhões de Dólares")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig("graficos/histograma_custos_missoes.png")
plt.show()

# ANÁLISE UNIVARIADA 1 - CUSTO DAS MISSÕES
custos = df_custos["Custo_Missao_Milhoes_USD"]

analise_custos = {
    "Media": custos.mean(),
    "Mediana": custos.median(),
    "Moda": ", ".join(map(str, custos.mode().round(2).tolist())),
    "Maximo": custos.max(),
    "Minimo": custos.min(),
    "Amplitude": custos.max() - custos.min(),
    "Variancia": custos.var(),
    "Desvio_Padrao": custos.std(),
    "Coeficiente_de_Variacao": (custos.std() / custos.mean()) * 100,
    "Primeiro_Quartil": custos.quantile(0.25),
    "Segundo_Quartil": custos.quantile(0.50),
    "Terceiro_Quartil": custos.quantile(0.75)
}

tabela_analise_custos = pd.DataFrame(
    list(analise_custos.items()),
    columns=["Medida", "Valor"]
)

tabela_analise_custos["Valor"] = tabela_analise_custos["Valor"].apply(
    lambda valor: round(valor, 2) if pd.api.types.is_number(valor) else valor
)

print("\nAnálise univariada - custos das missões:")
print(tabela_analise_custos)

tabela_analise_custos.to_csv(
    "saidas/analise_univariada_custos_missoes.csv",
    index=False,
    encoding="utf-8-sig"
)

# ANÁLISE UNIVARIADA 2 - QUANTIDADE DE MISSÕES POR ANO
qtd_missoes_ano = missoes_por_ano

analise_missoes_ano = {
    "Media": qtd_missoes_ano.mean(),
    "Mediana": qtd_missoes_ano.median(),
    "Moda": ", ".join(map(str, qtd_missoes_ano.mode().tolist())),
    "Maximo": qtd_missoes_ano.max(),
    "Minimo": qtd_missoes_ano.min(),
    "Amplitude": qtd_missoes_ano.max() - qtd_missoes_ano.min(),
    "Variancia": qtd_missoes_ano.var(),
    "Desvio_Padrao": qtd_missoes_ano.std(),
    "Coeficiente_de_Variacao": (qtd_missoes_ano.std() / qtd_missoes_ano.mean()) * 100,
    "Primeiro_Quartil": qtd_missoes_ano.quantile(0.25),
    "Segundo_Quartil": qtd_missoes_ano.quantile(0.50),
    "Terceiro_Quartil": qtd_missoes_ano.quantile(0.75)
}

tabela_analise_missoes_ano = pd.DataFrame(
    list(analise_missoes_ano.items()),
    columns=["Medida", "Valor"]
)

tabela_analise_missoes_ano["Valor"] = tabela_analise_missoes_ano["Valor"].apply(
    lambda valor: round(valor, 2) if pd.api.types.is_number(valor) else valor
)

print("\nAnálise univariada - quantidade de missões por ano:")
print(tabela_analise_missoes_ano)

tabela_analise_missoes_ano.to_csv(
    "saidas/analise_univariada_missoes_por_ano.csv",
    index=False,
    encoding="utf-8-sig"
)

# RESUMO FINAL
print("\nProcessamento finalizado com sucesso!")
print("\nArquivos gerados:")
print("- saidas/tabela_frequencia_discreta_missoes_por_ano.csv")
print("- saidas/tabela_frequencia_continua_custos.csv")
print("- saidas/analise_univariada_custos_missoes.csv")
print("- saidas/analise_univariada_missoes_por_ano.csv")
print("- graficos/grafico_missoes_por_ano.png")
print("- graficos/histograma_custos_missoes.png")