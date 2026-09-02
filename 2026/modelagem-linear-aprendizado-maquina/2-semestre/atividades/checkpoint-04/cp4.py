import random
import matplotlib.pyplot as plt

# Checkpoint 4 - Modelagem Linear para Aprendizado de Máquina
# Curso: Ciência da Computação - 1º ano - FIAP
# Tema: Análise probabilística de prazos e atrasos de entregas na cidade de São Paulo
#
# Integrantes:
# Bruno Riquelme Coutinho Pereira - RM569619
# Eduardo Bigoli Portela - RM569897
# Gabriel Martins Cordeiro Rodrigues - RM570497
# Gustavo Fondato de Souza - RM573651
# Gustavo Martins Da Silva - RM570584
# Lucas Lino Marques da Silva - RM572863

random.seed(42)

regioes = [
    "Centro",
    "Zona Norte",
    "Zona Sul",
    "Zona Leste",
    "Zona Oeste"
]

# Geração das entregas simuladas
entregas = []
for i in range(1, 101):
    regiao = random.choice(regioes)
    prazo_previsto = random.randint(2, 5)

    # Tempo real gerado com distribuição normal
    # A média fica 0,2 dia abaixo do prazo previsto.
    # O desvio padrão 0,8 representa a variação natural das entregas.
    tempo_real = round(
        random.gauss(prazo_previsto - 0.2, 0.8),
        2
    )

    if tempo_real <= 0:
        tempo_real = 0.5

    entrega = {
        "id": i,
        "regiao": regiao,
        "prazo_previsto": prazo_previsto,
        "tempo_real": tempo_real
    }

    entregas.append(entrega)

# Classificação das entregas
for entrega in entregas:
    diferenca = entrega["tempo_real"] - entrega["prazo_previsto"]

    if diferenca > 0:
        atraso = round(diferenca, 2)
        antecipacao = 0
        status = "Atrasada"

    else:
        atraso = 0
        antecipacao = round(abs(diferenca), 2)
        status = "No prazo"

    entrega["atraso"] = atraso
    entrega["antecipacao"] = antecipacao
    entrega["status"] = status

# Exibição das primeiras entregas
print("\n--- Primeiras Entregas Simuladas ---")
for entrega in entregas[:5]:
    print("\nEntrega:", entrega["id"])
    print("Região:", entrega["regiao"])
    print("Prazo previsto:", entrega["prazo_previsto"], "dias")
    print("Tempo real:", entrega["tempo_real"], "dias")
    print("Atraso:", entrega["atraso"], "dias")
    print("Antecipação:", entrega["antecipacao"], "dias")
    print("Status:", entrega["status"])

# Análise de probabilidade
total_entregas = len(entregas)

entregas_atrasadas = 0
entregas_no_prazo = 0

for entrega in entregas:
    if entrega["status"] == "Atrasada":
        entregas_atrasadas += 1
    else:
        entregas_no_prazo += 1


probabilidade_atraso = (
    entregas_atrasadas / total_entregas
) * 100

probabilidade_no_prazo = (
    entregas_no_prazo / total_entregas
) * 100


print("\n--- Análise de Probabilidade ---")
print("Total de entregas:", total_entregas)
print("Entregas atrasadas:", entregas_atrasadas)
print("Entregas no prazo:", entregas_no_prazo)
print(
    "Probabilidade de atraso:",
    round(probabilidade_atraso, 2),
    "%"
)
print(
    "Probabilidade de entrega no prazo:",
    round(probabilidade_no_prazo, 2),
    "%"
)

# Média dos tempos reais
soma_tempo_real = 0
for entrega in entregas:
    soma_tempo_real += entrega["tempo_real"]

media_tempo_real = soma_tempo_real / total_entregas

# Média dos atrasos considerando apenas as entregas atrasadas
soma_atrasos = 0
for entrega in entregas:
    soma_atrasos += entrega["atraso"]
if entregas_atrasadas > 0:
    media_atraso = soma_atrasos / entregas_atrasadas
else:
    media_atraso = 0

# Variância e desvio padrão dos tempos reais
soma_quadrados = 0
for entrega in entregas:
    diferenca_media = (
        entrega["tempo_real"] - media_tempo_real
    )

    soma_quadrados += diferenca_media ** 2

variancia = soma_quadrados / total_entregas
desvio_padrao = variancia ** 0.5

