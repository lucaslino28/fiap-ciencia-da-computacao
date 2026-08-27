"""
 Neste problema, deve-se ler o nome de uma peça que chamaremos de peça1, o número de peças1 que
o usuário quer, o valor unitário de cada peça1, o nome de uma peça2, o número de peças2 e o valor
unitário de cada peça2. Após, calcule e mostre o valor a ser pago.
"""

# Entrada de dados para a Peça 1
nome_p1 = input("Nome da peça 1: ")
qtd_p1 = int(input(f"Quantidade de {nome_p1}: "))
valor_p1 = float(input(f"Valor unitário de {nome_p1}: "))

# Entrada de dados para a Peça 2
nome_p2 = input("\nNome da peça 2: ")
qtd_p2 = int(input(f"Quantidade de {nome_p2}: "))
valor_p2 = float(input(f"Valor unitário de {nome_p2}: "))

# Cálculos
total_p1 = qtd_p1 * valor_p1
total_p2 = qtd_p2 * valor_p2
valor_total = total_p1 + total_p2

# Exibição do resultado
print("-" * 30)
print(f"Resumo da compra:")
print(f"{nome_p1}: R$ {total_p1:.2f}")
print(f"{nome_p2}: R$ {total_p2:.2f}")
print(f"VALOR TOTAL A PAGAR: R$ {valor_total:.2f}")