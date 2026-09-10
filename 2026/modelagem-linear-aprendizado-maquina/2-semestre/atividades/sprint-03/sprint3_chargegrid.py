# FIAP - Ciência da Computação
# Modelagem Linear para Aprendizado de Máquina
# Challenge Sprint 3 - ChargeGrid Intelligence
#
# Professor: Rodolfo Magliari de Paiva
#
# Integrantes:
# Bruno Riquelme Coutinho Pereira - 569619
# Eduardo Bigoli Portela - 569897
# Gabriel Martins Cordeiro Rodrigues - 570497
# Gustavo Fondato de Souza - 573651
# Gustavo Martins Da Silva - 570584
# Lucas Lino Marques da Silva - 572863

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Carregamento da base
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_CSV = PASTA_PROJETO / "dados" / "chargegrid_sessoes.csv"

dados = pd.read_csv(CAMINHO_CSV)

print("=" * 60)
print("SPRINT 3 - CHARGEGRID INTELLIGENCE")
print("=" * 60)

print("\nPrimeiros registros:")
print(dados.head())

print(f"\nQuantidade de sessões: {len(dados)}")

print("\nResumo estatístico:")
print(dados.describe())


# Variável principal das análises
energia = dados["energia_consumida_kwh"]


def classificar_evento(probabilidade):
    if probabilidade < 0.05:
        return "Raro"
    elif probabilidade < 0.50:
        return "Pouco provável"
    elif probabilidade < 0.90:
        return "Provável"
    else:
        return "Quase certo"


criterio_classificacao = (
    "Critério usado: raro < 5%, pouco provável < 50%, "
    "provável < 90% e quase certo >= 90%."
)

# ANÁLISE INICIAL DA BASE
print("\n" + "=" * 60)
print("ANÁLISE INICIAL DA BASE")
print("=" * 60)

print(f"\nDuração mínima: {dados['duracao_min'].min()} minutos")
print(f"Duração máxima: {dados['duracao_min'].max()} minutos")

print(
    f"Consumo mínimo: "
    f"{dados['energia_consumida_kwh'].min():.2f} kWh"
)

print(
    f"Consumo máximo: "
    f"{dados['energia_consumida_kwh'].max():.2f} kWh"
)

print(
    f"Potência média geral: "
    f"{dados['potencia_media_kw'].mean():.2f} kW"
)

# QUESTÃO 01 - PROBABILIDADE ACIMA DA MEDIANA
print("\n" + "=" * 60)
print("QUESTÃO 01 - PROBABILIDADE ACIMA DA MEDIANA")
print("=" * 60)

mediana = energia.median()
media = energia.mean()
desvio_padrao = energia.std()

probabilidade_acima_mediana = 1 - norm.cdf(
    mediana,
    loc=media,
    scale=desvio_padrao
)

probabilidade_acima_mediana_pct = (
    probabilidade_acima_mediana * 100
)

print(f"\nMediana: {mediana:.3f} kWh")
print(f"Média: {media:.3f} kWh")
print(f"Desvio padrão: {desvio_padrao:.3f} kWh")

print(
    f"Probabilidade de consumo acima da mediana: "
    f"{probabilidade_acima_mediana_pct:.2f}%"
)

print(
    f"Classificação do evento: "
    f"{classificar_evento(probabilidade_acima_mediana)}"
)
print(criterio_classificacao)

print(
    "\nInterpretação: considerando uma distribuição normal ajustada "
    "pela média e pelo desvio padrão da base, "
    f"a probabilidade estimada de uma sessão apresentar "
    f"consumo superior à mediana amostral ({mediana:.3f} kWh) "
    f"é de {probabilidade_acima_mediana_pct:.2f}%. "
    f"Em uma normal teórica perfeita, média e mediana seriam iguais; "
    f"a diferença aparece porque a mediana usada veio da amostra."
)

# GRÁFICO 1 - HISTOGRAMA DO CONSUMO
plt.figure(figsize=(10, 6))

plt.hist(
    energia,
    bins=12,
    edgecolor="black",
    alpha=0.7
)

plt.axvline(
    media,
    linestyle="--",
    linewidth=2,
    label=f"Média = {media:.2f} kWh"
)

