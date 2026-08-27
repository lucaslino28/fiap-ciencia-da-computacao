"""
Converta uma temperatura de Fahrenheit para Celsius. A fórmula de conversão é: Celsius = (Fahrenheit
- 32) * 5/9.
"""

# Definindo a temperatura em Fahrenheit
fahrenheit = int(input("Digite a temperatura em Fahrenheit: "))

# Aplicando a fórmula: C = (F - 32) * 5/9
celsius = (fahrenheit - 32) * 5 / 9

# Exibindo o resultado formatado com duas casas decimais
print(f"{fahrenheit}°F equivale a {celsius:.2f}°C")