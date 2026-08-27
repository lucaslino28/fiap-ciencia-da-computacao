endpoints = ["/login", "/produtos", "/pedidos"]
status = [
[200, 200, 401, 200, 500],
[200, 200, 200, 200, 200],
[201, 500, 502, 201, 500]
]

# print(endpoints[0])
# print(status[0])

#FUNÇÃO que verifica se UM código http é sucesso ou
# 200 -> True
# 401 -> False
def eh_sucesso(codigo):
    return codigo >= 200 and codigo <= 299

# FUNÇÃO que verifica se tem 2 erros seguidos
# nas requisições de UM endpoint
# [200, 200, 401, 200, 500] --> False
# [201, 500, 502, 201, 500] --> True
def erros_seguidos(requisicoes):
    for i in range(len(requisicoes) - 1):
        codigo_atual = requisicoes[i] # 200
        prox_codigo = requisicoes[i+1] # 200

        if not eh_sucesso(codigo_atual) and not eh_sucesso(prox_codigo):
            return True
    return False

# FUNÇÃO para analisar o endpoint
# [200, 200, 401, 200, 500] --> False
# [201, 500, 502, 201, 500] --> True
def analisar_endpoint(requisicoes):
    qtd_sucesso = 0

    for codigo in requisicoes:
        if eh_sucesso(codigo):
            qtd_sucesso += 1

    qtd_total_req = len(requisicoes)
    qtd_erros = qtd_total_req - qtd_sucesso
    percentual_sucesso = (qtd_sucesso / qtd_total_req) * 100

    tem_erros_seguidos = erros_seguidos(requisicoes)

    if tem_erros_seguidos:
        classificacao = "CRÍTICO"
    elif percentual_sucesso >= 80:
        classificacao = "ESTÁVEL"
    else:
        classificacao = "INSTÁVEL"

    return (qtd_sucesso, qtd_erros, percentual_sucesso, classificacao)

# PERCORRENDO A MATRIZ DE STATUS
maior_qtd_erros = -1
endpoint_maior_erro = ""

for i in range(len(endpoints)):
    nome_endpoint = endpoints[i]
    reqs_endpoint = status[i]

    sucessos, erros, percentual, classificacao = analisar_endpoint(reqs_endpoint)

    print(f"Endpoinr: {nome_endpoint}")
    print(f"Requisições: {reqs_endpoint}")
    print(f"Sucesso: {sucessos}")
    print(f"Erros: {erros}")
    print(f"Percentual: {percentual}")
    print(f"Classificacao: {classificacao}")
    print("-" * 30)
    print()

    if erros > maior_qtd_erros:
        maior_qtd_erros = erros
        endpoint_maior_erro = nome_endpoint

print(f"Endpoint + erros: {endpoint_maior_erro} ({maior_qtd_erros})")