plt.axvline(
    mediana,
    linestyle=":",
    linewidth=2,
    label=f"Mediana = {mediana:.2f} kWh"
)

plt.title("Distribuição do Consumo de Energia")
plt.xlabel("Energia consumida (kWh)")
plt.ylabel("Frequência")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(PASTA_PROJETO / "grafico_01_histograma_consumo.png", dpi=300)
plt.show()

# GRÁFICO 2 - PROBABILIDADE ACIMA DA MEDIANA
x = np.linspace(
    max(0, media - 4 * desvio_padrao),
    media + 4 * desvio_padrao,
    500
)

y_normal = norm.pdf(
    x,
    loc=media,
    scale=desvio_padrao
)

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    y_normal,
    label="Distribuição normal"
)

plt.fill_between(
    x,
    y_normal,
    where=(x >= mediana),
    alpha=0.4,
    label="Área acima da mediana"
)

plt.axvline(
    mediana,
    linestyle="--",
    linewidth=2,
    label=f"Mediana = {mediana:.2f} kWh"
)

plt.title("Probabilidade de Consumo Acima da Mediana")
plt.xlabel("Energia consumida (kWh)")
plt.ylabel("Densidade de probabilidade")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    PASTA_PROJETO / "grafico_02_probabilidade_acima_mediana.png",
    dpi=300
)

plt.show()

# QUESTÃO 02 - PROBABILIDADE NO INTERVALO MÉDIA ± 2s
print("\n" + "=" * 60)
print("QUESTÃO 02 - PROBABILIDADE NO INTERVALO MÉDIA ± 2s")
print("=" * 60)

limite_inferior = media - 2 * desvio_padrao
limite_superior = media + 2 * desvio_padrao

probabilidade_intervalo = (
    norm.cdf(
        limite_superior,
        loc=media,
        scale=desvio_padrao
    )
    -
    norm.cdf(
        limite_inferior,
        loc=media,
        scale=desvio_padrao
    )
)

probabilidade_intervalo_pct = (
    probabilidade_intervalo * 100
)

print(f"\nMédia: {media:.3f} kWh")
print(f"Desvio padrão: {desvio_padrao:.3f} kWh")
print(f"Limite inferior: {limite_inferior:.3f} kWh")
print(f"Limite superior: {limite_superior:.3f} kWh")

print(
    f"Probabilidade dentro do intervalo: "
    f"{probabilidade_intervalo_pct:.2f}%"
)

print(
    f"Classificação do evento: "
    f"{classificar_evento(probabilidade_intervalo)}"
)
print(criterio_classificacao)

print(
    "\nInterpretação: considerando uma distribuição normal, "
    f"aproximadamente {probabilidade_intervalo_pct:.2f}% "
    f"das sessões apresentam consumo entre "
    f"{limite_inferior:.3f} kWh e "
    f"{limite_superior:.3f} kWh."
)

# GRÁFICO 3 - INTERVALO MÉDIA ± 2s
plt.figure(figsize=(10, 6))

plt.plot(
    x,
    y_normal,
    label="Distribuição normal"
)

plt.fill_between(
    x,
    y_normal,
    where=(
        (x >= limite_inferior)
        &
        (x <= limite_superior)
    ),
    alpha=0.4,
    label="Intervalo média ± 2s"
)

plt.axvline(
    media,
    linestyle="--",
    linewidth=2,
    label=f"Média = {media:.2f} kWh"
)

plt.axvline(
    limite_inferior,
    linestyle="--",
    label=f"Limite inferior = {limite_inferior:.2f}"
)

plt.axvline(
    limite_superior,
    linestyle="--",
    label=f"Limite superior = {limite_superior:.2f}"
)

plt.title("Probabilidade no Intervalo Média ± 2 Desvios Padrão")
plt.xlabel("Energia consumida (kWh)")
plt.ylabel("Densidade de probabilidade")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    PASTA_PROJETO / "grafico_03_intervalo_media_2s.png",
    dpi=300
)

plt.show()

# QUESTÃO 03 - REGRESSÃO LINEAR
print("\n" + "=" * 60)
print("QUESTÃO 03 - REGRESSÃO LINEAR")
print("=" * 60)

# X = duração da sessão
# y = energia consumida
X = dados[["duracao_min"]]
y = dados["energia_consumida_kwh"]

