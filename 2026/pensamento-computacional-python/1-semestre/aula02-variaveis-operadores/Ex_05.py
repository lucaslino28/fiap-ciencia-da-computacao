"""
Um carro percorreu 150 km a uma velocidade média de 60 km/h. Quanto tempo (em horas) o carro
levou para percorrer essa distância?
"""

distancia = 150
velocidade_media = 60

# Cálculo do tempo total em decimal (2.5)
tempo_decimal = distancia / velocidade_media

# Pegando a parte inteira (horas)
horas = int(tempo_decimal)

# Convertendo o que sobrou (0.5) em minutos
# Multiplicamos a sobra por 60
minutos = int((tempo_decimal - horas) * 60)

print(f"O carro levou {horas} horas e {minutos} minutos.")