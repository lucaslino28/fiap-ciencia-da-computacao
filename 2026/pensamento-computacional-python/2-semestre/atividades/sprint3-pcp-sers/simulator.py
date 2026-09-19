"""Lógica da simulação realista de recarga CA com carregadores GoodWe HCA."""

from datetime import datetime
from math import ceil


CARREGADORES_GOODWE = {
    "GW7K-HCA": {
        "potencia_kw": 7.0,
        "tensao_v": 230,
        "corrente_a": 32,
        "fases": "Monofásico",
    },
    "GW11K-HCA": {
        "potencia_kw": 11.0,
        "tensao_v": 400,
        "corrente_a": 16,
        "fases": "Trifásico",
    },
    "GW22K-HCA": {
        "potencia_kw": 22.0,
        "tensao_v": 400,
        "corrente_a": 32,
        "fases": "Trifásico",
    },
}

EFICIENCIA_PADRAO_PERCENTUAL = 90.0


# ==================================================
# PLANEJAMENTO DA SESSÃO
# ==================================================

def calcular_plano_recarga(
    modelo_carregador,
    capacidade_bateria_kwh,
    soc_inicial,
    soc_alvo,
    potencia_max_veiculo_kw,
    potencia_solar_kw,
    tarifa_kwh,
    eficiencia_percentual=EFICIENCIA_PADRAO_PERCENTUAL,
):
    """Calcula potência, energia, duração e custo previstos para a sessão."""
    if modelo_carregador not in CARREGADORES_GOODWE:
        raise ValueError("Modelo de carregador GoodWe inválido.")
    if capacidade_bateria_kwh <= 0:
        raise ValueError("A capacidade da bateria deve ser maior que zero.")
    if not 0 <= soc_inicial < soc_alvo <= 100:
        raise ValueError("A carga desejada deve ser maior que a carga inicial.")
    if potencia_max_veiculo_kw <= 0:
        raise ValueError("O limite CA do veículo deve ser maior que zero.")
    if potencia_solar_kw < 0:
        raise ValueError("A potência solar não pode ser negativa.")
    if tarifa_kwh < 0:
        raise ValueError("A tarifa não pode ser negativa.")
    if not 50 <= eficiencia_percentual <= 100:
        raise ValueError("A eficiência deve estar entre 50% e 100%.")

    carregador = CARREGADORES_GOODWE[modelo_carregador]
    potencia_efetiva_kw = min(
        carregador["potencia_kw"],
        float(potencia_max_veiculo_kw),
    )
    potencia_solar_utilizada_kw = min(
        float(potencia_solar_kw),
        potencia_efetiva_kw,
    )
    potencia_rede_kw = potencia_efetiva_kw - potencia_solar_utilizada_kw
    eficiencia = eficiencia_percentual / 100

    energia_bateria_necessaria_kwh = (
        capacidade_bateria_kwh * (soc_alvo - soc_inicial) / 100
    )
    energia_total_necessaria_kwh = energia_bateria_necessaria_kwh / eficiencia
    duracao_exata_minutos = energia_total_necessaria_kwh / potencia_efetiva_kw * 60
    participacao_solar = potencia_solar_utilizada_kw / potencia_efetiva_kw
    energia_solar_prevista_kwh = energia_total_necessaria_kwh * participacao_solar
    energia_rede_prevista_kwh = energia_total_necessaria_kwh - energia_solar_prevista_kwh

    return {
        "modelo_carregador": modelo_carregador,
        "potencia_nominal_kw": carregador["potencia_kw"],
        "potencia_efetiva_kw": potencia_efetiva_kw,
        "potencia_solar_utilizada_kw": potencia_solar_utilizada_kw,
        "potencia_rede_kw": potencia_rede_kw,
        "tensao_v": carregador["tensao_v"],
        "corrente_a": carregador["corrente_a"],
        "fases": carregador["fases"],
        "capacidade_bateria_kwh": float(capacidade_bateria_kwh),
        "soc_inicial": float(soc_inicial),
        "soc_alvo": float(soc_alvo),
        "eficiencia_percentual": float(eficiencia_percentual),
        "energia_bateria_necessaria_kwh": energia_bateria_necessaria_kwh,
        "energia_total_necessaria_kwh": energia_total_necessaria_kwh,
        "energia_solar_prevista_kwh": energia_solar_prevista_kwh,
        "energia_rede_prevista_kwh": energia_rede_prevista_kwh,
        "perdas_previstas_kwh": energia_total_necessaria_kwh - energia_bateria_necessaria_kwh,
        "percentual_renovavel_previsto": participacao_solar * 100,
        "duracao_exata_minutos": duracao_exata_minutos,
        "duracao_estimada_minutos": ceil(duracao_exata_minutos),
        "tarifa_kwh": float(tarifa_kwh),
        "custo_previsto": energia_rede_prevista_kwh * tarifa_kwh,
    }


