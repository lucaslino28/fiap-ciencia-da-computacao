"""ChargeGrid Simulator - interface Streamlit.

Camada visual da aplicação. A regra de negócio continua em simulator.py
e o armazenamento continua em database.py.
"""

import base64
import time
from pathlib import Path

import pandas as pd
import streamlit as st

import database
import simulator


# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="ChargeGrid Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",
)


# ==================================================
# IDENTIDADE VISUAL
# ==================================================

FIAP = "#ED145B"
GOODWE = "#E84A36"
VERMELHO = FIAP
FUNDO = "#090C10"
CARD = "#11161D"
BORDA = "#28313D"
TEXTO = "#F4F6F8"
TEXTO_SECUNDARIO = "#A3ACB8"
SOLAR = "#F5A623"
REDE = "#6EA8FE"

LOGO_GOODWE = Path(__file__).resolve().parent / "assets" / "goodwe-logo.png"
GOODWE_LOGO_URI = (
    "data:image/png;base64,"
    + base64.b64encode(LOGO_GOODWE.read_bytes()).decode("ascii")
)


st.markdown(
    f"""<style>
/* BASE */
:root {{ color-scheme: dark; }}
.stApp {{ background: linear-gradient(180deg, #0B0E13 0%, {FUNDO} 100%); color: {TEXTO}; }}
.block-container {{ max-width: 1240px; padding-top: 1.6rem; padding-bottom: 3rem; }}
[data-testid="stMainBlockContainer"] > div {{ gap: 0.9rem; }}
hr {{ border-color: {BORDA} !important; }}

/* TIPOGRAFIA */
h1, h2, h3 {{ color: {TEXTO} !important; font-weight: 700 !important; letter-spacing: 0 !important; }}
p, label {{ color: {TEXTO_SECUNDARIO}; }}
[data-testid="stCaptionContainer"] {{ color: #8993A1; }}
.screen-title {{ color: {TEXTO}; font-size: 1.45rem; font-weight: 750; line-height: 1.25; margin: 0 0 0.2rem; }}
.screen-copy {{ color: {TEXTO_SECUNDARIO}; font-size: 0.92rem; margin: 0 0 1.1rem; }}
.section-title {{ color: {TEXTO}; font-size: 1rem; font-weight: 700; margin: 0.25rem 0 0.8rem; }}
.section-kicker {{ color: {VERMELHO}; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; margin-bottom: 0.25rem; }}

/* SIDEBAR */
[data-testid="stSidebar"] {{ background: #0D1117; border-right: 1px solid {BORDA}; }}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ padding-top: 1rem; }}
.sidebar-brand {{ border-bottom: 1px solid {BORDA}; padding: 0.25rem 0 1.1rem; margin-bottom: 1rem; }}
.sidebar-brand__eyebrow {{ color: {FIAP}; font-size: 0.66rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; margin-bottom: 0.35rem; }}
.sidebar-brand__name {{ color: #FFFFFF; font-size: 1.3rem; font-weight: 800; }}
.sidebar-brand__mark {{ color: {GOODWE}; margin-right: 0.35rem; }}
.sidebar-brand__copy {{ color: #8993A1; font-size: 0.78rem; margin-top: 0.3rem; }}
.sidebar-nav-label {{ color: #687382; font-size: 0.64rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; margin: 0 0 0.5rem 0.25rem; }}
[data-testid="stSidebar"] [data-testid="stRadio"] > label {{ display: none; }}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{ gap: 0.35rem; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"] {{ position: relative; overflow: hidden; width: 100%; border: 1px solid transparent; border-radius: 8px; padding: 0.72rem 0.78rem; transition: background 0.15s ease, border-color 0.15s ease; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div {{ width: 100%; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child {{ display: none !important; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"] p {{ color: #A8B1BD; font-size: 0.84rem; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover {{ background: #151B23; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] {{ background: rgba(237, 20, 91, 0.12); border-color: rgba(237, 20, 91, 0.48); }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"]::before {{ content: ""; position: absolute; inset: 0 auto 0 0; width: 3px; background: {FIAP}; }}
[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] p {{ color: #FFFFFF; font-weight: 700; }}
.sidebar-partner {{ background: #121820; border: 1px solid {BORDA}; border-radius: 8px; margin-top: 1.25rem; padding: 0.9rem 1rem; }}
.sidebar-partner__label {{ color: #6F7A88; font-size: 0.62rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; }}
.sidebar-partner__logo {{ display: block; width: 132px; max-width: 100%; height: auto; margin: 0.6rem 0 0.45rem; }}
.sidebar-partner__copy {{ color: #8F99A7; font-size: 0.7rem; line-height: 1.45; }}
.sidebar-footer {{ border-top: 1px solid {BORDA}; margin-top: 1rem; padding-top: 0.9rem; }}
.sidebar-footer__label {{ color: #687382; font-size: 0.62rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; }}
.sidebar-footer__title {{ color: #DCE1E7; font-size: 0.78rem; font-weight: 700; margin-top: 0.25rem; }}
.sidebar-footer__copy {{ color: #687382; font-size: 0.7rem; margin-top: 0.15rem; }}

/* CONTAINERS */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {{ background: {CARD}; border: 1px solid {BORDA} !important; border-radius: 8px; padding: 0.55rem; }}

/* MÉTRICAS */
[data-testid="stMetric"] {{ background: {CARD}; border: 1px solid {BORDA}; border-radius: 8px; padding: 1rem 1.1rem; min-height: 112px; box-shadow: inset 0 2px 0 {FIAP}; }}
[data-testid="stMetricLabel"] p {{ color: #9AA4B1; font-size: 0.82rem; }}
[data-testid="stMetricValue"] {{ color: #FFFFFF; font-weight: 750; }}
[data-testid="stMetricDelta"] {{ color: {TEXTO_SECUNDARIO}; }}

/* BOTÕES */
div.stButton > button {{ background: {FIAP}; color: #FFFFFF; font-weight: 750; border: 1px solid {FIAP}; border-radius: 8px; min-height: 46px; padding: 0.7rem 1.4rem; transition: background 0.15s ease, border-color 0.15s ease; }}
div.stButton > button:hover {{ background: #FF286E; color: #FFFFFF; border-color: #FF286E; }}
div.stButton > button:focus {{ box-shadow: 0 0 0 3px rgba(237, 20, 91, 0.24); }}

/* INPUTS */
[data-baseweb="select"] > div {{ background-color: #171D25 !important; border-color: #333D4A !important; border-radius: 8px !important; }}
[data-baseweb="select"] * {{ color: {TEXTO} !important; }}
[data-testid="stSlider"] {{ padding: 0.2rem 0 0.55rem; }}
[data-testid="stSlider"] [role="slider"] {{ background-color: {VERMELHO}; border-color: {VERMELHO}; }}
[data-testid="stProgress"] > div > div > div {{ background-color: {SOLAR}; }}

/* TABELAS */
[data-testid="stDataFrame"] {{ border: 1px solid {BORDA}; border-radius: 8px; overflow: hidden; }}

/* CLASSES PERSONALIZADAS */
.hero {{ position: relative; overflow: hidden; background: linear-gradient(115deg, rgba(237, 20, 91, 0.18) 0%, rgba(17, 22, 29, 0.98) 46%, rgba(232, 74, 54, 0.10) 100%); border: 1px solid #38414D; border-radius: 8px; padding: 1.65rem 1.75rem; margin-bottom: 1.3rem; }}
.hero::before {{ content: ""; position: absolute; inset: 0 auto 0 0; width: 4px; background: linear-gradient(180deg, {FIAP}, {GOODWE}); }}
.hero__eyebrow {{ color: #FF6F9E; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; margin-bottom: 0.45rem; }}
.hero__title {{ color: #FFFFFF; font-size: 2rem; font-weight: 800; line-height: 1.15; margin: 0; }}
.hero__subtitle {{ color: #B5BEC9; font-size: 0.96rem; line-height: 1.55; max-width: 720px; margin-top: 0.55rem; }}
.hero__scope {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); max-width: 760px; border-top: 1px solid rgba(255,255,255,0.10); border-bottom: 1px solid rgba(255,255,255,0.10); margin-top: 1.15rem; padding: 0.8rem 0; }}
.hero__scope-item {{ display: grid; grid-template-columns: auto 1fr; column-gap: 0.55rem; padding: 0 1rem; border-right: 1px solid rgba(255,255,255,0.10); }}
.hero__scope-item:first-child {{ padding-left: 0; }}
.hero__scope-item:last-child {{ border-right: 0; }}
.hero__scope-icon {{ grid-row: span 2; font-size: 1.1rem; align-self: center; }}
.hero__scope-label {{ color: #8F99A7; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0; }}
.hero__scope-value {{ color: #FFFFFF; font-size: 0.82rem; font-weight: 700; margin-top: 0.08rem; }}
.hero__badges {{ display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.9rem; }}
.badge {{ display: inline-flex; align-items: center; background: rgba(255,255,255,0.04); border: 1px solid #3A4451; color: #D4DAE1; border-radius: 999px; padding: 0.28rem 0.65rem; font-size: 0.72rem; font-weight: 650; }}
.badge--fiap {{ border-color: rgba(237, 20, 91, 0.55); color: #FF8BB2; }}
.badge--goodwe {{ border-color: rgba(232, 74, 54, 0.55); color: #FF9C87; }}
.status {{ display: inline-flex; align-items: center; gap: 0.45rem; border-radius: 999px; padding: 0.42rem 0.72rem; font-weight: 750; font-size: 0.76rem; }}
.status--live {{ background: rgba(237, 20, 91, 0.10); color: #FF7EAA; border: 1px solid rgba(237, 20, 91, 0.40); }}
.status--success {{ background: rgba(56, 201, 118, 0.1); color: #63DF99; border: 1px solid rgba(56, 201, 118, 0.35); }}
.status__dot {{ width: 7px; height: 7px; border-radius: 50%; background: currentColor; }}
.config-summary {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; border-top: 1px solid {BORDA}; margin-top: 0.55rem; padding-top: 1rem; }}
.config-summary__item {{ padding: 0 1rem; border-right: 1px solid {BORDA}; }}
.config-summary__item:first-child {{ padding-left: 0; }}
.config-summary__item:last-child {{ border-right: 0; }}
.config-summary__label {{ color: #8792A0; font-size: 0.74rem; margin-bottom: 0.2rem; }}
.config-summary__value {{ color: #FFFFFF; font-size: 1rem; font-weight: 750; }}
.config-summary__value--solar {{ color: {SOLAR}; }}
.config-summary__value--grid {{ color: {REDE}; }}
.energy-card {{ background: {CARD}; border: 1px solid {BORDA}; border-radius: 8px; padding: 1rem; min-height: 142px; text-align: left; position: relative; overflow: hidden; }}
.energy-card::before {{ content: ""; position: absolute; inset: 0 0 auto 0; height: 2px; background: var(--energy-accent); }}
.energy-card--solar {{ --energy-accent: {SOLAR}; }}
.energy-card--station {{ --energy-accent: {GOODWE}; }}
.energy-card--vehicle {{ --energy-accent: #D8DEE7; }}
.energy-card__icon {{ font-size: 1.55rem; margin-bottom: 0.65rem; }}
.energy-card__title {{ color: #98A2AF; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0; }}
.energy-card__value {{ color: #FFFFFF; font-size: 1.25rem; font-weight: 750; margin-top: 0.3rem; }}
.energy-card__meta {{ color: #75808E; font-size: 0.72rem; margin-top: 0.25rem; }}
.network-note {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; background: rgba(110, 168, 254, 0.07); border: 1px solid rgba(110, 168, 254, 0.28); border-radius: 8px; padding: 0.8rem 1rem; margin-top: 0.7rem; }}
.network-note__label {{ color: #A9BFE2; font-size: 0.78rem; }}
.network-note__value {{ color: {REDE}; font-size: 0.95rem; font-weight: 750; white-space: nowrap; }}

/* ANÁLISE DE DADOS */
.analysis-context {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; background: #0E141B; border: 1px solid {BORDA}; border-left: 3px solid {GOODWE}; border-radius: 8px; padding: 0.72rem 0.9rem; margin: 0.15rem 0 1rem; }}
.analysis-context__status {{ display: flex; align-items: center; gap: 0.5rem; color: #E7EBF0; font-size: 0.8rem; font-weight: 700; }}
.analysis-context__dot {{ width: 7px; height: 7px; border-radius: 50%; background: #43D17D; box-shadow: 0 0 0 4px rgba(67, 209, 125, 0.10); }}
.analysis-context__meta {{ color: #7F8A98; font-size: 0.74rem; text-align: right; }}
.analytics-kpis {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; margin-bottom: 1.25rem; }}
.analytics-kpi {{ --kpi-accent: {FIAP}; position: relative; overflow: hidden; background: {CARD}; border: 1px solid {BORDA}; border-radius: 8px; padding: 1rem 1.05rem; min-height: 128px; }}
.analytics-kpi::before {{ content: ""; position: absolute; inset: 0 0 auto 0; height: 3px; background: var(--kpi-accent); }}
.analytics-kpi--goodwe {{ --kpi-accent: {GOODWE}; }}
.analytics-kpi--solar {{ --kpi-accent: {SOLAR}; }}
.analytics-kpi--green {{ --kpi-accent: #43D17D; }}
.analytics-kpi__head {{ display: flex; align-items: center; justify-content: space-between; color: #8D98A6; font-size: 0.74rem; }}
.analytics-kpi__icon {{ display: grid; place-items: center; width: 28px; height: 28px; background: rgba(255,255,255,0.04); border: 1px solid #2A3440; border-radius: 6px; font-size: 0.85rem; }}
.analytics-kpi__value {{ color: #FFFFFF; font-size: 1.55rem; font-weight: 800; line-height: 1.15; margin-top: 0.62rem; }}
.analytics-kpi__meta {{ color: #727E8C; font-size: 0.7rem; margin-top: 0.3rem; }}
[data-testid="stTabs"] [data-baseweb="tab-list"] {{ gap: 0.38rem; background: #0D1218; border: 1px solid {BORDA}; border-radius: 8px; padding: 0.35rem; margin-bottom: 0.8rem; overflow-x: auto; }}
[data-testid="stTabs"] button[data-baseweb="tab"] {{ min-height: 42px; height: auto; border-radius: 6px; padding: 0.58rem 0.85rem; }}
[data-testid="stTabs"] button[data-baseweb="tab"] p {{ color: #8E99A7; font-size: 0.78rem; font-weight: 700; white-space: nowrap; }}
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {{ background: rgba(237, 20, 91, 0.14); }}
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] p {{ color: #FFFFFF; }}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{ display: none; }}
.dashboard-title {{ color: #FFFFFF; font-size: 1rem; font-weight: 750; margin: 0.1rem 0 0.2rem; }}
.dashboard-copy {{ color: #7F8A98; font-size: 0.76rem; margin-bottom: 0.8rem; }}
.energy-mix {{ padding: 0.2rem 0 0.35rem; }}
.energy-mix__totals {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; margin: 1rem 0 0.65rem; }}
.energy-mix__total-label {{ color: #7F8A98; font-size: 0.7rem; text-transform: uppercase; }}
.energy-mix__total-value {{ color: #FFFFFF; font-size: 1.35rem; font-weight: 800; margin-top: 0.15rem; }}
.energy-mix__renewable {{ color: #43D17D; font-size: 0.82rem; font-weight: 750; }}
.energy-mix__bar {{ display: flex; overflow: hidden; height: 18px; background: #1A222C; border: 1px solid #303A46; border-radius: 5px; }}
.energy-mix__solar {{ background: {SOLAR}; min-width: 2px; }}
.energy-mix__grid {{ background: {REDE}; min-width: 2px; }}
.energy-mix__legend {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.8rem; margin-top: 0.85rem; }}
.energy-mix__legend-item {{ display: grid; grid-template-columns: auto 1fr; column-gap: 0.5rem; align-items: center; }}
.energy-mix__swatch {{ width: 9px; height: 9px; border-radius: 2px; }}
.energy-mix__swatch--solar {{ background: {SOLAR}; }}
.energy-mix__swatch--grid {{ background: {REDE}; }}
.energy-mix__legend-label {{ color: #8994A2; font-size: 0.7rem; }}
.energy-mix__legend-value {{ color: #FFFFFF; font-size: 0.85rem; font-weight: 750; }}
.profile-list {{ margin-top: 0.55rem; }}
.profile-row {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; border-bottom: 1px solid #242D38; padding: 0.66rem 0; }}
.profile-row:last-child {{ border-bottom: 0; }}
.profile-row__label {{ color: #8994A2; font-size: 0.75rem; }}
.profile-row__value {{ color: #F4F6F8; font-size: 0.82rem; font-weight: 750; text-align: right; }}
.analysis-insight {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; background: rgba(67, 209, 125, 0.07); border: 1px solid rgba(67, 209, 125, 0.26); border-radius: 8px; padding: 0.8rem 0.95rem; margin-top: 0.75rem; }}
.analysis-insight__label {{ color: #62DC97; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; }}
.analysis-insight__text {{ color: #C9D3DD; font-size: 0.76rem; margin-top: 0.18rem; }}
.analysis-insight__value {{ color: #FFFFFF; font-size: 0.9rem; font-weight: 800; white-space: nowrap; }}
.source-gauge {{ display: grid; place-items: center; width: 210px; height: 210px; max-width: 100%; aspect-ratio: 1; border-radius: 50%; margin: 0.75rem auto; background: conic-gradient({SOLAR} 0 var(--solar-share), {REDE} var(--solar-share) 100%); position: relative; }}
.source-gauge::after {{ content: ""; position: absolute; width: 145px; height: 145px; border-radius: 50%; background: {CARD}; border: 1px solid {BORDA}; }}
.source-gauge__content {{ position: relative; z-index: 1; text-align: center; }}
.source-gauge__value {{ color: #FFFFFF; font-size: 1.75rem; font-weight: 800; line-height: 1; }}
.source-gauge__label {{ color: #8D98A6; font-size: 0.7rem; margin-top: 0.35rem; }}
.source-detail {{ margin-top: 0.35rem; }}
.source-detail__item {{ padding: 0.8rem 0; border-bottom: 1px solid #242D38; }}
.source-detail__item:last-child {{ border-bottom: 0; }}
.source-detail__head {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; }}
.source-detail__name {{ display: flex; align-items: center; gap: 0.5rem; color: #DDE2E8; font-size: 0.78rem; font-weight: 700; }}
.source-detail__value {{ color: #FFFFFF; font-size: 0.9rem; font-weight: 800; }}
.source-detail__track {{ height: 6px; border-radius: 3px; background: #202833; overflow: hidden; margin-top: 0.55rem; }}
.source-detail__fill {{ height: 100%; border-radius: 3px; }}
.source-detail__fill--solar {{ background: {SOLAR}; }}
.source-detail__fill--grid {{ background: {REDE}; }}
.session-highlight {{ display: grid; gap: 0.72rem; margin-top: 0.45rem; }}
.session-highlight__item {{ border-left: 3px solid {FIAP}; padding: 0.55rem 0 0.55rem 0.75rem; }}
.session-highlight__item--solar {{ border-color: {SOLAR}; }}
.session-highlight__item--goodwe {{ border-color: {GOODWE}; }}
.session-highlight__label {{ color: #7F8A98; font-size: 0.68rem; text-transform: uppercase; }}
.session-highlight__value {{ color: #FFFFFF; font-size: 0.98rem; font-weight: 800; margin-top: 0.18rem; }}
.session-highlight__meta {{ color: #7F8A98; font-size: 0.68rem; margin-top: 0.12rem; }}
@media (max-width: 760px) {{
    .block-container {{ padding-top: 3.75rem; }}
    .hero {{ padding: 1.25rem; }}
    .hero__title {{ font-size: 1.65rem; }}
    .hero__scope {{ grid-template-columns: 1fr; gap: 0.65rem; }}
    .hero__scope-item, .hero__scope-item:first-child {{ border-right: 0; padding: 0; }}
    .config-summary {{ grid-template-columns: 1fr; gap: 0.75rem; }}
    .config-summary__item, .config-summary__item:first-child {{ border-right: 0; border-bottom: 1px solid {BORDA}; padding: 0 0 0.75rem; }}
    .config-summary__item:last-child {{ border-bottom: 0; padding-bottom: 0; }}
    .network-note {{ align-items: flex-start; flex-direction: column; gap: 0.25rem; }}
    .analysis-context {{ align-items: flex-start; flex-direction: column; gap: 0.35rem; }}
    .analysis-context__meta {{ text-align: left; }}
    .analytics-kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .energy-mix__legend {{ grid-template-columns: 1fr; }}
    .analysis-insight {{ align-items: flex-start; flex-direction: column; gap: 0.4rem; }}
}}
@media (max-width: 480px) {{
    .analytics-kpis {{ grid-template-columns: 1fr; }}
    .analytics-kpi {{ min-height: 112px; }}
}}
</style>""",
    unsafe_allow_html=True,
)