modelo = LinearRegression()
modelo.fit(X, y)

previsoes = modelo.predict(X)

intercepto = modelo.intercept_
coeficiente = modelo.coef_[0]
r2 = r2_score(y, previsoes)

correlacao = dados[
    "duracao_min"
].corr(
    dados["energia_consumida_kwh"]
)

print(f"\nIntercepto: {intercepto:.4f}")
print(f"Coeficiente da duração: {coeficiente:.4f}")

print(
    f"\nEquação da reta:\n"
    f"energia_consumida = "
    f"{intercepto:.4f} + "
    f"{coeficiente:.4f} × duracao_min"
)

print(f"\nR²: {r2:.4f}")
print(f"Correlação: {correlacao:.4f}")

print(
    f"\nInterpretação do coeficiente: "
    f"a cada minuto adicional de recarga, "
    f"o modelo estima um aumento médio de "
    f"{coeficiente:.4f} kWh no consumo de energia."
)

print(
    f"\nO intercepto de {intercepto:.4f} kWh "
    f"representa o valor estimado pelo modelo "
    f"quando a duração é zero. "
    f"Nesse contexto, ele funciona principalmente "
    f"como parâmetro matemático da reta."
)

print(
    f"\nO R² de {r2:.4f} indica que aproximadamente "
    f"{r2 * 100:.2f}% da variação do consumo "
    f"de energia é explicada pela duração da sessão "
    f"nos dados analisados."
)

print(
    f"\nA correlação de {correlacao:.4f} indica "
    f"uma relação positiva forte entre "
    f"a duração da sessão e o consumo de energia."
)

# PREVISÃO PRÁTICA
duracao_exemplo = pd.DataFrame(
    {"duracao_min": [90]}
)

consumo_estimado = modelo.predict(
    duracao_exemplo
)[0]

print(
    f"\nExemplo de previsão:"
)

print(
    f"Para uma sessão com duração de 90 minutos, "
    f"o modelo estima um consumo de aproximadamente "
    f"{consumo_estimado:.2f} kWh. "
    f"Como 90 minutos está dentro do intervalo observado na base, "
    f"essa previsão é uma interpolação."
)

# GRÁFICO 4 - REGRESSÃO LINEAR
dados_ordenados = dados.sort_values(
    "duracao_min"
)

X_ordenado = dados_ordenados[
    ["duracao_min"]
]

previsoes_ordenadas = modelo.predict(
    X_ordenado
)

plt.figure(figsize=(10, 6))

plt.scatter(
    dados["duracao_min"],
    dados["energia_consumida_kwh"],
    label="Sessões de recarga"
)

plt.plot(
    dados_ordenados["duracao_min"],
    previsoes_ordenadas,
    linewidth=2,
    label="Reta de regressão linear"
)

plt.title(
    "Regressão Linear - Duração da Sessão x Energia Consumida"
)

plt.xlabel(
    "Duração da sessão (minutos)"
)

plt.ylabel(
    "Energia consumida (kWh)"
)

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    PASTA_PROJETO / "grafico_04_regressao_linear.png",
    dpi=300
)

plt.show()

# QUESTÃO 04 - INTERPRETAÇÃO GERAL
print("\n" + "=" * 60)
print("QUESTÃO 04 - INTERPRETAÇÃO GERAL")
print("=" * 60)

print(
    "\nAs análises estatísticas permitiram identificar "
    "características importantes do consumo de energia "
    "das sessões de recarga do ChargeGrid Intelligence."
)

print(
    "\nA análise probabilística mostrou como o consumo "
    "se distribui em relação à mediana, à média "
    "e ao desvio padrão."
)

print(
    "\nA regressão linear mostrou uma relação positiva "
    "entre a duração da sessão e a energia consumida."
)

print(
    "\nCom base em dados históricos, o modelo pode ser "
    "utilizado para realizar estimativas de consumo "
    "e apoiar decisões relacionadas ao planejamento "
    "da demanda energética."
)

print(
    "\nEsse tipo de análise pode contribuir para "
    "o gerenciamento da infraestrutura de recarga, "
    "controle de demanda e futuras políticas "
    "de tarifação do ChargeGrid Intelligence."
)

print("\nAnálise finalizada.")
