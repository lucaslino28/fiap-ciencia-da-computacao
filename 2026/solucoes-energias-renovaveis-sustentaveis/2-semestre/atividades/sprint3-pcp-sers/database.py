"""Acesso ao banco de dados SQLite.

Responsável por:
- criar o banco;
- salvar sessões;
- listar sessões;
- calcular indicadores gerais.
"""

import os
import sqlite3

# CONFIGURAÇÃO DO BANCO
PASTA = os.path.dirname(os.path.abspath(__file__))

NOME_BANCO = os.path.join(
    PASTA,
    "recargas.db"
)

# CONEXÃO
def conectar():
    return sqlite3.connect(NOME_BANCO)

# CRIAÇÃO DO BANCO
def criar_banco():
    """Cria a tabela e adiciona campos novos sem apagar registros antigos."""

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            potencia_kw REAL NOT NULL,
            duracao_minutos INTEGER NOT NULL,
            energia_total_kwh REAL NOT NULL,
            energia_solar_kwh REAL NOT NULL,
            energia_rede_kwh REAL NOT NULL,
            percentual_renovavel REAL NOT NULL
        )
        """
    )

    cursor.execute("PRAGMA table_info(sessoes)")
    colunas_existentes = {coluna[1] for coluna in cursor.fetchall()}
    colunas_adicionais = {
        "modelo_carregador": "TEXT",
        "capacidade_bateria_kwh": "REAL",
        "soc_inicial": "REAL",
        "soc_final": "REAL",
        "energia_bateria_kwh": "REAL",
        "perdas_kwh": "REAL",
        "custo_estimado": "REAL",
    }

    for nome, tipo in colunas_adicionais.items():
        if nome not in colunas_existentes:
            cursor.execute(f"ALTER TABLE sessoes ADD COLUMN {nome} {tipo}")

    conexao.commit()

    conexao.close()

# SALVAR SESSÃO
def salvar_sessao(sessao):
    """Salva uma sessão de recarga no banco."""

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO sessoes (
            data_hora,
            potencia_kw,
            duracao_minutos,
            energia_total_kwh,
            energia_solar_kwh,
            energia_rede_kwh,
            percentual_renovavel,
            modelo_carregador,
            capacidade_bateria_kwh,
            soc_inicial,
            soc_final,
            energia_bateria_kwh,
            perdas_kwh,
            custo_estimado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sessao["data_hora"],
            sessao["potencia_kw"],
            sessao["duracao_minutos"],
            sessao["energia_total_kwh"],
            sessao["energia_solar_kwh"],
            sessao["energia_rede_kwh"],
            sessao["percentual_renovavel"],
            sessao.get("modelo_carregador"),
            sessao.get("capacidade_bateria_kwh"),
            sessao.get("soc_inicial"),
            sessao.get("soc_atual"),
            sessao.get("energia_bateria_kwh"),
            sessao.get("perdas_kwh"),
            sessao.get("custo_estimado")
        )
    )

    conexao.commit()

    conexao.close()

# LISTAR SESSÕES
def listar_sessoes():
    """Retorna as sessões da mais recente para a mais antiga."""

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            data_hora,
            potencia_kw,
            duracao_minutos,
            energia_total_kwh,
            energia_solar_kwh,
            energia_rede_kwh,
            percentual_renovavel,
            modelo_carregador,
            capacidade_bateria_kwh,
            soc_inicial,
            soc_final,
            energia_bateria_kwh,
            perdas_kwh,
            custo_estimado
        FROM sessoes
        ORDER BY id DESC
        """
    )

    sessoes = cursor.fetchall()

    conexao.close()

    return sessoes

# RESUMO DOS DADOS
def calcular_resumo():
    """Calcula os principais indicadores das sessões."""

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),
            COALESCE(SUM(energia_total_kwh), 0),
            COALESCE(SUM(energia_solar_kwh), 0),
            COALESCE(SUM(energia_rede_kwh), 0),
            COALESCE(AVG(energia_total_kwh), 0)
        FROM sessoes
        """
    )

    resultado = cursor.fetchone()

    conexao.close()

    total_sessoes = resultado[0]

    energia_total = resultado[1]

    energia_solar = resultado[2]

    energia_rede = resultado[3]

    consumo_medio = resultado[4]


    # Participação renovável geral
    if energia_total > 0:

        percentual_renovavel = (
            energia_solar
            / energia_total
        ) * 100

    else:

        percentual_renovavel = 0


    resumo = {
        "total_sessoes": total_sessoes,

        "energia_total": round(
            energia_total,
            2
        ),

        "energia_solar": round(
            energia_solar,
            2
        ),

        "energia_rede": round(
            energia_rede,
            2
        ),

        "consumo_medio": round(
            consumo_medio,
            2
        ),

        "percentual_medio": round(
            percentual_renovavel,
            2
        )
    }

    return resumo