# ==================================================
# COMPONENTES VISUAIS
# ==================================================

HERO_HTML = (
    '<section class="hero"><div class="hero__eyebrow">FIAP · Sprint 3 · Energia e mobilidade</div>'
    '<h1 class="hero__title">ChargeGrid Simulator</h1>'
    '<div class="hero__subtitle">Simulação e monitoramento de sessões de recarga com integração de energia solar.</div>'
    '<div class="hero__scope"><div class="hero__scope-item"><span class="hero__scope-icon">🚗</span><span class="hero__scope-label">Mobilidade</span><span class="hero__scope-value">Recarga de veículos elétricos</span></div>'
    '<div class="hero__scope-item"><span class="hero__scope-icon">☀️</span><span class="hero__scope-label">Geração</span><span class="hero__scope-value">Energia solar integrada</span></div>'
    '<div class="hero__scope-item"><span class="hero__scope-icon">⚡</span><span class="hero__scope-label">Continuidade</span><span class="hero__scope-value">Complemento da rede elétrica</span></div></div>'
    '<div class="hero__badges"><span class="badge">Sprint 3</span><span class="badge badge--fiap">FIAP</span>'
    '<span class="badge badge--goodwe">GoodWe</span></div></section>'
)


def render_html(content):
    """Renderiza fragmentos HTML compactos sem indentação Markdown."""
    st.markdown(content, unsafe_allow_html=True)


