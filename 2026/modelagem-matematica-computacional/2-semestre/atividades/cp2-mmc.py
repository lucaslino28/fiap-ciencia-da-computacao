# CP2 - Modelagem Matemática e Computacional
# Sistemas de Recomendação e Álgebra Linear

u1 = [5, 1, 4]
u2 = [4, 1, 5]
u3 = [1, 5, 2]
u4 = [1, 4, 1]
u5 = [4, 2, 3]


def produto_escalar(vetor1, vetor2):
    resultado = 0

    for i in range(len(vetor1)):
        resultado += vetor1[i] * vetor2[i]

    return resultado


resultado_u1 = produto_escalar(u5, u1)
resultado_u2 = produto_escalar(u5, u2)
resultado_u3 = produto_escalar(u5, u3)
resultado_u4 = produto_escalar(u5, u4)

print("U5 x U1 =", resultado_u1)
print("U5 x U2 =", resultado_u2)
print("U5 x U3 =", resultado_u3)
print("U5 x U4 =", resultado_u4)


similaridades = {
    "U1": resultado_u1,
    "U2": resultado_u2,
    "U3": resultado_u3,
    "U4": resultado_u4
}

usuario_mais_semelhante = max(similaridades, key=similaridades.get)

print()
print("Usuário mais semelhante ao U5:", usuario_mais_semelhante)
print("Produto escalar:", similaridades[usuario_mais_semelhante])