V = [10, 4, 8, 2, 9, 3, 7, 5]

def quick_sort(lista):
    if len(lista) <= 1:
        return lista

    pivo = lista[-1]
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

    resultado_ordenado = quick_sort(menores) + iguais + quick_sort(maiores)
    return resultado_ordenado

quick_sort(V)