print("\n--- Estatísticas dos Tempos ---")
print(
    "Média do tempo real:",
    round(media_tempo_real, 2),
    "dias"
)
print(
    "Média de atraso:",
    round(media_atraso, 2),
    "dias"
)
print(
    "Variância:",
    round(variancia, 2)
)
print(
    "Desvio padrão:",
    round(desvio_padrao, 2),
    "dias"
)

# Análise por região
print("\n--- Análise por Região ---")
print(
    "Observação: as regiões foram sorteadas aleatoriamente. "
    "Portanto, os resultados abaixo representam apenas a "
    "amostra simulada, e não dados reais de São Paulo."
)
probabilidades_regioes = []
for regiao in regioes:
    total_regiao = 0
    atrasadas_regiao = 0
    soma_tempo_regiao = 0

    for entrega in entregas:
        if entrega["regiao"] == regiao:
            total_regiao += 1
            soma_tempo_regiao += entrega["tempo_real"]
            if entrega["status"] == "Atrasada":
                atrasadas_regiao += 1
    if total_regiao > 0:
        probabilidade_regiao = (
            atrasadas_regiao / total_regiao
        ) * 100
        media_regiao = (
            soma_tempo_regiao / total_regiao
        )
    else:
        probabilidade_regiao = 0
        media_regiao = 0

    probabilidades_regioes.append(
        probabilidade_regiao
    )

    print("\nRegião:", regiao)
    print(
        "Total de entregas:",
        total_regiao
    )
    print(
        "Entregas atrasadas:",
        atrasadas_regiao
    )
    print(
        "Probabilidade de atraso:",
        round(probabilidade_regiao, 2),
        "%"
    )
    print(
        "Média do tempo real:",
        round(media_regiao, 2),
        "dias"
    )

# Gráfico 1 - Entregas no prazo x atrasadas
categorias = [
    "No prazo",
    "Atrasadas"
]

quantidades = [
    entregas_no_prazo,
    entregas_atrasadas
]

cores_status = [
    "#2E8B57",
    "#DC3545"
]

plt.figure(figsize=(8, 5))

barras = plt.bar(
    categorias,
    quantidades,
    color=cores_status,
    edgecolor="black"
)

plt.title(
    "Situação das Entregas",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Status")
plt.ylabel("Quantidade de Entregas")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 1,
        str(int(altura)),
        ha="center"
    )

plt.tight_layout()
plt.show()

# Gráfico 2 - Distribuição dos tempos
tempos_reais = []
for entrega in entregas:
    tempos_reais.append(
        entrega["tempo_real"]
    )

plt.figure(figsize=(9, 5))

plt.hist(
    tempos_reais,
    bins=10,
    color="#4C78A8",
    edgecolor="black",
    alpha=0.8
)

plt.axvline(
    media_tempo_real,
    color="#DC3545",
    linestyle="--",
    linewidth=2,
    label="Média"
)

