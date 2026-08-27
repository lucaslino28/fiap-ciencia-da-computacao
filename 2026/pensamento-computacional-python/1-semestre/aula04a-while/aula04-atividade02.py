# Ecreva um programa que dadas duas notas de 0 a 10
# calcula a média aritmética entre eleas.

def validar_nota(nota):
    while nota < 0 or nota > 10:
        print("A nota deve estar entre 0 e 10")
        nota = float(input("Digite a nota novamente: "))
    return nota

notaA = float(input("Digite a 1ª nota: "))
notaA = validar_nota(notaA)

notaB = float(input("Digite a 2ª nota: "))
notaB = validar_nota(notaB)

media = (notaA + notaB) / 2
print(media)



