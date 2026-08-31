# Faça um programa que percorra os números de 1 até 20 e, em vez de mostrar os pares, conte quantos números pares existem.

contador = 0

for numero in range(1, 21):
    if numero % 2 == 0:
        contador += 1

print(contador)