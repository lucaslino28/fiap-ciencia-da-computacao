"""ChargeGrid Simulator - interface Streamlit.

Camada visual apenas. Toda a regra de negocio continua em
simulator.py e todo o armazenamento continua em database.py.
"""

import time

import streamlit as st

import database
import simulator

# Configuracao da pagina
st.set_page_config(page_title="ChargeGrid Simulator", layout="wide")

# Cores da identidade
VERMELHO = "#E30613"

# Fundo da página

st.markdown(f"""
<style>

.stApp {{
    background:
        radial-gradient(
            circle at top right, 
            rgba(227, 6, 19, 0.8),
            transparent 28%),
        ),
        #0B0F14;
        
    color: #F8FAFC;
}}

</style>

""", unsafe_allow_html=True)

# Garante que a tabela existe
database.criar_banco()

# ---------- Estado da aplicacao (simples) ----------
if "ativa" not in st.session_state:
    st.session_state.ativa = False
if "tempo_min" not in st.session_state:
    st.session_state.tempo_min = 0
if "potencia" not in st.session_state:
    st.session_state.potencia = 11.0
if "perc_solar" not in st.session_state:
    st.session_state.perc_solar = 70
if "pontos" not in st.session_state:
    st.session_state.pontos = []
if "ultima_concluida" not in st.session_state:
    st.session_state.ultima_concluida = None

PASSO_MINUTOS = 5      # quantos minutos simulados avancam por tick
INTERVALO_SEG = 0.5    # pausa real entre ticks (tempo acelerado)

# ---------- Sidebar discreta ----------
with st.sidebar:
    st.markdown("### ChargeGrid")
    menu = st.radio("Menu", ["Simulação", "Histórico", "Análise dos Dados"])
    st.markdown("---")
    st.caption("Sprint 3 — FIAP")

# ---------- Topo ----------
st.title("ChargeGrid Simulator")
st.write("Simulação e monitoramento de sessões de recarga com integração de energia solar.")
st.caption("Protótipo acadêmico — FIAP / GoodWe")


# ==================================================
# TELA: SIMULACAO
# ==================================================
def tela_simulacao():
    # Sessao ativa: mostra evolucao em tempo acelerado
    if st.session_state.ativa:
        st.subheader("🔴 RECARGA EM ANDAMENTO")

        # Calcula o estado atual reaproveitando a regra de negocio
        atual = simulator.calcular_sessao(
            st.session_state.potencia,
            st.session_state.tempo_min,
            st.session_state.perc_solar,
        )

        # Metricas (2 linhas x 3 colunas)
        c1, c2, c3 = st.columns(3)
        c1.metric("Tempo Simulado", f"{atual['duracao_minutos']} min")
        c2.metric("Potência", f"{atual['potencia_kw']} kW")
        c3.metric("Energia Total", f"{atual['energia_total_kwh']} kWh")

        c4, c5, c6 = st.columns(3)
        c4.metric("Energia Solar", f"{atual['energia_solar_kwh']} kWh")
        c5.metric("Energia da Rede", f"{atual['energia_rede_kwh']} kWh")
        c6.metric("Energia Renovável", f"{atual['percentual_renovavel']}%")

        # Visualizacao energetica: solar + rede alimentando estacao e veiculo
        with st.container(border=True):
            st.markdown("**Fluxo de energia da sessão**")
            f1, f2, f3 = st.columns(3)
            f1.markdown(f"☀️ **PAINEL SOLAR**\n\n{atual['energia_solar_kwh']} kWh")
            f2.markdown("🔌 **ESTAÇÃO DE RECARGA**\n\n↓ alimenta ↓")
            f3.markdown("🚗 **VEÍCULO ELÉTRICO**\n\n"
                        f"{atual['energia_total_kwh']} kWh recebidos")
            st.write(f"⚡ Rede elétrica complementa com {atual['energia_rede_kwh']} kWh")
            st.progress(atual["percentual_renovavel"] / 100)
            st.caption("Parte da energia vem da geração solar e o restante é "
                       "complementado pela rede.")

        # Um unico grafico: energia acumulada ao longo do tempo
        if len(st.session_state.pontos) > 1:
            st.markdown("**Energia acumulada ao longo do tempo**")
            st.line_chart(
                {
                    "Energia Total": [p["total"] for p in st.session_state.pontos],
                    "Energia Solar": [p["solar"] for p in st.session_state.pontos],
                    "Energia da Rede": [p["rede"] for p in st.session_state.pontos],
                }
            )

        if st.button("FINALIZAR RECARGA"):
            # Calculo final com a mesma funcao + salvamento com a mesma funcao
            final = simulator.calcular_sessao(
                st.session_state.potencia,
                st.session_state.tempo_min,
                st.session_state.perc_solar,
            )
            database.salvar_sessao(final)
            st.session_state.ativa = False
            st.session_state.ultima_concluida = final
            st.rerun()

        # Avanco do tempo acelerado (estavel, sem concorrencia)
        st.session_state.tempo_min += PASSO_MINUTOS
        novo = simulator.calcular_sessao(
            st.session_state.potencia,
            st.session_state.tempo_min,
            st.session_state.perc_solar,
        )
        st.session_state.pontos.append({
            "min": st.session_state.tempo_min,
            "total": novo["energia_total_kwh"],
            "solar": novo["energia_solar_kwh"],
            "rede": novo["energia_rede_kwh"],
        })
        time.sleep(INTERVALO_SEG)
        st.rerun()

    # Recarga concluida: resumo visual com os mesmos dados salvos
    elif st.session_state.ultima_concluida is not None:
        s = st.session_state.ultima_concluida
        st.subheader("✅ RECARGA CONCLUÍDA")
        d1, d2, d3 = st.columns(3)
        d1.metric("Duração", simulator.formatar_duracao(s["duracao_minutos"]))
        d2.metric("Energia Total", f"{s['energia_total_kwh']} kWh")
        d3.metric("Energia Solar", f"{s['energia_solar_kwh']} kWh")
        d4, d5 = st.columns(2)
        d4.metric("Energia da Rede", f"{s['energia_rede_kwh']} kWh")
        d5.metric("Participação Renovável", f"{s['percentual_renovavel']}%")
        if st.button("Nova simulação"):
            st.session_state.ultima_concluida = None
            st.session_state.pontos = []
            st.session_state.tempo_min = 0
            st.rerun()

    # Nenhuma sessao ativa: formulario inicial
    else:
        with st.container(border=True):
            st.markdown("### NOVA SESSÃO DE RECARGA")
            potencia = st.selectbox(
                "Potência do carregador",
                [7.4, 11.0, 22.0],
                index=1,
                format_func=lambda x: f"{x} kW",
            )
            perc = st.slider("Disponibilidade de energia solar (%)", 0, 100, 70)
            if st.button("INICIAR RECARGA"):
                st.session_state.potencia = float(potencia)
                st.session_state.perc_solar = float(perc)
                st.session_state.tempo_min = PASSO_MINUTOS
                primeiro = simulator.calcular_sessao(
                    float(potencia), PASSO_MINUTOS, float(perc)
                )
                st.session_state.pontos = [{
                    "min": PASSO_MINUTOS,
                    "total": primeiro["energia_total_kwh"],
                    "solar": primeiro["energia_solar_kwh"],
                    "rede": primeiro["energia_rede_kwh"],
                }]
                st.session_state.ativa = True
                st.session_state.ultima_concluida = None
                st.rerun()


