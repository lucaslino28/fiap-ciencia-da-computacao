# Seção 2

# Ex3
valores = [4, 7, 2, 9, 5]

soma = 0

for v in valores:
    if v % 2 != 0:
        soma += v
print(soma)

# Ex4
numeros = [3, 6, 9, 12]

for i in range(len(numeros)):
    numeros[i] = numeros[i] + i
print(numeros)

# Ex5
matriz = [
    [2, 4, 6],
    [1, 3, 5],
    [7, 8, 9]
]

contador = 0

for linha in matriz:
    for valor in linha:
        if valor > 5:
            contador += 1

print(contador)

# Ex6
nomes = ["Ana", "Bruno", "Carlos", "Duda"]

for i in range(len(nomes)):
    if i % 2 == 0:
        print(nomes[i])

# Ex7
texto = "PYTHON"

resultado = ""

for letra in texto:
    resultado = letra + resultado

print(resultado)

# Ex8
dados = [
    [10, 20],
    [30, 40],
    [50, 60]
]

soma = 0

for i in range(len(dados)):
    soma += dados[i][1]
print(soma)

# Ex9
x = 0

while x < 10:
    x += 2

print(x)

# Ex10
matriz = [
    [1, 2, 3],
    [4, 5, 6]
]

for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        if matriz[i][j] % 2 == 0:
            print(matriz[i][j])