"""Acesso ao banco de dados SQLite.

Conceitos usados: funcoes, listas, tuplas, dicionarios e SQL basico.
"""

import os
import sqlite3

# Banco fica na mesma pasta deste arquivo
PASTA = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO = os.path.join(PASTA, "recargas.db")


def conectar():
    return sqlite3.connect(NOME_BANCO)


def criar_banco():
    """Cria a tabela de sessoes se ela ainda nao existir."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
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
    """)
    conexao.commit()
    conexao.close()


def salvar_sessao(sessao):
    """Salva uma sessao (dicionario) no banco."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO sessoes
        (data_hora, potencia_kw, duracao_minutos, energia_total_kwh,
         energia_solar_kwh, energia_rede_kwh, percentual_renovavel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sessao["data_hora"],
        sessao["potencia_kw"],
        sessao["duracao_minutos"],
        sessao["energia_total_kwh"],
        sessao["energia_solar_kwh"],
        sessao["energia_rede_kwh"],
        sessao["percentual_renovavel"],
    ))
    conexao.commit()
    conexao.close()


def listar_sessoes():
    """Retorna a lista de sessoes (lista de tuplas), da mais nova para a mais antiga."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, data_hora, potencia_kw, duracao_minutos,
               energia_total_kwh, energia_solar_kwh,
               energia_rede_kwh, percentual_renovavel
        FROM sessoes
        ORDER BY id DESC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return linhas


def calcular_resumo():
    """Calcula as estatisticas gerais e retorna um dicionario."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT COUNT(*),
               COALESCE(SUM(energia_total_kwh), 0),
               COALESCE(SUM(energia_solar_kwh), 0),
               COALESCE(SUM(energia_rede_kwh), 0),
               COALESCE(AVG(energia_total_kwh), 0),
               COALESCE(AVG(percentual_renovavel), 0)
        FROM sessoes
    """)
    resultado = cursor.fetchone()
    conexao.close()

    resumo = {
        "total_sessoes": resultado[0],
        "energia_total": round(resultado[1], 2),
        "energia_solar": round(resultado[2], 2),
        "energia_rede": round(resultado[3], 2),
        "consumo_medio": round(resultado[4], 2),
        "percentual_medio": round(resultado[5], 2),
    }
    return resumo
