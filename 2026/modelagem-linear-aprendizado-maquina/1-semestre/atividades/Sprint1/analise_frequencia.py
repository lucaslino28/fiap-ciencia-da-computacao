import pandas as pd

# Leitura da base de dados
df = pd.read_csv("../dados/pesquisa_mobilidade_eletrica.csv")

print("Quantidade de respostas na base:", len(df))
print("\nColunas da base:")
print(df.columns)

# =====================================================
# VARIÁVEL QUANTITATIVA DISCRETA
# =====================================================

coluna_discreta = "Quantas vezes por semana você acredita que precisaria recarregar?"

# Convertendo para número
df[coluna_discreta] = pd.to_numeric(df[coluna_discreta], errors="coerce")

# Removendo respostas inválidas
df_discreta = df.dropna(subset=[coluna_discreta])

# Tabela de frequência
frequencia_discreta = df_discreta[coluna_discreta].value_counts().sort_index()
frequencia_relativa_discreta = round(
    (frequencia_discreta / frequencia_discreta.sum()) * 100, 2
)

tabela_discreta = pd.DataFrame({
    "Frequência Absoluta": frequencia_discreta,
    "Frequência Relativa (%)": frequencia_relativa_discreta
})

print("\n==============================================")
print("TABELA DE FREQUÊNCIA - VARIÁVEL DISCRETA")
print("Variável:", coluna_discreta)
print("==============================================")
print(tabela_discreta)

# Insight 1: A tabela permite identificar quantas vezes por semana os participantes acreditam que precisariam recarregar um veículo elétrico.
# Insight 2: A maior concentração de respostas indica uma possível frequência média de uso da infraestrutura de recarga.

# =====================================================
# VARIÁVEL QUANTITATIVA CONTÍNUA
# =====================================================

coluna_continua = "Quanto tempo você acha aceitável para uma recarga completa? (em minutos)"

# Convertendo para número
df[coluna_continua] = pd.to_numeric(df[coluna_continua], errors="coerce")

# Removendo respostas inválidas
df_continua = df.dropna(subset=[coluna_continua])

# Criando faixas de tempo
classes = [0, 30, 60, 90, 120, 180, 240, 600]
rotulos = [
    "0 a 30 min",
    "31 a 60 min",
    "61 a 90 min",
    "91 a 120 min",
    "121 a 180 min",
    "181 a 240 min",
    "241 a 600 min"
]

df_continua["Faixa de tempo"] = pd.cut(
    df_continua[coluna_continua],
    bins=classes,
    labels=rotulos,
    include_lowest=True
)

# Tabela de frequência
frequencia_continua = df_continua["Faixa de tempo"].value_counts().sort_index()
frequencia_relativa_continua = round(
    (frequencia_continua / frequencia_continua.sum()) * 100, 2
)

tabela_continua = pd.DataFrame({
    "Frequência Absoluta": frequencia_continua,
    "Frequência Relativa (%)": frequencia_relativa_continua
})

print("\n==============================================")
print("TABELA DE FREQUÊNCIA - VARIÁVEL CONTÍNUA")
print("Variável:", coluna_continua)
print("==============================================")
print(tabela_continua)

# Insight 1: A tabela mostra quais faixas de tempo são consideradas mais aceitáveis pelos participantes para uma recarga completa.
# Insight 2: A concentração em faixas menores de tempo pode indicar preferência por soluções de recarga mais rápidas e eficientes.