import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# CP5 - MODELAGEM LINEAR PARA APRENDIZADO DE MÁQUINA
# Tema: Análise da Otimização de Rotas Logísticas

# DADOS

# Tempos de entrega, em minutos, de uma operação logística
# utilizando o método tradicional de roteirização.
rota_tradicional = np.array([
    52, 48, 55, 50, 61, 57, 49, 54, 58, 53,
    47, 56, 60, 51, 59, 50, 55, 62, 48, 53,
    57, 52, 54, 58, 49, 56, 61, 50, 55, 53
])

# Tempos de entrega, em minutos, utilizando uma estratégia
# de roteirização otimizada.
rota_otimizada = np.array([
    45, 43, 47, 44, 50, 48, 42, 46, 49, 45,
    41, 47, 51, 43, 48, 44, 46, 52, 42, 45,
    49, 44, 46, 48, 43, 47, 50, 44, 46, 45
])

# ESTATÍSTICAS DESCRITIVAS
def calcular_estatisticas(dados):
    media = np.mean(dados)
    desvio_padrao = np.std(dados, ddof=1)
    quantidade = len(dados)

    return media, desvio_padrao, quantidade


# TESTE DE HIPÓTESE

def teste_hipotese(amostra1, amostra2):
    media1, desvio1, n1 = calcular_estatisticas(amostra1)
    media2, desvio2, n2 = calcular_estatisticas(amostra2)

    # Erro padrão
    erro_padrao = np.sqrt(
        (desvio1 ** 2 / n1) +
        (desvio2 ** 2 / n2)
    )

    # Estatística t
    estatistica_t = (
        media1 - media2
    ) / erro_padrao

    # Graus de liberdade pelo método de Welch
    numerador = (
        (desvio1 ** 2 / n1) +
        (desvio2 ** 2 / n2)
    ) ** 2

    denominador = (
        ((desvio1 ** 2 / n1) ** 2 / (n1 - 1)) +
        ((desvio2 ** 2 / n2) ** 2 / (n2 - 1))
    )

    graus_liberdade = numerador / denominador

    # Valor-p unilateral
    valor_p = t.sf(
        estatistica_t,
        graus_liberdade
    )

    return estatistica_t, graus_liberdade, valor_p

# ANÁLISE PRINCIPAL
def analisar_dados():

    media_tradicional, desvio_tradicional, n_tradicional = (
        calcular_estatisticas(rota_tradicional)
    )

    media_otimizada, desvio_otimizada, n_otimizada = (
        calcular_estatisticas(rota_otimizada)
    )

    estatistica_t, graus_liberdade, valor_p = teste_hipotese(
        rota_tradicional,
        rota_otimizada
    )

    nivel_significancia = 0.05

    reducao_minutos = (
        media_tradicional - media_otimizada
    )

    reducao_percentual = (
        reducao_minutos / media_tradicional
    ) * 100

    print("=" * 65)
    print("CP5 - MODELAGEM LINEAR PARA APRENDIZADO DE MÁQUINA")
    print("Tema: Análise da Otimização de Rotas Logísticas")
    print("=" * 65)

    print("\n1. ESTATÍSTICAS DESCRITIVAS")

    print("\nRota tradicional:")
    print(f"Quantidade de entregas: {n_tradicional}")
    print(f"Tempo médio: {media_tradicional:.2f} minutos")
    print(f"Desvio padrão: {desvio_tradicional:.2f} minutos")

    print("\nRota otimizada:")
    print(f"Quantidade de entregas: {n_otimizada}")
    print(f"Tempo médio: {media_otimizada:.2f} minutos")
    print(f"Desvio padrão: {desvio_otimizada:.2f} minutos")

    print("\n2. IMPACTO DA OTIMIZAÇÃO")

    print(
        f"Redução média: "
        f"{reducao_minutos:.2f} minutos"
    )

    print(
        f"Redução percentual: "
        f"{reducao_percentual:.2f}%"
    )

    print("\n3. TESTE DE HIPÓTESE")

    print(
        "H0: A rota otimizada não reduz "
        "o tempo médio de entrega."
    )

    print(
        "H1: A rota otimizada reduz "
        "o tempo médio de entrega."
    )

    print(
        f"\nEstatística t: "
        f"{estatistica_t:.4f}"
    )

    print(
        f"Graus de liberdade: "
        f"{graus_liberdade:.2f}"
    )

    print(
        f"Valor-p: "
        f"{valor_p:.3e}"
    )

    print(
        f"Nível de significância: "
        f"{nivel_significancia}"
    )

    print("\n4. CONCLUSÃO")

    if valor_p < nivel_significancia:

        print(
            "Rejeitamos a hipótese nula (H0)."
        )

        print(
            "Existem evidências estatísticas de que "
            "a rota otimizada reduz o tempo médio "
            "de entrega."
        )

    else:

        print(
            "Não rejeitamos a hipótese nula (H0)."
        )

        print(
            "Não existem evidências estatísticas "
            "suficientes para afirmar que a rota "
            "otimizada reduz o tempo médio."
        )


