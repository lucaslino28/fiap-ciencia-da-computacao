import pandas as pd
import random
from datetime import datetime, timedelta

nomes = ["Ana", "Carlos", "João", "Mariana", "Lucas", "Fernanda", "Pedro", "Juliana", "Rafael", "Beatriz"]
sobrenomes = ["Silva", "Souza", "Oliveira", "Santos", "Lima", "Pereira"]
departamentos = ["TI", "RH", "Financeiro", "Vendas", "Marketing"]
cargos = ["Analista", "Assistente", "Gerente", "Coordenador"]

# Cidades com seus estados corretos
cidades_estados = {
    "São Paulo": "SP",
    "Rio de Janeiro": "RJ",
    "Belo Horizonte": "MG",
    "Curitiba": "PR",
    "Salvador": "BA"
}

def gerar_data():
    inicio = datetime(2015, 1, 1)
    fim = datetime(2023, 12, 31)
    return inicio + timedelta(days=random.randint(0, (fim - inicio).days))

dados = []

for i in range(120):
    nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    idade = random.randint(18, 60)
    salario = round(random.uniform(1500, 12000), 2)
    departamento = random.choice(departamentos)
    cargo = random.choice(cargos)

    cidade = random.choice(list(cidades_estados.keys()))
    estado = cidades_estados[cidade]  # pega o estado correto

    data_contratacao = gerar_data()

    registro = {
        "ID": i + 1,
        "Nome": nome_completo,
        "Idade": idade,
        "Salario": salario,
        "Departamento": departamento,
        "Cargo": cargo,
        "Cidade": cidade,
        "Estado": estado,
        "Data_Contratacao": data_contratacao,
        "Tempo_Empresa_Anos": datetime.now().year - data_contratacao.year,
        "Ativo": random.choice([True, False]),
        "Genero": random.choice(["Masculino", "Feminino"]),
        "Avaliacao": round(random.uniform(0, 10), 1),
        "Numero_Projetos": random.randint(1, 20),
        "Nivel": random.choice(["Junior", "Pleno", "Senior"])
    }

    dados.append(registro)

df = pd.DataFrame(dados)

# Validação
df = df[df["Idade"] >= 18]
df = df[df["Salario"] > 0]
df = df[(df["Avaliacao"] >= 0) & (df["Avaliacao"] <= 10)]
df = df.dropna()

# Exportar Excel
df.to_excel("base_dados_empresa.xlsx", index=False)

# Mostrar no terminal
print("\n PRIMEIROS DADOS:")
print(df.head())

print("\nTotal de registros:", len(df))

print("\n Base de dados criada com sucesso!")