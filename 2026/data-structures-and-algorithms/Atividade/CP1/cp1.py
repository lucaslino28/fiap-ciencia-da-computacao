"""
AVALIAÇÃO - PARTE PRÁTICA
Central de Triagem Orbital - Versão A - Bubble Sort
"""

# ------------------------------------------------------------------
# Base de dados (vetor estático obrigatório)
# ------------------------------------------------------------------
containers_A = [
    482, 173, 905, 241, 667, 318, 754, 126, 590, 433, 812, 205, 691, 347,
    978, 154, 526, 739, 284, 861,
    615, 92, 447, 830, 271, 704, 358, 999, 116, 563, 790, 225, 648, 401,
    876, 139, 512, 733, 296, 944,
    187, 620, 455, 808, 332, 571, 14, 684, 253, 917, 365, 742, 198, 536,
    889, 307, 651, 420, 773, 105,
    598, 246, 934, 381, 719, 160, 547, 825, 293, 672, 438, 981, 121, 504,
    756, 339, 690, 214, 867, 475,
    928, 146, 583, 261, 714, 396, 845, 72, 631, 287, 960, 518, 352, 799,
    183, 606, 449, 874, 235, 697,
    323, 910, 167, 552, 781, 409, 995, 128, 644, 274, 835, 491, 759, 203,
    576, 341, 888, 64, 622, 457,
    936, 312, 705, 149, 539, 820, 266, 681, 427, 973, 111, 594, 748, 384,
    862, 229, 517, 301, 793, 176,
    655, 470, 921, 137, 568, 245, 730, 414, 856, 98, 609, 286, 947, 361,
    712, 194, 525, 804, 257, 678,
    443, 986, 119, 591, 764, 335, 841, 208, 549, 392, 913, 155, 632, 278,
    725, 461, 870, 83, 603, 319,
    958, 171, 557, 240, 699, 406, 823, 132, 586, 270, 932, 375, 716, 201,
    531, 788, 349, 663, 454, 902
]

# ------------------------------------------------------------------
# Missão 1 - Diagnóstico da carga (0,5 ponto)
# ------------------------------------------------------------------
def analisar_carga(lista):
    """
    Determina quantidade, menor código e maior código da lista.
    Não usa min(), max(), sort() ou sorted().
    """
    quantidade = 0
    menor = lista[0]
    maior = lista[0]

    for codigo in lista:
        quantidade += 1
        if codigo < menor:
            menor = codigo
        if codigo > maior:
            maior = codigo

    return quantidade, menor, maior

# ------------------------------------------------------------------
# Missão 2 - Localização de emergência (1,0 ponto)
# ------------------------------------------------------------------
def busca_linear(lista, codigo):
    """
    Busca sequencial sobre a lista original (desordenada).
    Retorna (posicao, comparacoes).
    Se não encontrar, retorna (-1, comparacoes).
    Conta uma comparação a cada elemento verificado contra o código.
    """
    comparacoes = 0

    for posicao in range(len(lista)):
        comparacoes += 1
        if lista[posicao] == codigo:
            return posicao, comparacoes

    return -1, comparacoes

# ------------------------------------------------------------------
# Missão 3 - Bubble Sort (2,5 pontos)
# ------------------------------------------------------------------
def ordenar(lista):
    """
    Ordena a lista usando Bubble Sort.
    Conta uma comparação a cada comparação relevante entre valores e
    uma movimentação a cada troca efetivamente realizada.
    Retorna (lista_ordenada, comparacoes, movimentacoes).
    """
    lista_ordenada = lista[:]  # preserva o vetor original recebido
    n = len(lista_ordenada)
    comparacoes = 0
    movimentacoes = 0

    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            comparacoes += 1
            if lista_ordenada[j] > lista_ordenada[j + 1]:
                lista_ordenada[j], lista_ordenada[j + 1] = (
                    lista_ordenada[j + 1],
                    lista_ordenada[j],
                )
                movimentacoes += 1
                trocou = True
        if not trocou:
            # lista já está ordenada, não há mais o que comparar
            break

    return lista_ordenada, comparacoes, movimentacoes

# ------------------------------------------------------------------
# Missão 4 - Busca otimizada (1,5 ponto)
# ------------------------------------------------------------------
def busca_binaria(lista, codigo):
    """
    Busca binária sobre uma lista ORDENADA.
    Retorna (posicao, comparacoes).
    Se não encontrar, retorna (-1, comparacoes).

    Critério de contagem: cada verificação do elemento do meio contra o
    código procurado (lista[meio] == codigo) conta como UMA comparação,
    independente de o resultado levar à busca na metade esquerda ou
    direita.
    """
    comparacoes = 0
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        if lista[meio] == codigo:
            return meio, comparacoes
        elif lista[meio] < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1, comparacoes


# ------------------------------------------------------------------
# Missão 5 - Relatório da estação (0,5 ponto) + testes
# ------------------------------------------------------------------
if __name__ == "__main__":
    # ---------- Missão 1 ----------
    quantidade, menor, maior = analisar_carga(containers_A)

    # ---------- Missão 3 (ordenação, preservando o vetor original) ----------
    ordenada, comparacoes_ordenacao, movimentacoes = ordenar(containers_A[:])

    # ---------- Código usado nas Missões 2, 4 e 5 ----------
    # Código existente (presente no vetor) para demonstrar sucesso na busca
    codigo_existente = 482
    # Código inexistente para demonstrar busca sem sucesso
    codigo_inexistente = 1000

    print("Teste com código existente:", codigo_existente)
    pos_linear, comp_linear = busca_linear(containers_A, codigo_existente)
    pos_binaria, comp_binaria = busca_binaria(ordenada, codigo_existente)
    print(f"  Busca Linear  -> posição: {pos_linear} | comparações: {comp_linear}")
    print(f"  Busca Binária -> posição: {pos_binaria} | comparações: {comp_binaria}")

    print("\nTeste com código inexistente:", codigo_inexistente)
    pos_linear_ne, comp_linear_ne = busca_linear(containers_A, codigo_inexistente)
    pos_binaria_ne, comp_binaria_ne = busca_binaria(ordenada, codigo_inexistente)
    print(f"  Busca Linear  -> posição: {pos_linear_ne} | comparações: {comp_linear_ne}")
    print(f"  Busca Binária -> posição: {pos_binaria_ne} | comparações: {comp_binaria_ne}")

    # Código usado no relatório final (mesmo código nas duas buscas, como pede o enunciado)
    codigo_relatorio = codigo_existente
    pos_linear_rel, comp_linear_rel = busca_linear(containers_A, codigo_relatorio)
    pos_binaria_rel, comp_binaria_rel = busca_binaria(ordenada, codigo_relatorio)

    print("\n========== CENTRAL DE TRIAGEM ==========")
    print(f"Quantidade de contêineres: {quantidade}")
    print(f"Menor código: {menor}")
    print(f"Maior código: {maior}")
    print()
    print("---------- ORDENAÇÃO ----------")
    print("Algoritmo: Bubble Sort")
    print(f"Comparações: {comparacoes_ordenacao}")
    print(f"Movimentações: {movimentacoes}")
    print()
    print("---------- BUSCAS ----------")
    print(f"Código procurado: {codigo_relatorio}")
    print(f"Busca Linear - Posição: {pos_linear_rel} | Comparações: {comp_linear_rel}")
    print(f"Busca Binária - Posição: {pos_binaria_rel} | Comparações: {comp_binaria_rel}")
    print("========================================")