# GRÁFICO 1: COMPARAÇÃO DAS MÉDIAS
def grafico_medias():

    media_tradicional = np.mean(
        rota_tradicional
    )

    media_otimizada = np.mean(
        rota_otimizada
    )

    medias = [
        media_tradicional,
        media_otimizada
    ]

    nomes = [
        "Rota Tradicional",
        "Rota Otimizada"
    ]

    reducao = (
        (media_tradicional - media_otimizada)
        / media_tradicional
    ) * 100

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    barras = ax.bar(
        nomes,
        medias,
        width=0.55
    )

    ax.set_title(
        "Comparação do Tempo Médio de Entrega",
        fontsize=17,
        fontweight="bold",
        pad=18
    )

    ax.set_ylabel(
        "Tempo médio (minutos)",
        fontsize=12
    )

    ax.set_ylim(
        0,
        68
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    for barra, media in zip(
        barras,
        medias
    ):

        ax.text(
            barra.get_x()
            + barra.get_width() / 2,
            media + 0.8,
            f"{media:.2f} min",
            ha="center",
            fontsize=12,
            fontweight="bold"
        )

    ax.text(
        0.5,
        61.5,
        f"Redução média de {reducao:.1f}%",
        ha="center",
        fontsize=13
    )

    fig.tight_layout()

    fig.savefig(
        "01_comparacao_medias.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

# GRÁFICO 2: DISTRIBUIÇÃO DOS TEMPOS
def grafico_boxplot():

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.boxplot(
        [
            rota_tradicional,
            rota_otimizada
        ],
        tick_labels=[
            "Rota Tradicional",
            "Rota Otimizada"
        ],
        patch_artist=True,
        widths=0.5
    )

    ax.set_title(
        "Distribuição dos Tempos de Entrega",
        fontsize=17,
        fontweight="bold",
        pad=18
    )

    ax.set_ylabel(
        "Tempo de entrega (minutos)",
        fontsize=12
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    mediana_tradicional = np.median(
        rota_tradicional
    )

    mediana_otimizada = np.median(
        rota_otimizada
    )

    ax.text(
        1,
        mediana_tradicional + 1,
        f"Mediana: {mediana_tradicional:.1f}",
        ha="center",
        fontsize=11
    )

    ax.text(
        2,
        mediana_otimizada + 1,
        f"Mediana: {mediana_otimizada:.1f}",
        ha="center",
        fontsize=11
    )

    fig.tight_layout()

    fig.savefig(
        "02_distribuicao_tempos.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

# GRÁFICO 3: COMPARAÇÃO DAS OBSERVAÇÕES
def grafico_entregas():

    observacoes = np.arange(
        1,
        len(rota_tradicional) + 1
    )

    media_tradicional = np.mean(
        rota_tradicional
    )

    media_otimizada = np.mean(
        rota_otimizada
    )

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        observacoes,
        rota_tradicional,
        marker="o",
        linewidth=2,
        markersize=5,
        label="Rota Tradicional"
    )

    ax.plot(
        observacoes,
        rota_otimizada,
        marker="o",
        linewidth=2,
        markersize=5,
        label="Rota Otimizada"
    )

    ax.axhline(
        media_tradicional,
        linestyle="--",
        alpha=0.6,
        label=(
            f"Média Tradicional "
            f"({media_tradicional:.1f} min)"
        )
    )

    ax.axhline(
        media_otimizada,
        linestyle="--",
        alpha=0.6,
        label=(
            f"Média Otimizada "
            f"({media_otimizada:.1f} min)"
        )
    )

    ax.set_title(
        "Comparação dos Tempos nas Amostras",
        fontsize=17,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel(
        "Observação da amostra",
        fontsize=12
    )

    ax.set_ylabel(
        "Tempo de entrega (minutos)",
        fontsize=12
    )

    ax.set_xticks(
        np.arange(1, 31, 2)
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    ax.legend(
        loc="upper right"
    )

    fig.tight_layout()

    fig.savefig(
        "03_comparacao_amostras.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

# GRÁFICO 4: SIMULAÇÃO DE CENÁRIOS
def grafico_cenarios():

    # Garante que os valores simulados sejam
    # sempre iguais a cada execução.
    np.random.seed(42)

    media_referencia = np.mean(
        rota_tradicional
    )

    nomes_cenarios = [
        "Sem otimização",
        "Pequena melhoria",
        "Melhoria moderada",
        "Grande melhoria"
    ]

    # Primeiro cenário utiliza os próprios dados tradicionais.
    dados_cenarios = [
        rota_tradicional,

        np.random.normal(
            loc=52,
            scale=4,
            size=30
        ),

        np.random.normal(
            loc=48,
            scale=4,
            size=30
        ),

        np.random.normal(
            loc=44,
            scale=4,
            size=30
        )
    ]

    medias_simuladas = []
    reducoes = []
    valores_p = []

    print("\n" + "=" * 65)
    print("SIMULAÇÃO DE CENÁRIOS")
    print("=" * 65)

    for nome, dados in zip(
        nomes_cenarios,
        dados_cenarios
    ):

        media_cenario = np.mean(
            dados
        )

        reducao = (
            (media_referencia - media_cenario)
            / media_referencia
        ) * 100

        # O cenário sem otimização é a referência.
        if nome == "Sem otimização":

            valor_p = 0.5

        else:

            _, _, valor_p = teste_hipotese(
                rota_tradicional,
                dados
            )

        medias_simuladas.append(
            media_cenario
        )

        reducoes.append(
            reducao
        )

        valores_p.append(
            valor_p
        )

        print(
            f"\nCenário: {nome}"
        )

        print(
            f"Tempo médio: "
            f"{media_cenario:.2f} minutos"
        )

        print(
            f"Redução: "
            f"{reducao:.2f}%"
        )

        if nome == "Sem otimização":

            print(
                "Valor-p: cenário de referência"
            )

            print(
                "Resultado: situação utilizada "
                "como base de comparação."
            )

        else:

            print(
                f"Valor-p: "
                f"{valor_p:.3e}"
            )

            if valor_p < 0.05:

                print(
                    "Resultado: diferença "
                    "estatisticamente significativa."
                )

            else:

                print(
                    "Resultado: diferença não "
                    "estatisticamente significativa."
                )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    barras = ax.bar(
        nomes_cenarios,
        medias_simuladas,
        width=0.62
    )

    ax.axhline(
        media_referencia,
        linestyle="--",
        linewidth=2,
        label=(
            f"Referência: "
            f"{media_referencia:.1f} min"
        )
    )

    ax.set_title(
        "Impacto de Diferentes Cenários de Otimização",
        fontsize=17,
        fontweight="bold",
        pad=18
    )

    ax.set_ylabel(
        "Tempo médio de entrega (minutos)",
        fontsize=12
    )

    ax.set_xlabel(
        "Cenários simulados",
        fontsize=12
    )

    ax.set_ylim(
        0,
        70
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    for i, (
        barra,
        media,
        reducao,
        valor_p
    ) in enumerate(
        zip(
            barras,
            medias_simuladas,
            reducoes,
            valores_p
        )
    ):

        altura = barra.get_height()

        ax.text(
            barra.get_x()
            + barra.get_width() / 2,
            altura + 0.7,
            f"{media:.1f} min",
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

        if i == 0:

            texto = "Referência"

        else:

            if valor_p < 0.05:
                significancia = "Significativo"
            else:
                significancia = "Não significativo"

            texto = (
                f"Redução: {reducao:.1f}%\n"
                f"{significancia}"
            )

        ax.text(
            barra.get_x()
            + barra.get_width() / 2,
            altura + 4,
            texto,
            ha="center",
            fontsize=10
        )

    ax.legend(
        loc="lower left"
    )

    fig.tight_layout()

    fig.savefig(
        "04_simulacao_cenarios.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

# EXECUÇÃO
def main():

    analisar_dados()

    grafico_medias()

    grafico_boxplot()

    grafico_entregas()

    grafico_cenarios()

    print("\n" + "=" * 65)

    print(
        "ANÁLISE CONCLUÍDA COM SUCESSO"
    )

    print(
        "Os quatro gráficos foram salvos "
        "na pasta do projeto."
    )

    print("=" * 65)


if __name__ == "__main__":
    main()