def render_screen_header(title, copy):
    render_html(
        f'<div class="screen-title">{title}</div>'
        f'<div class="screen-copy">{copy}</div>'
    )


def render_section_title(title, kicker=None):
    kicker_html = f'<div class="section-kicker">{kicker}</div>' if kicker else ""
    render_html(f'{kicker_html}<div class="section-title">{title}</div>')


def render_status(label, kind):
    render_html(
        f'<span class="status status--{kind}"><span class="status__dot"></span>{label}</span>'
    )


def render_energy_card(icon, title, value, meta, kind):
    render_html(
        f'<div class="energy-card energy-card--{kind}"><div class="energy-card__icon">{icon}</div>'
        f'<div class="energy-card__title">{title}</div><div class="energy-card__value">{value}</div>'
        f'<div class="energy-card__meta">{meta}</div></div>'
    )


def formatar_numero(valor, casas=2):
    """Formata números no padrão brasileiro para a interface."""
    numero = f"{valor:,.{casas}f}"
    return numero.replace(",", "_").replace(".", ",").replace("_", ".")


def render_dashboard_header(title, copy):
    render_html(
        f'<div class="dashboard-title">{title}</div>'
        f'<div class="dashboard-copy">{copy}</div>'
    )


# ==================================================
# BANCO E ESTADO DA APLICAÇÃO
# ==================================================

