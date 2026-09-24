V = [10, 4, 8, 2, 9, 3, 7, 5]
pivo_teste = 8

def particionar(lista, pivo):
    menores = []
    iguais = []
    maiores = []

    for elemento in lista:
        if elemento < pivo:
            menores.append(elemento)
        elif elemento == pivo:
            iguais.append(elemento)
        else:
            maiores.append(elemento)

    return menores, iguais, maiores

print(particionar(V, pivo_teste))