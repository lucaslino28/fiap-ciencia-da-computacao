"""
▪ Crie um programa que receba o valor do produto e valor pago.
▪ Calcule o troco a ser pago.
▪ O valor do troco deve ser exibido no terminal.
"""

# Entrada de dados
valor_produto = float(input("Digite o valor do produto: R$ "))
valor_pago = float(input("Digite o valor pago pelo cliente: R$ "))

# Cálculo do troco
troco = valor_pago - valor_produto

# Verificação e exibição do resultado
if troco < 0:
    falta = abs(troco)
    print(f"Valor insuficiente! Faltam R$ {falta:.2f}")
elif troco == 0:
    print("Valor exato. Não há troco.")
else:
    print(f"O valor do troco a ser pago é: R$ {troco:.2f}")