database.criar_banco()

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

PASSO_MINUTOS = 5
INTERVALO_SEG = 0.5


# ==================================================
# SIDEBAR E CABEÇALHO
# ==================================================

with st.sidebar:
    render_html(
        '<div class="sidebar-brand"><div class="sidebar-brand__eyebrow">Energia &amp; mobilidade</div>'
        '<div class="sidebar-brand__name">'
        '<span class="sidebar-brand__mark">⚡</span>ChargeGrid</div>'
        '<div class="sidebar-brand__copy">Simulador de recarga elétrica</div></div>'
    )
    render_html('<div class="sidebar-nav-label">Menu principal</div>')
    opcoes_menu = {
        "⚡  Simulação": "Simulação",
        "🕘  Histórico": "Histórico",
        "▦  Análise dos Dados": "Análise dos Dados",
    }
    menu_selecionado = st.radio(
        "Navegação",
        list(opcoes_menu),
        label_visibility="collapsed",
    )
    menu = opcoes_menu[menu_selecionado]
    render_html(
        '<div class="sidebar-partner"><div class="sidebar-partner__label">Tecnologia solar</div>'
        f'<img class="sidebar-partner__logo" src="{GOODWE_LOGO_URI}" alt="GoodWe">'
        '<div class="sidebar-partner__copy">Referência em soluções fotovoltaicas e gestão inteligente de energia.</div></div>'
    )
    render_html(
        '<div class="sidebar-footer"><div class="sidebar-footer__label">Projeto acadêmico</div>'
        '<div class="sidebar-footer__title">FIAP · Sprint 3</div>'
        '<div class="sidebar-footer__copy">Pensamento Computacional com Python · SERS</div></div>'
    )

