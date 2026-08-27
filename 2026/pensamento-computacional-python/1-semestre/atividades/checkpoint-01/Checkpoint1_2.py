# Declarando variaveis
nome_produto = input("Digite o nome do produto: ")
preco_unitario = float(input("Digite o preço unitário: "))
quantidade = int(input("Digite a quantidade de itens: "))
percentual_desconto = float(input("Digite o percentual de desconto: "))

# validação de dados
valor_bruto = preco_unitario * quantidade
valor_total = valor_bruto - percentual_desconto

# saída de dados
print(f"Produto: {nome_produto}")
print(f'Valor Bruto: {valor_bruto}')
print(f'Desconto: {percentual_desconto}')
print(f'Valor Final: {valor_total}')