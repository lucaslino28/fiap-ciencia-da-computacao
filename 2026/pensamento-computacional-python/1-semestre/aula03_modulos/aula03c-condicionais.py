# OPERADORES DE ATRIBUÇÃO
num = 15
print(num)

num = num + 2
print(num) #17

num *= 2
print(num)

# OPERADORES RELACIONAIS

print() #pular linha
print(6 >= 3)

idade = 20
print(idade == 20)

maior_idade = idade >= 18
print(maior_idade)

# OPERADORES LOGICOS
# LOGICA E (and)
print()

verifica_email = True
verifica_senha = False

login = verifica_email and verifica_senha
print(login)

if not login:
    print("Po cara acerta ai...")

print()
# NOTAS...

nota_final = 6

if nota_final < 4:
    print("Reprovado")
elif nota_final < 6:
    print("Recuperação")
else:
    print("Aprovado")

print("FIM")