render_html(HERO_HTML)


# ==================================================
# TELA: SIMULAÇÃO
# ==================================================

def tela_simulacao():
    if st.session_state.ativa:
        render_status("RECARGA EM ANDAMENTO", "live")
        st.write("")

        atual = simulator.calcular_sessao(
            st.session_state.potencia,
            st.session_state.tempo_min,
            st.session_state.perc_solar,
        )

        render_section_title("Indicadores da sessão", "Monitoramento")
        c1, c2, c3 = st.columns(3)
        c1.metric("⏱ Tempo Simulado", f"{atual['duracao_minutos']} min")
        c2.metric("⚡ Potência", f"{atual['potencia_kw']} kW")
        c3.metric("🔋 Energia Total", f"{atual['energia_total_kwh']} kWh")

        c4, c5, c6 = st.columns(3)
        c4.metric("☀️ Energia Solar", f"{atual['energia_solar_kwh']} kWh")
        c5.metric("🏙 Energia da Rede", f"{atual['energia_rede_kwh']} kWh")
        c6.metric("♻️ Energia Renovável", f"{atual['percentual_renovavel']}%")

        st.write("")
        render_section_title("Fluxo de energia da sessão", "Distribuição")

        f1, f2, f3 = st.columns(3)
        with f1:
            render_energy_card(
                "☀️",
                "Painel Solar",
                f"{atual['energia_solar_kwh']} kWh",
                "Fonte renovável",
                "solar",
            )
        with f2:
            render_energy_card(
                "🔌",
                "Estação de Recarga",
                f"{atual['potencia_kw']} kW",
                "Conversão e entrega",
                "station",
            )
        with f3:
            render_energy_card(
                "🚗",
                "Veículo Elétrico",
                f"{atual['energia_total_kwh']} kWh",
                "Energia acumulada",
                "vehicle",
            )

        render_html(
            '<div class="network-note"><div><div class="network-note__label">Rede elétrica · complemento da sessão</div>'
            f'<div class="network-note__value">{atual["energia_rede_kwh"]} kWh</div></div>'
            '<div class="network-note__label">Solar → Estação → Veículo<br>Rede → Estação</div></div>'
        )
        st.progress(atual["percentual_renovavel"] / 100)
        st.caption(
            f"{atual['percentual_renovavel']}% da energia utilizada nesta sessão "
            "é proveniente de fonte solar."
        )

        if len(st.session_state.pontos) > 1:
            st.write("")
            with st.container(border=True):
                render_section_title("Evolução da energia acumulada", "Série temporal")
                dados_grafico = {
                    "Tempo (min)": [p["min"] for p in st.session_state.pontos],
                    "Energia Total": [p["total"] for p in st.session_state.pontos],
                    "Energia Solar": [p["solar"] for p in st.session_state.pontos],
                    "Energia da Rede": [p["rede"] for p in st.session_state.pontos],
                }
                st.line_chart(
                    dados_grafico,
                    x="Tempo (min)",
                    y=["Energia Total", "Energia Solar", "Energia da Rede"],
                    color=["#F4F6F8", SOLAR, REDE],
                    height=320,
                )

        st.write("")
        if st.button("FINALIZAR RECARGA", width="stretch"):
            final = simulator.calcular_sessao(
                st.session_state.potencia,
                st.session_state.tempo_min,
                st.session_state.perc_solar,
            )
            database.salvar_sessao(final)
            st.session_state.ativa = False
            st.session_state.ultima_concluida = final
            st.rerun()

        st.session_state.tempo_min += PASSO_MINUTOS
        novo = simulator.calcular_sessao(
            st.session_state.potencia,
            st.session_state.tempo_min,
            st.session_state.perc_solar,
        )
        st.session_state.pontos.append(
            {
                "min": st.session_state.tempo_min,
                "total": novo["energia_total_kwh"],
                "solar": novo["energia_solar_kwh"],
                "rede": novo["energia_rede_kwh"],
            }
        )
        time.sleep(INTERVALO_SEG)
        st.rerun()

    elif st.session_state.ultima_concluida is not None:
        s = st.session_state.ultima_concluida
        render_status("RECARGA CONCLUÍDA", "success")
        st.write("")
        render_screen_header(
            "Resumo da sessão",
            "Confira os principais resultados energéticos da recarga finalizada.",
        )

        d1, d2, d3 = st.columns(3)
        d1.metric("⏱ Duração", simulator.formatar_duracao(s["duracao_minutos"]))
        d2.metric("🔋 Energia Total", f"{s['energia_total_kwh']} kWh")
        d3.metric("☀️ Energia Solar", f"{s['energia_solar_kwh']} kWh")

        d4, d5 = st.columns(2)
        d4.metric("🏙 Energia da Rede", f"{s['energia_rede_kwh']} kWh")
        d5.metric("♻️ Participação Renovável", f"{s['percentual_renovavel']}%")

        st.write("")
        if st.button("NOVA SIMULAÇÃO", width="stretch"):
            st.session_state.ultima_concluida = None
            st.session_state.pontos = []
            st.session_state.tempo_min = 0
            st.rerun()

    else:
        render_screen_header(
            "Nova Sessão de Recarga",
            "Configure a potência e a disponibilidade solar para iniciar a simulação.",
        )

        with st.container(border=True):
            render_section_title("Parâmetros da recarga", "Configuração")
            col1, col2 = st.columns(2)

            with col1:
                potencia = st.selectbox(
                    "Potência do carregador",
                    [7.4, 11.0, 22.0],
                    index=1,
                    format_func=lambda x: f"{x} kW",
                )
            with col2:
                perc = st.slider(
                    "Disponibilidade de energia solar (%)",
                    0,
                    100,
                    70,
                )

            render_html(
                '<div class="config-summary">'
                f'<div class="config-summary__item"><div class="config-summary__label">Potência selecionada</div><div class="config-summary__value">{potencia} kW</div></div>'
                f'<div class="config-summary__item"><div class="config-summary__label">Energia solar disponível</div><div class="config-summary__value config-summary__value--solar">{perc}%</div></div>'
                f'<div class="config-summary__item"><div class="config-summary__label">Complemento estimado da rede</div><div class="config-summary__value config-summary__value--grid">{100 - perc}%</div></div>'
                '</div>'
            )

            st.write("")
            if st.button("INICIAR RECARGA", width="stretch"):
                st.session_state.potencia = float(potencia)
                st.session_state.perc_solar = float(perc)
                st.session_state.tempo_min = PASSO_MINUTOS

                primeiro = simulator.calcular_sessao(
                    float(potencia),
                    PASSO_MINUTOS,
                    float(perc),
                )
                st.session_state.pontos = [
                    {
                        "min": PASSO_MINUTOS,
                        "total": primeiro["energia_total_kwh"],
                        "solar": primeiro["energia_solar_kwh"],
                        "rede": primeiro["energia_rede_kwh"],
                    }
                ]
                st.session_state.ativa = True
                st.session_state.ultima_concluida = None
                st.rerun()


