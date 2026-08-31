nota = float(input("Digite a nota: "))

while nota < 0 or nota > 10:
    print("Nota inválida!")
    nota = float(input("Digite novamente: "))

print("Nota válida:", nota)