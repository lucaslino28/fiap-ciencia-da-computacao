# DESAFIO: ANALISADOR DE E-MAILS DA FIAP

# Recebe os e-mails digitados pelo usuário
entrada = input("Digite os e-mails separados por vírgula: ")

# Separa os e-mails pela vírgula
emails = entrada.split(",")

# Lista para armazenar os nomes dos usuários
usuarios = []

# Dicionário para contar os domínios
dominios = dict()


# Percorre cada e-mail
for email in emails:

    # Remove espaços antes ou depois do e-mail
    email = email.strip()

    # Separa o nome de usuário e o domínio
    usuario, dominio = email.split("@")

    # Adiciona o nome na lista de usuários
    usuarios.append(usuario)

    # Conta quantas vezes cada domínio aparece
    if dominio not in dominios:
        dominios[dominio] = 1
    else:
        dominios[dominio] += 1


# Organiza os usuários em ordem alfabética
usuarios.sort()

# Converte a lista para tupla
usuarios_tupla = tuple(usuarios)


print("\nRelatório:")

print("\nQuantidade de e-mails por domínio:")

for dominio in dominios:
    print(f"{dominio}: {dominios[dominio]}")


print("\nLista de usuários:", usuarios_tupla)

print("Primeiro usuário:", usuarios_tupla[0])
print("Último usuário:", usuarios_tupla[-1])


# Troca o primeiro e o último usuário
usuarios[0], usuarios[-1] = usuarios[-1], usuarios[0]

# Converte novamente para tupla
usuarios_trocados = tuple(usuarios)

print("Após troca de posições:", usuarios_trocados)