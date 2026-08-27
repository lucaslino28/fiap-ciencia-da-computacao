# Declarando Variaveis
nome = input('Digite seu nome: ')
valor_hora = float(input('Digite o valor da hora trabalhada: '))
qtd_horas = float(input('Digite a quantidade de horas trabalhadas: '))
bonus = float(input('Digite o valor do bonus fixo do mês: '))
desconto = float(input('Digite o valor do desconto total do mês: '))

# Validação de dados
salario_bruto = valor_hora * qtd_horas + bonus
salario_liquido = salario_bruto - desconto

# Saída de dados
print(f'Colaborador: {nome}')
print(f'Salário Bruto: {salario_bruto}')
print(f'Salário Liquido: {salario_liquido}')