plt.title(
    "Distribuição dos Tempos Reais de Entrega",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Tempo real de entrega (dias)")
plt.ylabel("Frequência")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.legend()

plt.tight_layout()
plt.show()

# Gráfico 3 - Probabilidade de atraso por região
cores_regioes = [
    "#4C78A8",
    "#F58518",
    "#54A24B",
    "#E45756",
    "#B279A2"
]

plt.figure(figsize=(10, 6))

barras = plt.bar(
    regioes,
    probabilidades_regioes,
    color=cores_regioes,
    edgecolor="black"
)

plt.title(
    "Probabilidade de Atraso por Região",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Região de São Paulo")
plt.ylabel("Probabilidade de Atraso (%)")

plt.ylim(0, 100)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 1,
        str(round(altura, 1)) + "%",
        ha="center"
    )

plt.tight_layout()
plt.show()

# Gráfico 4 - Diferença entre tempo real e prazo previsto
diferencas_prazo = []
for entrega in entregas:
    diferenca = (
        entrega["tempo_real"] -
        entrega["prazo_previsto"]
    )

    diferencas_prazo.append(diferenca)

plt.figure(figsize=(9, 5))

plt.hist(
    diferencas_prazo,
    bins=10,
    color="#7A5195",
    edgecolor="black",
    alpha=0.8
)

plt.axvline(
    0,
    color="#2E8B57",
    linestyle="--",
    linewidth=2,
    label="Prazo previsto"
)

plt.axvline(
    -0.2,
    color="#DC3545",
    linestyle="--",
    linewidth=2,
    label="Média simulada (-0,2 dia)"
)

plt.title(
    "Distribuição da Diferença entre Tempo Real e Prazo"
)

plt.xlabel(
    "Diferença em relação ao prazo previsto (dias)"
)

plt.ylabel("Frequência")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.legend()

plt.tight_layout()
plt.show()

# Simulação de diferentes cenários
print("\n--- Simulação de Cenários ---")
media_cenario_1 = 3
desvio_cenario_1 = 0.5
tempos_cenario_1 = []

for i in range(100):
    tempo = random.gauss(
        media_cenario_1,
        desvio_cenario_1
    )

    if tempo <= 0:
        tempo = 0.5

    tempos_cenario_1.append(tempo)

media_cenario_2 = 4
desvio_cenario_2 = 0.8
tempos_cenario_2 = []

for i in range(100):
    tempo = random.gauss(
        media_cenario_2,
        desvio_cenario_2
    )

    if tempo <= 0:
        tempo = 0.5

    tempos_cenario_2.append(tempo)

media_cenario_3 = 3
desvio_cenario_3 = 1.2
tempos_cenario_3 = []

for i in range(100):
    tempo = random.gauss(
        media_cenario_3,
        desvio_cenario_3
    )

    if tempo <= 0:
        tempo = 0.5

    tempos_cenario_3.append(tempo)

# Média do cenário 1
soma_cenario_1 = 0
for tempo in tempos_cenario_1:
    soma_cenario_1 += tempo

resultado_media_cenario_1 = (
    soma_cenario_1 / len(tempos_cenario_1)
)


# Média do cenário 2
soma_cenario_2 = 0
for tempo in tempos_cenario_2:
    soma_cenario_2 += tempo

resultado_media_cenario_2 = (
    soma_cenario_2 / len(tempos_cenario_2)
)


# Média do cenário 3
soma_cenario_3 = 0
for tempo in tempos_cenario_3:
    soma_cenario_3 += tempo

resultado_media_cenario_3 = (
    soma_cenario_3 / len(tempos_cenario_3)
)

# Desvio padrão do cenário 1
soma_quadrados_cenario_1 = 0
for tempo in tempos_cenario_1:
    diferenca = tempo - resultado_media_cenario_1
    soma_quadrados_cenario_1 += diferenca ** 2

variancia_cenario_1 = (
    soma_quadrados_cenario_1 /
    len(tempos_cenario_1)
)

resultado_desvio_cenario_1 = (
    variancia_cenario_1 ** 0.5
)

# Desvio padrão do cenário 2
soma_quadrados_cenario_2 = 0
for tempo in tempos_cenario_2:
    diferenca = tempo - resultado_media_cenario_2
    soma_quadrados_cenario_2 += diferenca ** 2

variancia_cenario_2 = (
    soma_quadrados_cenario_2 /
    len(tempos_cenario_2)
)

resultado_desvio_cenario_2 = (
    variancia_cenario_2 ** 0.5
)

# Desvio padrão do cenário 3
soma_quadrados_cenario_3 = 0
for tempo in tempos_cenario_3:
    diferenca = tempo - resultado_media_cenario_3
    soma_quadrados_cenario_3 += diferenca ** 2

variancia_cenario_3 = (
    soma_quadrados_cenario_3 /
    len(tempos_cenario_3)
)

resultado_desvio_cenario_3 = (
    variancia_cenario_3 ** 0.5
)

print(
    "Cenário 1 - Operação normal | Média:",
    round(resultado_media_cenario_1, 2),
    "dias | Desvio padrão:",
    round(resultado_desvio_cenario_1, 2)
)
print(
    "Cenário 2 - Maior tempo médio | Média:",
    round(resultado_media_cenario_2, 2),
    "dias | Desvio padrão:",
    round(resultado_desvio_cenario_2, 2)
)
print(
    "Cenário 3 - Maior variação | Média:",
    round(resultado_media_cenario_3, 2),
    "dias | Desvio padrão:",
    round(resultado_desvio_cenario_3, 2)
)

# Conclusão
print("\n--- Conclusão ---")
print(
    "A análise mostrou como a probabilidade e a "
    "distribuição normal podem ser utilizadas para "
    "estudar prazos de entregas em uma operação logística."
)
print(
    "Os dados utilizados são fictícios e foram gerados "
    "por simulação para representar entregas na cidade "
    "de São Paulo."
)
print(
    "Os resultados podem ajudar na identificação de "
    "atrasos, variações dos tempos de entrega e diferenças "
    "entre regiões dentro do cenário simulado."
)