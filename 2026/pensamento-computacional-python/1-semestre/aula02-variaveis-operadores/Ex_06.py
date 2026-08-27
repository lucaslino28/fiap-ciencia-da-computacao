"""
Leia 2 valores A e B, que correspondem a 2 notas de um aluno. A seguir calcule e informe a média
aritmética do aluno.
"""

# Lendo os valores (usamos float para permitir notas com vírgula, como 7.5))
nota_a = float(input("Digite a primeira nota: "))
nota_b = float(input("Digite a segunda nota: "))

# Cálculo da média aritmética
media = (nota_a + nota_b) / 2

# Exibindo o resultado
print(f"A média do aluno é: {media:.1f}")