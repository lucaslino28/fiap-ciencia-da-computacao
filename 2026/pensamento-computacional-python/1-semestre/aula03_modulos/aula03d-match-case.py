# Imagina um programa... que recebe a esolha do usuário
# 0 --> sair do programa
# 1 --> entrar no programa
# ----> erro!

escolha_usuario = 1232131

match escolha_usuario:
    case 0:
        print("Sair do programa")
    case 1:
        print("Entrar no programa")
    case _:
        print("ERRO!")