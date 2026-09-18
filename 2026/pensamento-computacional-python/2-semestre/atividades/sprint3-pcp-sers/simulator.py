"""Lógica da simulação de recarga.

Responsável por:
- validar os dados;
- calcular consumo de energia;
- calcular energia solar;
- calcular energia da rede;
- calcular participação renovável;
- formatar duração.
"""

from datetime import datetime


# ==================================================
# CÁLCULO DA SESSÃO
# ==================================================

def calcular_sessao(
    potencia_kw,
    duracao_minutos,
    percentual_solar
):
    """Calcula os dados de uma sessão de recarga."""

    # =========================
    # VALIDAÇÕES
    # =========================

    if potencia_kw <= 0:
        raise ValueError(
            "A potência deve ser maior que zero."
        )

    if duracao_minutos <= 0:
        raise ValueError(
            "A duração deve ser maior que zero."
        )

    if percentual_solar < 0 or percentual_solar > 100:
        raise ValueError(
            "O percentual solar deve estar entre 0 e 100."
        )


    # =========================
    # TEMPO
    # =========================

    tempo_horas = duracao_minutos / 60


    # =========================
    # ENERGIA TOTAL
    # =========================

    energia_total = (
        potencia_kw
        * tempo_horas
    )


    # =========================
    # ENERGIA SOLAR
    # =========================

    energia_solar = (
        energia_total
        * percentual_solar
        / 100
    )


    # =========================
    # ENERGIA DA REDE
    # =========================

    energia_rede = (
        energia_total
        - energia_solar
    )


    # =========================
    # PARTICIPAÇÃO RENOVÁVEL
    # =========================

    if energia_total > 0:

        percentual_renovavel = (
            energia_solar
            / energia_total
        ) * 100

    else:

        percentual_renovavel = 0


    # =========================
    # DATA E HORA
    # =========================

    data_hora = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )


    # =========================
    # RESULTADO
    # =========================

    sessao = {
        "data_hora": data_hora,

        "potencia_kw": round(
            float(potencia_kw),
            2
        ),

        "duracao_minutos": int(
            duracao_minutos
        ),

        "energia_total_kwh": round(
            energia_total,
            2
        ),

        "energia_solar_kwh": round(
            energia_solar,
            2
        ),

        "energia_rede_kwh": round(
            energia_rede,
            2
        ),

        "percentual_renovavel": round(
            percentual_renovavel,
            2
        )
    }

    return sessao


# ==================================================
# FORMATAÇÃO DA DURAÇÃO
# ==================================================

def formatar_duracao(duracao_minutos):
    """Converte minutos para um formato mais amigável."""

    duracao_minutos = int(
        duracao_minutos
    )

    horas = duracao_minutos // 60

    minutos = duracao_minutos % 60


    if horas > 0 and minutos > 0:

        return f"{horas}h {minutos:02d}min"


    if horas > 0:

        return f"{horas}h"


    return f"{minutos} min"