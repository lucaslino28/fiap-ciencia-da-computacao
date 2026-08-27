numeros = [5, 3, 8, 2]

def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j] > lista [j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def selection_sort(lista):
    n = len(lista)
    for i in range(n):
        menor = i
        for j in range(i + 1, n):
            if lista[j] < lista[menor]:
                menor = j
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista

def insertion_sort(lista):
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > atual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista

print("bubble_sort:")
print(bubble_sort(numeros))
print("selection_sort:")
print(selection_sort(numeros))
print("insertion+sort:")
print(insertion_sort(numeros))