# ==================================================
# TELA: HISTÓRICO
# ==================================================

def tela_historico():
    render_screen_header(
        "Histórico de Recargas",
        "Consulte as sessões simuladas e armazenadas no sistema.",
    )
    sessoes = database.listar_sessoes()

    if not sessoes:
        st.info("Nenhuma sessão registrada ainda. Inicie uma recarga na aba Simulação.")
        return

    resumo = database.calcular_resumo()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Sessões", resumo["total_sessoes"])
    c2.metric("Energia Consumida", f"{resumo['energia_total']} kWh")
    c3.metric("Energia Solar", f"{resumo['energia_solar']} kWh")

    st.write("")
    render_section_title("Sessões registradas", "Base local")
    linhas = []
    for s in sessoes:
        linhas.append(
            {
                "ID": s[0],
                "Data": s[1],
                "Potência": f"{s[2]} kW",
                "Duração": simulator.formatar_duracao(s[3]),
                "Energia Total": f"{s[4]:.2f} kWh",
                "Energia Solar": f"{s[5]:.2f} kWh",
                "Energia da Rede": f"{s[6]:.2f} kWh",
                "Renovável": f"{s[7]:.1f}%",
            }
        )

    st.dataframe(linhas, width="stretch", hide_index=True)


# ==================================================
# TELA: ANÁLISE DOS DADOS
# ==================================================

