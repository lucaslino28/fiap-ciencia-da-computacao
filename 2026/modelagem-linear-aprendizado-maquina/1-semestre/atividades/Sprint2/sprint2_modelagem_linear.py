# Sprint 2 - Modelagem Linear para Aprendizado de Máquina
# Tema: Análise Exploratória sobre Mobilidade Elétrica, Energia Solar e Infraestrutura de Recarga
#
# Integrantes:
# Bruno Riquelme Coutinho Pereira - 569619
# Eduardo Bigoli Portela - 569897
# Gabriel Martins Cordeiro Rodrigues - 570497
# Gustavo Fondato de Souza - 573651
# Gustavo Martins Da Silva - 570584
# Lucas Lino Marques da Silva - 572863
#
# Objetivo:
# Realizar análises gráficas e estatísticas utilizando Python, com base nos dados coletados na Sprint 1.

import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Leitura da base de dados
pasta_projeto = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_projeto, "pesquisa_mobilidade_eletrica.csv")

df = pd.read_csv(arquivo)

print("Base carregada com sucesso!")
print(f"Quantidade de linhas: {df.shape[0]}")
print(f"Quantidade de colunas: {df.shape[1]}")
print("\nColunas da base:")
print(df.columns)

# Definição das colunas usadas
col_carro_eletrico = "Você possui ou pretende ter um carro elétrico?"
col_local_recarga = "Onde você mais utilizaria um ponto de recarga?"
col_veiculos_residencia = "Quantos veículos existem na sua residência?"
col_recargas_semana = "Quantas vezes por semana você acredita que precisaria recarregar?"

# Conferência das variáveis categóricas
print("\nDistribuição - Interesse em carro elétrico:")
print(df[col_carro_eletrico].value_counts())

print("\nDistribuição - Local onde mais utilizaria ponto de recarga:")
print(df[col_local_recarga].value_counts())

# Função para tratar respostas numéricas
def extrair_numero(valor):
    """
    Esta função recebe uma resposta da base e tenta transformar em número.
    Exemplos:
    "60 minutos" -> 60
    "90min" -> 90
    "1 vez" -> 1
    "5 x" -> 5
    "2 a 3" -> 2.5
    """
    valor_texto = str(valor).replace(",", ".").lower()

    numeros = re.findall(r"\d+\.?\d*", valor_texto)

    if len(numeros) == 0:
        return None

    numeros = [float(numero) for numero in numeros]

    if len(numeros) >= 2:
        return sum(numeros) / len(numeros)

    return numeros[0]

# Criação das colunas numéricas tratadas
df["veiculos_residencia"] = df[col_veiculos_residencia].apply(extrair_numero)
df["recargas_semana"] = df[col_recargas_semana].apply(extrair_numero)

print("\nResumo da coluna veiculos_residencia:")
print(df["veiculos_residencia"].describe())

print("\nResumo da coluna recargas_semana:")
print(df["recargas_semana"].describe())

# Criação da pasta de gráficos
pasta_graficos = os.path.join(pasta_projeto, "graficos")

if not os.path.exists(pasta_graficos):
    os.makedirs(pasta_graficos)

print("\nPasta de gráficos pronta!")

# Gráfico de setores
dados_carro_eletrico = df[col_carro_eletrico].value_counts()

cores_setores = ["#4CAF50", "#2196F3", "#FFC107", "#F44336"]

plt.figure(figsize=(9, 6))

plt.pie(
    dados_carro_eletrico,
    autopct="%1.1f%%",
    colors=cores_setores,
    startangle=90
)

plt.title("Distribuição sobre possuir ou pretender ter carro elétrico")

plt.legend(
    dados_carro_eletrico.index,
    title="Respostas",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "grafico_setores_carro_eletrico.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico de Barras
dados_local_recarga = df[col_local_recarga].value_counts()

plt.figure(figsize=(10, 6))

plt.bar(
    dados_local_recarga.index,
    dados_local_recarga.values,
    color="#2196F3",
    label="Quantidade de respostas"
)

plt.title("Locais onde os respondentes mais utilizariam ponto de recarga")
plt.xlabel("Local de utilização")
plt.ylabel("Quantidade de respostas")
plt.xticks(rotation=30, ha="right")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "grafico_barras_ponto_recarga.png"), dpi=300)
plt.show()
plt.close()

# Histograma
veiculos_residencia_limpo = df["veiculos_residencia"].dropna()
maior_quantidade_veiculos = int(veiculos_residencia_limpo.max())
bins_veiculos = [numero - 0.5 for numero in range(0, maior_quantidade_veiculos + 2)]

plt.figure(figsize=(10, 6))

plt.hist(
    veiculos_residencia_limpo,
    bins=bins_veiculos,
    color="#4CAF50",
    edgecolor="black"
)

