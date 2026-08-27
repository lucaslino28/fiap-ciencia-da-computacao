# cp = 0
# while cp < 3:
#     print(f'Produto {cp}')
#     cp += 1
#
# # While
# i = 4
# while i > 0:
#     print(i)
#     i -= 1
#
# # Repetição com entrada do usuário
# jogar = "Sim"
#
# while jogar.lower() == "sim":
#     print("Iniciar ou repetir o jogo")
#     jogar = input("Deseja jogar novamente? ")

i = 0
while i < 10:
    i += 1

    if i == 3 or i == 5:
        continue

    if i ==7:
        break

    print(f"Produto {i}")
