numeros = (5, 8, 10, 3, 12, 7, 4)

contador = 0

for numero in numeros:
    if numero % 2 == 0:
        contador += 1

print(f'Quantidade de pares: {contador}')