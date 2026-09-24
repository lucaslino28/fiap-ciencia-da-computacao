V = [10, 4, 8, 2, 9, 3, 7, 5]

def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = lista[:meio]
    direita = lista[meio:]

    esquerda = merge_sort(esquerda)
    direita = merge_sort(direita)
    return merge(esquerda, direita)

merge_sort(V)