# ==================================================
# TELA: HISTORICO
# ==================================================
def tela_historico():
    st.subheader("Histórico de Recargas")
    sessoes = database.listar_sessoes()
    if not sessoes:
        st.info("Nenhuma sessão registrada ainda. Inicie uma recarga na aba Simulação.")
        return
    linhas = []
    for s in sessoes:
        linhas.append({
            "ID": s[0],
            "Data": s[1],
            "Potência": f"{s[2]} kW",
            "Duração": simulator.formatar_duracao(s[3]),
            "Energia Total": f"{s[4]:.2f} kWh",
            "Energia Solar": f"{s[5]:.2f} kWh",
            "Energia da Rede": f"{s[6]:.2f} kWh",
            "Renovável %": f"{s[7]:.1f}%",
        })
    st.dataframe(linhas, use_container_width=True)


# ==================================================
# TELA: ANALISE DOS DADOS
# ==================================================
def tela_analise():
    st.subheader("Análise dos Dados")
    r = database.calcular_resumo()
    if r["total_sessoes"] == 0:
        st.info("Sem dados para analisar. Finalize ao menos uma recarga.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Sessões", r["total_sessoes"])
    c2.metric("Energia Consumida", f"{r['energia_total']} kWh")
    c3.metric("Energia Solar", f"{r['energia_solar']} kWh")
    c4.metric("Energia da Rede", f"{r['energia_rede']} kWh")

    c5, c6 = st.columns(2)
    c5.metric("Participação Renovável", f"{r['percentual_medio']}%")
    c6.metric("Consumo Médio por Sessão", f"{r['consumo_medio']} kWh")

    # Um unico grafico: solar x rede (totais reais do banco)
    st.markdown("**Energia Solar x Energia da Rede (totais)**")
    st.bar_chart({"Energia Solar": [r["energia_solar"]], "Energia da Rede": [r["energia_rede"]]})
    st.caption("Solar x Rede — fonte: dados calculados pelo próprio sistema.")


# ---------- Roteamento simples ----------
if menu == "Simulação":
    tela_simulacao()
elif menu == "Histórico":
    tela_historico()
else:
    tela_analise()