# ==================================================
# CÁLCULO DA SESSÃO
# ==================================================

def calcular_sessao(
    modelo_carregador,
    duracao_minutos,
    capacidade_bateria_kwh,
    soc_inicial,
    soc_alvo,
    potencia_max_veiculo_kw,
    potencia_solar_kw,
    tarifa_kwh,
    eficiencia_percentual=EFICIENCIA_PADRAO_PERCENTUAL,
):
    """Calcula o estado acumulado de uma recarga CA em andamento."""
    if duracao_minutos < 0:
        raise ValueError("A duração não pode ser negativa.")

    plano = calcular_plano_recarga(
        modelo_carregador,
        capacidade_bateria_kwh,
        soc_inicial,
        soc_alvo,
        potencia_max_veiculo_kw,
        potencia_solar_kw,
        tarifa_kwh,
        eficiencia_percentual,
    )

    duracao_efetiva_minutos = min(
        float(duracao_minutos),
        plano["duracao_exata_minutos"],
    )
    energia_total = min(
        plano["potencia_efetiva_kw"] * duracao_efetiva_minutos / 60,
        plano["energia_total_necessaria_kwh"],
    )
    participacao_solar = (
        plano["potencia_solar_utilizada_kw"] / plano["potencia_efetiva_kw"]
    )
    energia_solar = energia_total * participacao_solar
    energia_rede = energia_total - energia_solar
    energia_bateria = energia_total * eficiencia_percentual / 100
    perdas = energia_total - energia_bateria
    soc_atual = min(
        soc_alvo,
        soc_inicial + energia_bateria / capacidade_bateria_kwh * 100,
    )
    concluida = duracao_minutos >= plano["duracao_exata_minutos"] - 1e-9

    return {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "modelo_carregador": modelo_carregador,
        "potencia_nominal_kw": round(plano["potencia_nominal_kw"], 2),
        "potencia_kw": round(plano["potencia_efetiva_kw"], 2),
        "potencia_solar_kw": round(plano["potencia_solar_utilizada_kw"], 2),
        "potencia_rede_kw": round(plano["potencia_rede_kw"], 2),
        "duracao_minutos": ceil(duracao_efetiva_minutos),
        "duracao_estimada_minutos": plano["duracao_estimada_minutos"],
        "tempo_restante_minutos": max(
            0,
            ceil(plano["duracao_exata_minutos"] - duracao_efetiva_minutos),
        ),
        "capacidade_bateria_kwh": round(float(capacidade_bateria_kwh), 2),
        "soc_inicial": round(float(soc_inicial), 1),
        "soc_alvo": round(float(soc_alvo), 1),
        "soc_atual": round(soc_atual, 1),
        "energia_total_kwh": round(energia_total, 2),
        "energia_bateria_kwh": round(energia_bateria, 2),
        "energia_solar_kwh": round(energia_solar, 2),
        "energia_rede_kwh": round(energia_rede, 2),
        "perdas_kwh": round(perdas, 2),
        "percentual_renovavel": round(participacao_solar * 100, 2),
        "eficiencia_percentual": round(float(eficiencia_percentual), 1),
        "tarifa_kwh": round(float(tarifa_kwh), 2),
        "custo_estimado": round(energia_rede * tarifa_kwh, 2),
        "concluida": concluida,
        "tensao_v": plano["tensao_v"],
        "corrente_a": plano["corrente_a"],
        "fases": plano["fases"],
    }


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