def tela_analise():
    render_screen_header(
        "Análise dos Dados",
        "Quatro perspectivas para acompanhar consumo, fontes e eficiência das recargas.",
    )
    r = database.calcular_resumo()

    if r["total_sessoes"] == 0:
        st.info("Sem dados para analisar. Finalize ao menos uma recarga.")
        return

    sessoes = list(reversed(database.listar_sessoes()))
    ultima_sessao = sessoes[-1]
    duracao_total = sum(sessao[3] for sessao in sessoes)
    duracao_media = duracao_total / len(sessoes)
    potencia_media = sum(sessao[2] for sessao in sessoes) / len(sessoes)
    maior_consumo = max(sessoes, key=lambda sessao: sessao[4])
    melhor_renovavel = max(sessoes, key=lambda sessao: sessao[7])
    dependencia_rede = 100 - r["percentual_medio"]

    dados = pd.DataFrame(
        [
            {
                "Sessão": f"#{sessao[0]}",
                "Energia total": sessao[4],
                "Energia solar": sessao[5],
                "Energia da rede": sessao[6],
                "Renovável (%)": sessao[7],
            }
            for sessao in sessoes
        ]
    )

    render_html(
        '<div class="analysis-context"><div class="analysis-context__status">'
        '<span class="analysis-context__dot"></span>Dados consolidados</div>'
        f'<div class="analysis-context__meta">Última recarga: {ultima_sessao[1]} · '
        f'{r["total_sessoes"]} sessões processadas</div></div>'
    )

    render_html(
        '<div class="analytics-kpis">'
        '<div class="analytics-kpi"><div class="analytics-kpi__head"><span>Sessões concluídas</span>'
        '<span class="analytics-kpi__icon">⚡</span></div>'
        f'<div class="analytics-kpi__value">{r["total_sessoes"]}</div>'
        f'<div class="analytics-kpi__meta">{simulator.formatar_duracao(duracao_total)} de recarga acumulada</div></div>'
        '<div class="analytics-kpi analytics-kpi--goodwe"><div class="analytics-kpi__head"><span>Energia entregue</span>'
        '<span class="analytics-kpi__icon">🔋</span></div>'
        f'<div class="analytics-kpi__value">{formatar_numero(r["energia_total"])} kWh</div>'
        '<div class="analytics-kpi__meta">Consumo total de todas as sessões</div></div>'
        '<div class="analytics-kpi analytics-kpi--solar"><div class="analytics-kpi__head"><span>Média por sessão</span>'
        '<span class="analytics-kpi__icon">↗</span></div>'
        f'<div class="analytics-kpi__value">{formatar_numero(r["consumo_medio"])} kWh</div>'
        f'<div class="analytics-kpi__meta">Potência média de {formatar_numero(potencia_media, 1)} kW</div></div>'
        '<div class="analytics-kpi analytics-kpi--green"><div class="analytics-kpi__head"><span>Participação renovável</span>'
        '<span class="analytics-kpi__icon">♻</span></div>'
        f'<div class="analytics-kpi__value">{formatar_numero(r["percentual_medio"])}%</div>'
        f'<div class="analytics-kpi__meta">{formatar_numero(r["energia_solar"])} kWh de origem solar</div></div>'
        '</div>'
    )

    resumo_tab, evolucao_tab, fontes_tab, eficiencia_tab = st.tabs(
        ["⚡ Resumo geral", "📈 Evolução", "☀️ Matriz energética", "♻ Eficiência"]
    )

    with resumo_tab:
        render_dashboard_header(
            "Resumo operacional",
            "Balanço acumulado e perfil médio das sessões concluídas.",
        )
        coluna_balanco, coluna_perfil = st.columns([1.25, 1])

        with coluna_balanco:
            with st.container(border=True):
                render_section_title("Balanço de energia", "Energia entregue")
                render_html(
                    '<div class="energy-mix"><div class="energy-mix__totals"><div>'
                    '<div class="energy-mix__total-label">Consumo acumulado</div>'
                    f'<div class="energy-mix__total-value">{formatar_numero(r["energia_total"])} kWh</div></div>'
                    f'<div class="energy-mix__renewable">{formatar_numero(r["percentual_medio"])}% solar</div></div>'
                    '<div class="energy-mix__bar" aria-label="Distribuição entre energia solar e rede elétrica">'
                    f'<div class="energy-mix__solar" style="width:{r["percentual_medio"]}%"></div>'
                    f'<div class="energy-mix__grid" style="width:{dependencia_rede}%"></div></div>'
                    '<div class="energy-mix__legend">'
                    '<div class="energy-mix__legend-item"><span class="energy-mix__swatch energy-mix__swatch--solar"></span><div>'
                    '<div class="energy-mix__legend-label">Energia solar</div>'
                    f'<div class="energy-mix__legend-value">{formatar_numero(r["energia_solar"])} kWh</div></div></div>'
                    '<div class="energy-mix__legend-item"><span class="energy-mix__swatch energy-mix__swatch--grid"></span><div>'
                    '<div class="energy-mix__legend-label">Energia da rede</div>'
                    f'<div class="energy-mix__legend-value">{formatar_numero(r["energia_rede"])} kWh</div></div></div>'
                    '</div></div>'
                )

        with coluna_perfil:
            with st.container(border=True):
                render_section_title("Perfil das recargas", "Operação")
                render_html(
                    '<div class="profile-list">'
                    f'<div class="profile-row"><span class="profile-row__label">Duração média</span><span class="profile-row__value">{simulator.formatar_duracao(round(duracao_media))}</span></div>'
                    f'<div class="profile-row"><span class="profile-row__label">Potência média</span><span class="profile-row__value">{formatar_numero(potencia_media, 1)} kW</span></div>'
                    f'<div class="profile-row"><span class="profile-row__label">Maior consumo</span><span class="profile-row__value">Sessão #{maior_consumo[0]} · {formatar_numero(maior_consumo[4])} kWh</span></div>'
                    f'<div class="profile-row"><span class="profile-row__label">Uso da rede</span><span class="profile-row__value">{formatar_numero(dependencia_rede)}%</span></div>'
                    '</div>'
                )

        render_html(
            '<div class="analysis-insight"><div><div class="analysis-insight__label">Leitura rápida</div>'
            f'<div class="analysis-insight__text">A fonte solar evitou o uso de {formatar_numero(r["energia_solar"])} kWh da rede elétrica.</div></div>'
            f'<div class="analysis-insight__value">{formatar_numero(r["percentual_medio"])}% renovável</div></div>'
        )

    with evolucao_tab:
        render_dashboard_header(
            "Evolução das recargas",
            "Comparação cronológica da energia total, solar e proveniente da rede.",
        )
        with st.container(border=True):
            st.line_chart(
                dados,
                x="Sessão",
                y=["Energia total", "Energia solar", "Energia da rede"],
                color=[FIAP, SOLAR, REDE],
                x_label="Sessões concluídas",
                y_label="Energia (kWh)",
                height=370,
                width="stretch",
            )
            st.caption("Passe o cursor sobre as linhas para comparar os valores de cada sessão.")

    with fontes_tab:
        render_dashboard_header(
            "Matriz energética",
            "Participação acumulada de cada fonte no abastecimento dos veículos.",
        )
        coluna_grafico, coluna_fontes = st.columns([0.9, 1.15])

        with coluna_grafico:
            with st.container(border=True):
                render_section_title("Origem da energia", "Composição")
                render_html(
                    f'<div class="source-gauge" style="--solar-share:{r["percentual_medio"]}%">'
                    '<div class="source-gauge__content">'
                    f'<div class="source-gauge__value">{formatar_numero(r["percentual_medio"], 1)}%</div>'
                    '<div class="source-gauge__label">energia solar</div></div></div>'
                )

        with coluna_fontes:
            with st.container(border=True):
                render_section_title("Detalhamento das fontes", "Acumulado")
                render_html(
                    '<div class="source-detail">'
                    '<div class="source-detail__item"><div class="source-detail__head">'
                    '<div class="source-detail__name"><span class="energy-mix__swatch energy-mix__swatch--solar"></span>Energia solar</div>'
                    f'<div class="source-detail__value">{formatar_numero(r["energia_solar"])} kWh</div></div>'
                    '<div class="source-detail__track">'
                    f'<div class="source-detail__fill source-detail__fill--solar" style="width:{r["percentual_medio"]}%"></div></div></div>'
                    '<div class="source-detail__item"><div class="source-detail__head">'
                    '<div class="source-detail__name"><span class="energy-mix__swatch energy-mix__swatch--grid"></span>Energia da rede</div>'
                    f'<div class="source-detail__value">{formatar_numero(r["energia_rede"])} kWh</div></div>'
                    '<div class="source-detail__track">'
                    f'<div class="source-detail__fill source-detail__fill--grid" style="width:{dependencia_rede}%"></div></div></div>'
                    '</div>'
                )
                st.caption(
                    f"A cada 100 kWh consumidos, {formatar_numero(r['percentual_medio'], 1)} kWh vieram dos painéis solares."
                )

    with eficiencia_tab:
        render_dashboard_header(
            "Eficiência renovável por sessão",
            "Percentual solar de cada recarga e destaques de desempenho.",
        )
        coluna_eficiencia, coluna_destaques = st.columns([1.55, 0.75])

        with coluna_eficiencia:
            with st.container(border=True):
                st.bar_chart(
                    dados,
                    x="Sessão",
                    y="Renovável (%)",
                    color=SOLAR,
                    x_label="Sessões concluídas",
                    y_label="Participação renovável (%)",
                    height=350,
                    width="stretch",
                )

        with coluna_destaques:
            with st.container(border=True):
                render_section_title("Destaques", "Desempenho")
                render_html(
                    '<div class="session-highlight">'
                    '<div class="session-highlight__item session-highlight__item--solar">'
                    '<div class="session-highlight__label">Melhor uso solar</div>'
                    f'<div class="session-highlight__value">Sessão #{melhor_renovavel[0]}</div>'
                    f'<div class="session-highlight__meta">{formatar_numero(melhor_renovavel[7], 1)}% renovável</div></div>'
                    '<div class="session-highlight__item">'
                    '<div class="session-highlight__label">Média geral</div>'
                    f'<div class="session-highlight__value">{formatar_numero(r["percentual_medio"], 1)}%</div>'
                    '<div class="session-highlight__meta">participação solar acumulada</div></div>'
                    '<div class="session-highlight__item session-highlight__item--goodwe">'
                    '<div class="session-highlight__label">Última sessão</div>'
                    f'<div class="session-highlight__value">{formatar_numero(ultima_sessao[7], 1)}%</div>'
                    f'<div class="session-highlight__meta">{formatar_numero(ultima_sessao[4])} kWh entregues</div></div>'
                    '</div>'
                )


# ==================================================
# ROTEAMENTO
# ==================================================

if menu == "Simulação":
    tela_simulacao()
elif menu == "Histórico":
    tela_historico()
else:
    tela_analise()