plt.title("Distribuição da quantidade de veículos por residência")
plt.xlabel("Quantidade de veículos na residência")
plt.ylabel("Quantidade de respostas")
plt.xticks(range(0, maior_quantidade_veiculos + 1))

plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "histograma_veiculos_residencia.png"), dpi=300)
plt.show()
plt.close()

# Boxplot
recargas_semana_limpo = df["recargas_semana"].dropna()

plt.figure(figsize=(8, 6))

plt.boxplot(
    recargas_semana_limpo,
    patch_artist=True,
    boxprops=dict(facecolor="#FFC107", color="black"),
    medianprops=dict(color="black"),
    whiskerprops=dict(color="black"),
    capprops=dict(color="black"),
    flierprops=dict(markerfacecolor="#F44336", marker="o", markersize=6)
)

plt.title("Boxplot da quantidade de recargas semanais")
plt.xlabel("Frequência de recarga")
plt.ylabel("Quantidade de recargas por semana")
plt.xticks([1], ["Recargas semanais"])

plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "boxplot_recargas_semanais.png"), dpi=300)
plt.show()
plt.close()

print("\nGráficos gerados e salvos com sucesso na pasta 'graficos'!")

# Função para estatística descritiva
def estatistica_descritiva(serie, nome_variavel):
    """
    Esta função calcula as principais medidas de estatística descritiva
    para uma variável numérica.
    """
    serie_limpa = serie.dropna()

    media = serie_limpa.mean()
    mediana = serie_limpa.median()
    moda = serie_limpa.mode()

    minimo = serie_limpa.min()
    maximo = serie_limpa.max()
    amplitude = maximo - minimo
    variancia = serie_limpa.var()
    desvio_padrao = serie_limpa.std()

    q1 = serie_limpa.quantile(0.25)
    q2 = serie_limpa.quantile(0.50)
    q3 = serie_limpa.quantile(0.75)
    p10 = serie_limpa.quantile(0.10)
    p90 = serie_limpa.quantile(0.90)

    if len(moda) > 0:
        moda_valor = moda.iloc[0]
    else:
        moda_valor = "Não possui moda"

    resultados = {
        "Variável": nome_variavel,
        "Média": media,
        "Mediana": mediana,
        "Moda": moda_valor,
        "Mínimo": minimo,
        "Máximo": maximo,
        "Amplitude": amplitude,
        "Variância": variancia,
        "Desvio padrão": desvio_padrao,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "P10": p10,
        "P90": p90
    }

    return resultados

# Análises univariadas
analise_veiculos_residencia = estatistica_descritiva(
    df["veiculos_residencia"],
    "Quantidade de veículos na residência"
)

analise_recargas_semana = estatistica_descritiva(
    df["recargas_semana"],
    "Quantidade de recargas por semana"
)

tabela_estatistica = pd.DataFrame([
    analise_veiculos_residencia,
    analise_recargas_semana
])

print("\nEstatística Descritiva - Análises Univariadas:")
print(tabela_estatistica)

# Exportação dos resultados estatísticos
tabela_estatistica.to_csv(
    os.path.join(pasta_projeto, "estatistica_descritiva_sprint2.csv"),
    index=False,
    encoding="utf-8-sig"
)

print("\nTabela de estatística descritiva salva como 'estatistica_descritiva_sprint2.csv'.")

# Exibição organizada dos resultados
def formatar_valor(valor):
    try:
        return f"{valor:.2f}"
    except (ValueError, TypeError):
        return str(valor)

def exibir_analise(analise):
    print("\n" + "=" * 60)
    print(f"ANÁLISE UNIVARIADA: {analise['Variável']}")
    print("=" * 60)

    print("\nMedidas de Tendência Central:")
    print(f"Média: {analise['Média']:.2f}")
    print(f"Mediana: {analise['Mediana']:.2f}")
    print(f"Moda: {formatar_valor(analise['Moda'])}")

    print("\nMedidas de Dispersão:")
    print(f"Mínimo: {analise['Mínimo']:.2f}")
    print(f"Máximo: {analise['Máximo']:.2f}")
    print(f"Amplitude: {analise['Amplitude']:.2f}")
    print(f"Variância: {analise['Variância']:.2f}")
    print(f"Desvio padrão: {analise['Desvio padrão']:.2f}")

    print("\nMedidas Separatrizes:")
    print(f"Q1: {analise['Q1']:.2f}")
    print(f"Q2: {analise['Q2']:.2f}")
    print(f"Q3: {analise['Q3']:.2f}")
    print(f"P10: {analise['P10']:.2f}")
    print(f"P90: {analise['P90']:.2f}")

exibir_analise(analise_veiculos_residencia)
exibir_analise(analise_recargas_semana)

print("\nProcessamento finalizado com sucesso!")
