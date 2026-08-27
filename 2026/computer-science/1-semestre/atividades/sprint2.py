'''
Disciplina: COMPUTER SCIENCE
Turma: 1CCPX
Entrega: Sprint 02 – Algoritmo em Python e Simulação com Arduino
Equipe: ChargeGrid Intelligence

Integrantes:                          RM:
Bruno Riquelme Coutinho Pereira       569619
Eduardo Bigoli Portela                569897
Gabriel Martins Cordeiro Rodrigues    570497
Gustavo Fondato de Souza              573651
Gustavo Martins Da Silva              570584
Lucas Lino Marques da Silva           572863

Desafio: Carregamento Inteligente GoodWe
'''

# Função que lê uma entrada e só devolve o valor quando for 0 ou 1
def ler_entrada(nome):
    while True:
        valor = input(nome).strip()          # strip para tirar espaços digitados sem querer
        if valor == "0" or valor == "1":
            return int(valor)
        print("   O valor digitado deve ser 0 ou 1, digite novamente.")

# Definição das entradas digitadas pelo usuário
A = ler_entrada("A - RFID            (0 ou 1): ")
B = ler_entrada("B - Saldo           (0 ou 1): ")
C = ler_entrada("C - Cabo Conectado  (0 ou 1): ")
D = ler_entrada("D - Carga Completa  (0 ou 1): ")
E = ler_entrada("E - Sobrecarga      (0 ou 1): ")

# Calcula as saídas
S1 = A and B and C and (not D) and (not E)
S2 = A and B and C and (not D) and (not E)
S3 = (not C) and (not E)
S4 = C and (not E) and ((not A) or (not B) or D)
S5 = E

#Mostra as entradas digitadas pelo usuário e as saídas
print("\n_________ ESTADO DA ESTAÇÃO _________")
print(f"\nEntradas: A={A} B={B} C={C} D={D} E={E}")
print(f"S1 Relé de Carga     {'Ligado (carregando)' if S1 else 'Desligado'}")
print(f"S2 LED Azul          {'Aceso (Carregando)' if S2 else 'Apagado'}")
print(f"S3 LED Verde         {'Aceso (Livre)' if S3 else 'Apagado'}")
print(f"S4 LED Amarelo       {'Aceso (Aguardando ação)' if S4 else 'Apagado'}")
print(f"S5 LED Vermelho      {'Aceso (SOBRECARGA!)' if S5 else 'Apagado'}")

#Mostra um resumo de acordo com as saídas (seguindo ordem de prioridade)
print("\nResumo:")
if S5:
    print("   SOBRECARGA DETECTADA, USO SUSPENSO!")
elif S1:
    print("   Carregando o veículo normalmente")
elif S3:
    print("   Estação livre e pronta para uso")
elif S4:
    print("   Cabo conectado, mas a carga não foi liberada")
    print("   (Verifique o RFID, saldo ou se a bateria já esta cheia)")
else:
    print("   Nenhuma ação ativa no momento.")


