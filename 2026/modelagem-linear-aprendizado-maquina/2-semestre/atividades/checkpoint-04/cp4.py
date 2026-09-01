regioes = [
    "Centro",
    "Zona Norte",
    "Zona Sul",
    "Zona Leste",
    "Zona Oeste"
]

entregas = [
    {
        "id": 1,
        "regiao": "Zona Sul",
        "prazo_previsto": 3,
        "tempo_real": 2.5
    },
    {
        "id": 2,
        "regiao": "Zona Leste",
        "prazo_previsto": 3,
        "tempo_real": 4.2
    },
    {
        "id": 3,
        "regiao": "Centro",
        "prazo_previsto": 2,
        "tempo_real": 2
    }
]

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

    print("\nEntrega:", entrega["id"])
    print("Região:", entrega["regiao"])
    print("Prazo previsto:", entrega["prazo_previsto"])
    print("Tempo real:", entrega["tempo_real"])
    print("Atraso:", atraso)
    print("Antecipação:", antecipacao)
    print("Status:", status)

total_entregas = len(entregas)

entregas_atrasadas = 0

for entrega in entregas:
    if entrega["status"] == "Atrasada":
        entregas_atrasadas += 1

probabilidade_atraso = (entregas_atrasadas / total_entregas) * 100

print("\n--- Análise de Probabilidade ---")
print("Total de entregas:", total_entregas)
print("Entregas atrasadas:", entregas_atrasadas)
print("Probabilidade de atraso:", round(probabilidade_atraso, 2), "%")