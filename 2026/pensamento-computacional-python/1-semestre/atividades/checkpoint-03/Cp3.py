# Seção 1
temperaturas = [
    [28, 31, 34, 33],
    [25, 27, 29, 28],
    [32, 35, 36, 34],
    [24, 26, 25, 27]
]

somas = [0, 0, 0, 0]
tempcriticas = [0, 0, 0, 0]
medias = [0, 0, 0, 0]

mais_critico = 0
sala_mais_critica = 0

for i in range(len(temperaturas)):
    for j in range(len(temperaturas[i])):

        somas[i] += temperaturas[i][j]

        if (temperaturas[i][j] >= 33):
            tempcriticas[i] += 1

for i in range(len(somas)):

    medias[i] = somas[i] / len(somas)

    sala = i + 1

    if (mais_critico < tempcriticas[i]):
        mais_critico = tempcriticas[i]
        sala_mais_critica = sala

    print(f"Sala: {sala}.")
    print(f"Media: {medias[i]}.")
    print(f"Registros crititcos: {tempcriticas[i]}.")

print(f"A sala com maior risco e: {sala_mais_critica}")