"""Funcoes de calculo da sessao de recarga.

Conceitos usados: variaveis, funcoes, condicionais e dicionario.
"""

from datetime import datetime


def calcular_sessao(potencia_kw, duracao_minutos, percentual_solar):
    """Calcula os dados de uma sessao de recarga.

    Retorna um dicionario com os resultados.
    Levanta ValueError se os dados forem invalidos.
    """
    # Validacoes simples
    if potencia_kw <= 0:
        raise ValueError("Potencia deve ser maior que zero.")
    if duracao_minutos <= 0:
        raise ValueError("Duracao deve ser maior que zero.")
    if percentual_solar < 0 or percentual_solar > 100:
        raise ValueError("Percentual solar deve estar entre 0 e 100.")

    # 1. Converte minutos para horas
    tempo_horas = duracao_minutos / 60

    # 2. Energia total consumida
    energia_total = round(potencia_kw * tempo_horas, 2)

    # 3. Energia de origem solar
    energia_solar = round(energia_total * percentual_solar / 100, 2)

    # 4. Energia proveniente da rede (garante soma exata)
    energia_rede = round(energia_total - energia_solar, 2)

    # 5. Percentual renovavel
    if energia_total > 0:
        percentual_renovavel = round(energia_solar / energia_total * 100, 2)
    else:
        percentual_renovavel = 0.0

    # 6. Data e hora do registro
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    sessao = {
        "data_hora": data_hora,
        "potencia_kw": potencia_kw,
        "duracao_minutos": int(duracao_minutos),
        "energia_total_kwh": energia_total,
        "energia_solar_kwh": energia_solar,
        "energia_rede_kwh": energia_rede,
        "percentual_renovavel": percentual_renovavel,
    }
    return sessao


def formatar_duracao(duracao_minutos):
    """Transforma minutos em texto tipo '1h30' ou '90 min'."""
    duracao_minutos = int(duracao_minutos)
    horas = duracao_minutos // 60
    minutos = duracao_minutos % 60

    if horas > 0 and minutos > 0:
        return f"{horas}h{minutos:02d}"
    if horas > 0:
        return f"{horas}h"
    return f"{minutos} min"
