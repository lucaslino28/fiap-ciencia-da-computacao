import streamlit as st
import datetime
import random

st.set_page_config(page_title="ChargeGrid Sustentável - PoC", layout="wide")

st.title("ChargeGrid Sustentável - Prova de Conceito")
st.subheader("Sprint 2 - Soluções em Energias Renováveis e Sustentáveis")
st.markdown("---")

st.sidebar.header("Parâmetros da Simulação Sustentável")

hora_simulada = st.sidebar.slider("Horário da Simulação (Hora do Dia)", 0, 23, 14)
veiculos_conectados = st.sidebar.number_input("Veículos Elétricos Conectados", min_value=1, max_value=20, value=5)
limite_rede = st.sidebar.slider("Capacidade Máxima da Rede Elétrica (kW)", 20, 150, 70)
geracao_solar_disponivel = st.sidebar.slider("Potência Solar Disponível (kW)", 0, 100, 35)

potencia_nominal_veiculo = 11

demanda_total = veiculos_conectados * potencia_nominal_veiculo

if 18 <= hora_simulada <= 21:
    tipo_tarifa = "Horário de Pico"
    custo_kwh = 1.20
    status_periodo = "Período Crítico"
else:
    tipo_tarifa = "Horário Fora de Pico"
    custo_kwh = 0.45
    status_periodo = "Período Normal"

if demanda_total > limite_rede or status_periodo == "Período Crítico":
    potencia_permitida_por_veiculo = min(
        potencia_nominal_veiculo,
        round(limite_rede / veiculos_conectados, 2)
    )
    decisao_sustentavel = "Modo de Eficiência Ativado: potência limitada para reduzir sobrecarga na rede elétrica."
    status_sustentavel = "Atenção / Otimização Necessária"
else:
    potencia_permitida_por_veiculo = potencia_nominal_veiculo
    decisao_sustentavel = "Operação Sustentável: energia solar aproveitada e recarga mantida em condição eficiente."
    status_sustentavel = "Operação Eficiente"

carga_total_hub = potencia_permitida_por_veiculo * veiculos_conectados

duracao_simulacao_horas = 1

energia_total_kwh = carga_total_hub * duracao_simulacao_horas
energia_solar_utilizada_kwh = min(geracao_solar_disponivel, carga_total_hub) * duracao_simulacao_horas
energia_rede_necessaria_kwh = max(0, energia_total_kwh - energia_solar_utilizada_kwh)

percentual_renovavel = (energia_solar_utilizada_kwh / energia_total_kwh) * 100
economia_estimativa = energia_solar_utilizada_kwh * custo_kwh

st.subheader("Indicadores Energéticos da Estação de Recarga")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Demanda Total dos Veículos", value=f"{demanda_total:.1f} kW")

with col2:
    st.metric(label="Energia Solar Utilizada", value=f"{energia_solar_utilizada_kwh:.1f} kWh")

with col3:
    st.metric(label="Energia da Rede Necessária", value=f"{energia_rede_necessaria_kwh:.1f} kWh")

with col4:
    st.metric(label="Percentual Renovável", value=f"{percentual_renovavel:.1f}%")

st.markdown("---")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(label="Status do Período", value=status_periodo, delta=tipo_tarifa)

with col6:
    st.metric(label="Tarifa Atual", value=f"R$ {custo_kwh:.2f}/kWh")

with col7:
    st.metric(label="Economia Estimada com Solar", value=f"R$ {economia_estimativa:.2f}")

with col8:
    st.metric(label="Carga Total no Hub", value=f"{carga_total_hub:.1f} kW", delta=f"Limite: {limite_rede} kW")

st.markdown("---")

st.subheader("Decisão do Motor Sustentável")

if "Modo de Eficiência Ativado" in decisao_sustentavel:
    st.warning(f"Análise do Sistema: {decisao_sustentavel}")
else:
    st.success(f"Análise do Sistema: {decisao_sustentavel}")

st.info(
    "A prova de conceito simula o uso combinado de energia solar fotovoltaica e rede elétrica. "
    "O objetivo é reduzir a dependência da rede em horários críticos, melhorar a eficiência energética "
    "e priorizar o aproveitamento de energia renovável."
)

st.markdown("---")

st.subheader("Fluxo Energético Simulado")

col_fluxo1, col_fluxo2 = st.columns([2, 1])

with col_fluxo1:
    st.write("Distribuição simulada da energia entre os veículos conectados:")
    for i in range(1, veiculos_conectados + 1):
        soc_atual = random.randint(20, 85)
        energia_origem = "Solar + Rede" if energia_rede_necessaria_kwh > 0 else "100% Solar"
        st.text(
            f"Vaga 0{i} - EV ID: 000{i*12} | Status: Carregando | "
            f"SoC: {soc_atual}% | Potência Recebida: {potencia_permitida_por_veiculo} kW | "
            f"Origem: {energia_origem}"
        )

with col_fluxo2:
    st.write("Logs Técnicos da Simulação:")
    st.code(
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Leitura da potência solar disponível -> {geracao_solar_disponivel} kW\n"
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Cálculo da demanda dos veículos -> {demanda_total} kW\n"
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Energia necessária da rede elétrica -> {energia_rede_necessaria_kwh:.1f} kWh\n"
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Percentual de energia renovável -> {percentual_renovavel:.1f}%\n"
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Status do modo sustentável -> {status_sustentavel}",
        language="text"
    )

st.markdown("---")

st.subheader("Resumo da Sustentabilidade")

st.write(
    f"Nesta simulação, a estação possui {veiculos_conectados} veículos conectados, "
    f"com uma demanda total estimada de {demanda_total:.1f} kW. "
    f"A potência solar disponível é de {geracao_solar_disponivel:.1f} kW. "
    f"Considerando 1 hora de simulação, isso permite utilizar {energia_solar_utilizada_kwh:.1f} kWh de energia renovável. "
    f"Isso representa {percentual_renovavel:.1f}% da demanda atendida por fonte renovável "
    f"e uma economia estimada de R$ {economia_estimativa:.2f} no período simulado."
)

st.caption(
    "ChargeGrid Sustentável - Prova de Conceito v1.0 - "
    "Desenvolvido para a FIAP / Soluções em Energias Renováveis e Sustentáveis / GoodWe."
)