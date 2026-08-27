"""
Você comprou 3 livros por R$ 25 cada e 2 canetas por R$ 5 cada. Calcule o total gasto.
"""

# Declarando Valores
Qtd_Livro = 3
Val_Livro = 25
Qtd_caneta = 2
Val_Caneta = 5

# Calculo de compra
Total_Livro = Val_Livro * Qtd_Livro
print(f"Total gasto em livros R$ {Total_Livro}")

Total_Caneta = Val_Caneta * Qtd_caneta
print(f"Total gasto em canetas R$ {Total_Caneta}")

Total_Gasto = Total_Livro + Total_Caneta
print(f'O total gasto da compra R$ {Total_Gasto}')
