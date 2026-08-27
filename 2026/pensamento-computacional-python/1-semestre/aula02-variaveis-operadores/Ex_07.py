"""
Leia 2 valores A e B, que correspondem a 2 notas de um aluno. A seguir calcule e informe a média
ponderada do aluno, sabendo que a nota A tem peso 4 e a nota B tem peso 6.
Exemplo: nota a * 4 e nota b * 6.
"""

# Lendo as notas
nota_a = float(input("Digite a nota A: "))
nota_b = float(input("Digite a nota B: "))

# Definindo os pesos
peso_a = 4
peso_b = 6

# Cálculo da média ponderada
# Multiplicamos as notas pelos pesos e dividimos pela soma dos pesos (10)
media_ponderada = ((nota_a * peso_a) + (nota_b * peso_b)) / (peso_a + peso_b)

# Exibindo o resultado
print(f"A média ponderada do aluno é: {media_ponderada:.1f}")