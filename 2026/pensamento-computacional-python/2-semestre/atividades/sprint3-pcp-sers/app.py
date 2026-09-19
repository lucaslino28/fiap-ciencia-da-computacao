"""ChargeGrid Intelligence - interface Streamlit.

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
    page_title="ChargeGrid Intelligence",
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
.block-container {{ max-width: 1420px; padding-top: 1.6rem; padding-bottom: 3rem; }}
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
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ padding-top: 0.75rem; }}
.sidebar-brand {{ border-bottom: 1px solid {BORDA}; padding: 0.4rem 0 1.2rem; margin-bottom: 1rem; }}
.sidebar-brand__logo-wrap {{ display: flex; align-items: center; min-height: 72px; padding: 0.8rem 0 1.05rem; border-bottom: 1px solid #222B36; margin-bottom: 1rem; }}
.sidebar-brand__logo {{ display: block; width: 174px; max-width: 82%; height: auto; }}
.sidebar-brand__eyebrow {{ color: {FIAP}; font-size: 0.66rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0; margin-bottom: 0.35rem; }}
.sidebar-brand__name {{ color: #FFFFFF; font-size: 1.18rem; font-weight: 800; line-height: 1.25; }}
.sidebar-brand__copy {{ color: #8993A1; font-size: 0.76rem; line-height: 1.45; margin-top: 0.35rem; }}
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

/* SIMULAÇÃO */
.simulation-steps {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; background: #0D1218; border: 1px solid {BORDA}; border-radius: 8px; margin: 0.2rem 0 1.25rem; overflow: hidden; }}
.simulation-step {{ display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 0.65rem; min-height: 72px; padding: 0.8rem 1rem; border-right: 1px solid {BORDA}; }}
.simulation-step:last-child {{ border-right: 0; }}
.simulation-step__number {{ display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: #1A222C; border: 1px solid #35404D; color: #8E99A7; font-size: 0.76rem; font-weight: 800; }}
.simulation-step__title {{ color: #8E99A7; font-size: 0.78rem; font-weight: 750; }}
.simulation-step__copy {{ color: #626D7A; font-size: 0.68rem; margin-top: 0.12rem; }}
.simulation-step--active {{ background: rgba(237, 20, 91, 0.08); }}
.simulation-step--active .simulation-step__number {{ background: {FIAP}; border-color: {FIAP}; color: #FFFFFF; }}
.simulation-step--active .simulation-step__title {{ color: #FFFFFF; }}
.simulation-step--done .simulation-step__number {{ background: rgba(67, 209, 125, 0.12); border-color: rgba(67, 209, 125, 0.42); color: #63DF99; }}
.simulation-step--done .simulation-step__title {{ color: #C8D0D9; }}
.config-helper {{ color: #7F8A98; font-size: 0.72rem; line-height: 1.5; margin: -0.25rem 0 0.8rem; }}
.charger-profile {{ display: grid; grid-template-columns: auto 1fr; gap: 0.7rem; align-items: center; background: #0D131A; border: 1px solid #27313C; border-left: 3px solid {GOODWE}; border-radius: 8px; padding: 0.75rem 0.85rem; margin: 0.2rem 0 1rem; }}
.charger-profile__icon {{ display: grid; place-items: center; width: 36px; height: 36px; border-radius: 7px; background: rgba(232, 74, 54, 0.1); font-size: 1rem; }}
.charger-profile__title {{ color: #F2F4F7; font-size: 0.78rem; font-weight: 750; }}
.charger-profile__copy {{ color: #7F8A98; font-size: 0.68rem; margin-top: 0.12rem; }}
.charger-profile__specs {{ display: flex; flex-wrap: wrap; gap: 0.35rem 0.7rem; color: #AAB3BE; font-size: 0.66rem; margin-top: 0.45rem; }}
.charger-profile__specs span {{ display: inline-flex; align-items: center; gap: 0.25rem; }}
.preview-panel {{ position: relative; overflow: hidden; height: 100%; min-height: 560px; background: #10161D; border: 1px solid {BORDA}; border-radius: 8px; padding: 1.15rem; }}
.preview-panel::before {{ content: ""; position: absolute; inset: 0 0 auto; height: 3px; background: linear-gradient(90deg, {SOLAR} var(--solar-share), {REDE} var(--solar-share)); }}
.preview-panel__eyebrow {{ color: #7E8996; font-size: 0.67rem; font-weight: 800; text-transform: uppercase; }}
.preview-panel__title {{ color: #FFFFFF; font-size: 1.05rem; font-weight: 780; margin-top: 0.28rem; }}
.preview-panel__copy {{ color: #7F8A98; font-size: 0.72rem; line-height: 1.45; margin-top: 0.28rem; }}
.preview-panel__total {{ border-bottom: 1px solid {BORDA}; padding: 1rem 0 0.85rem; }}
.preview-panel__total-label {{ color: #7F8A98; font-size: 0.7rem; }}
.preview-panel__total-value {{ color: #FFFFFF; font-size: 1.8rem; font-weight: 800; line-height: 1.15; margin-top: 0.2rem; }}
.preview-panel__total-unit {{ color: #8A95A3; font-size: 0.75rem; font-weight: 650; }}
.preview-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.7rem; margin-top: 0.85rem; }}
.preview-stat {{ background: #0C1117; border: 1px solid #252E39; border-radius: 7px; padding: 0.75rem; }}
.preview-stat__label {{ color: #788492; font-size: 0.67rem; }}
.preview-stat__value {{ color: #FFFFFF; font-size: 0.95rem; font-weight: 780; margin-top: 0.2rem; }}
.preview-stat__value--solar {{ color: {SOLAR}; }}
.preview-stat__value--grid {{ color: {REDE}; }}
.preview-split {{ margin-top: 0.95rem; }}
.preview-split__head {{ display: flex; justify-content: space-between; gap: 1rem; color: #8994A2; font-size: 0.68rem; margin-bottom: 0.42rem; }}
.preview-split__bar {{ display: flex; height: 10px; overflow: hidden; background: #1B232D; border-radius: 3px; }}
.preview-split__solar {{ width: var(--solar-share); background: {SOLAR}; }}
.preview-split__grid {{ flex: 1; background: {REDE}; }}
.preview-limit {{ color: #AAB8CA; font-size: 0.7rem; line-height: 1.5; background: #0C1117; border-left: 3px solid {GOODWE}; padding: 0.65rem 0.75rem; margin-top: 0.9rem; }}
.simulation-note {{ display: flex; align-items: flex-start; gap: 0.65rem; background: rgba(110, 168, 254, 0.06); border: 1px solid rgba(110, 168, 254, 0.22); border-radius: 8px; color: #AAB8CA; font-size: 0.72rem; line-height: 1.5; padding: 0.75rem 0.85rem; margin: 0.85rem 0; }}
.simulation-note__icon {{ color: {REDE}; font-size: 0.9rem; }}
.session-strip {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; background: #0E141B; border: 1px solid {BORDA}; border-left: 3px solid {GOODWE}; border-radius: 8px; margin: 0.75rem 0 1.1rem; }}
.session-strip__item {{ padding: 0.72rem 0.85rem; border-right: 1px solid {BORDA}; }}
.session-strip__item:last-child {{ border-right: 0; }}
.session-strip__label {{ color: #747F8D; font-size: 0.65rem; }}
.session-strip__value {{ color: #F4F6F8; font-size: 0.78rem; font-weight: 750; margin-top: 0.15rem; }}
.completion-note {{ display: flex; justify-content: space-between; gap: 1rem; align-items: center; background: rgba(67, 209, 125, 0.07); border: 1px solid rgba(67, 209, 125, 0.25); border-radius: 8px; padding: 0.8rem 0.9rem; margin-top: 0.75rem; }}
.completion-note__copy {{ color: #B7C3CC; font-size: 0.72rem; line-height: 1.45; }}
.completion-note__value {{ color: #63DF99; font-size: 0.84rem; font-weight: 800; white-space: nowrap; }}

/* HISTÓRICO */
.history-context {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; background: #0E141B; border: 1px solid {BORDA}; border-left: 3px solid {FIAP}; border-radius: 8px; padding: 0.75rem 0.9rem; margin: 0.15rem 0 1rem; }}
.history-context__status {{ display: flex; align-items: center; gap: 0.5rem; color: #E7EBF0; font-size: 0.78rem; font-weight: 700; }}
.history-context__dot {{ width: 7px; height: 7px; border-radius: 50%; background: #43D17D; box-shadow: 0 0 0 4px rgba(67, 209, 125, 0.10); }}
.history-context__meta {{ color: #7F8A98; font-size: 0.72rem; text-align: right; }}
.history-kpis {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; margin-bottom: 1.2rem; }}
.history-kpi {{ --history-accent: {FIAP}; position: relative; overflow: hidden; min-height: 122px; background: {CARD}; border: 1px solid {BORDA}; border-radius: 8px; padding: 0.95rem 1rem; }}
.history-kpi::before {{ content: ""; position: absolute; inset: 0 0 auto; height: 3px; background: var(--history-accent); }}
.history-kpi--energy {{ --history-accent: {GOODWE}; }}
.history-kpi--solar {{ --history-accent: {SOLAR}; }}
.history-kpi--green {{ --history-accent: #43D17D; }}
.history-kpi__head {{ display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; color: #8D98A6; font-size: 0.72rem; }}
.history-kpi__icon {{ display: grid; place-items: center; width: 28px; height: 28px; flex: 0 0 28px; border-radius: 6px; background: rgba(255,255,255,0.04); border: 1px solid #2A3440; }}
.history-kpi__value {{ color: #FFFFFF; font-size: 1.45rem; font-weight: 800; line-height: 1.15; margin-top: 0.55rem; }}
.history-kpi__meta {{ color: #727E8C; font-size: 0.68rem; margin-top: 0.28rem; }}
.history-panel {{ height: 100%; min-height: 285px; background: {CARD}; border: 1px solid {BORDA}; border-radius: 8px; padding: 1rem 1.05rem; }}
.history-panel__eyebrow {{ color: {FIAP}; font-size: 0.67rem; font-weight: 800; text-transform: uppercase; }}
.history-panel__title {{ color: #FFFFFF; font-size: 1rem; font-weight: 780; margin-top: 0.25rem; }}
.history-panel__copy {{ color: #7F8A98; font-size: 0.7rem; margin-top: 0.22rem; }}
.latest-session__head {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; padding-bottom: 0.85rem; border-bottom: 1px solid {BORDA}; }}
.latest-session__status {{ display: inline-flex; align-items: center; gap: 0.35rem; color: #63DF99; font-size: 0.66rem; font-weight: 750; white-space: nowrap; }}
.latest-session__status::before {{ content: ""; width: 6px; height: 6px; border-radius: 50%; background: #43D17D; }}
.latest-session__energy {{ color: #FFFFFF; font-size: 1.65rem; font-weight: 800; line-height: 1.1; margin-top: 0.9rem; }}
.latest-session__energy span {{ color: #7F8A98; font-size: 0.72rem; font-weight: 650; }}
.latest-session__details {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.65rem; margin-top: 0.8rem; }}
.latest-session__detail {{ background: #0D1218; border: 1px solid #252E39; border-radius: 7px; padding: 0.7rem; }}
.latest-session__label {{ color: #747F8D; font-size: 0.66rem; }}
.latest-session__value {{ color: #F4F6F8; font-size: 0.86rem; font-weight: 750; margin-top: 0.18rem; }}
.history-source {{ margin-top: 0.9rem; }}
.history-source__head {{ display: flex; justify-content: space-between; gap: 1rem; color: #7F8A98; font-size: 0.67rem; margin-bottom: 0.42rem; }}
.history-source__bar {{ display: flex; height: 9px; border-radius: 3px; overflow: hidden; background: #1A222C; }}
.history-source__solar {{ background: {SOLAR}; }}
.history-source__grid {{ background: {REDE}; }}
.history-source__legend {{ display: flex; justify-content: space-between; gap: 0.75rem; margin-top: 0.45rem; color: #AAB3BE; font-size: 0.68rem; }}
.history-summary {{ margin-top: 0.65rem; }}
.history-summary__row {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.72rem 0; border-bottom: 1px solid #242D38; }}
.history-summary__row:last-child {{ border-bottom: 0; }}
.history-summary__label {{ color: #85909E; font-size: 0.72rem; }}
.history-summary__value {{ color: #FFFFFF; font-size: 0.82rem; font-weight: 750; text-align: right; }}
.history-local-note {{ display: flex; gap: 0.5rem; align-items: flex-start; color: #7F8A98; font-size: 0.68rem; line-height: 1.45; margin-top: 0.75rem; }}
.history-local-note__icon {{ color: {REDE}; }}
.history-table-head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; margin: 1.35rem 0 0.65rem; }}
.history-table-head__meta {{ color: #7F8A98; font-size: 0.7rem; text-align: right; }}
.history-empty {{ display: grid; place-items: center; min-height: 300px; background: #0E141B; border: 1px dashed #35404D; border-radius: 8px; padding: 2rem; text-align: center; }}
.history-empty__icon {{ display: grid; place-items: center; width: 52px; height: 52px; border-radius: 8px; background: rgba(237, 20, 91, 0.09); border: 1px solid rgba(237, 20, 91, 0.28); font-size: 1.35rem; }}
.history-empty__title {{ color: #FFFFFF; font-size: 1rem; font-weight: 780; margin-top: 0.85rem; }}
.history-empty__copy {{ color: #7F8A98; font-size: 0.75rem; line-height: 1.5; max-width: 420px; margin-top: 0.3rem; }}

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
    .simulation-steps {{ grid-template-columns: 1fr; }}
    .simulation-step {{ border-right: 0; border-bottom: 1px solid {BORDA}; }}
    .simulation-step:last-child {{ border-bottom: 0; }}
    .preview-panel {{ min-height: auto; }}
    .session-strip {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .session-strip__item {{ border-bottom: 1px solid {BORDA}; }}
    .session-strip__item:nth-child(2) {{ border-right: 0; }}
    .session-strip__item:nth-last-child(-n+2) {{ border-bottom: 0; }}
    .completion-note {{ align-items: flex-start; flex-direction: column; gap: 0.35rem; }}
    .history-context {{ align-items: flex-start; flex-direction: column; gap: 0.35rem; }}
    .history-context__meta {{ text-align: left; }}
    .history-kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .history-panel {{ min-height: auto; }}
    .history-table-head {{ align-items: flex-start; flex-direction: column; gap: 0.25rem; }}
    .history-table-head__meta {{ text-align: left; }}
    .analysis-context {{ align-items: flex-start; flex-direction: column; gap: 0.35rem; }}
    .analysis-context__meta {{ text-align: left; }}
    .analytics-kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .energy-mix__legend {{ grid-template-columns: 1fr; }}
    .analysis-insight {{ align-items: flex-start; flex-direction: column; gap: 0.4rem; }}
}}
@media (max-width: 480px) {{
    .history-kpis {{ grid-template-columns: 1fr; }}
    .history-kpi {{ min-height: 108px; }}
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
    '<h1 class="hero__title">ChargeGrid Intelligence</h1>'
    '<div class="hero__subtitle">Inteligência para simular, monitorar e analisar recargas com integração de energia solar.</div>'
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


def formatar_moeda(valor):
    return f"R$ {formatar_numero(valor)}"


def render_dashboard_header(title, copy):
    render_html(
        f'<div class="dashboard-title">{title}</div>'
        f'<div class="dashboard-copy">{copy}</div>'
    )


def render_simulation_steps(active_step):
    """Exibe o fluxo da jornada de simulação."""
    steps = (
        (1, "Configure", "Escolha HCA, veículo e energia"),
        (2, "Monitore", "Acompanhe carga, fontes e custo"),
        (3, "Analise", "Revise o resultado da sessão"),
    )
    items = []
    for number, title, copy in steps:
        state = "done" if number < active_step else "active" if number == active_step else ""
        icon = "✓" if number < active_step else str(number)
        items.append(
            f'<div class="simulation-step simulation-step--{state}">'
            f'<div class="simulation-step__number">{icon}</div><div>'
            f'<div class="simulation-step__title">{title}</div>'
            f'<div class="simulation-step__copy">{copy}</div></div></div>'
        )
    render_html(f'<div class="simulation-steps">{"".join(items)}</div>')


# ==================================================
# BANCO E ESTADO DA APLICAÇÃO
# ==================================================

database.criar_banco()

VERSAO_SIMULACAO = 2
if st.session_state.get("versao_simulacao") != VERSAO_SIMULACAO:
    st.session_state.versao_simulacao = VERSAO_SIMULACAO
    st.session_state.ativa = False
    st.session_state.tempo_min = 0
    st.session_state.pontos = []
    st.session_state.ultima_concluida = None
    st.session_state.motivo_finalizacao = None

estado_padrao = {
    "ativa": False,
    "tempo_min": 0,
    "modelo_carregador": "GW11K-HCA",
    "capacidade_bateria_kwh": 60.0,
    "soc_inicial": 20.0,
    "soc_alvo": 80.0,
    "potencia_max_veiculo_kw": 11.0,
    "potencia_solar_kw": 5.0,
    "tarifa_kwh": 1.0,
    "eficiencia_percentual": simulator.EFICIENCIA_PADRAO_PERCENTUAL,
    "pontos": [],
    "ultima_concluida": None,
    "motivo_finalizacao": None,
}
for chave, valor in estado_padrao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

PASSO_MINUTOS = 5
INTERVALO_SEG = 0.5


def calcular_estado_sessao(duracao_minutos=None):
    return simulator.calcular_sessao(
        st.session_state.modelo_carregador,
        st.session_state.tempo_min if duracao_minutos is None else duracao_minutos,
        st.session_state.capacidade_bateria_kwh,
        st.session_state.soc_inicial,
        st.session_state.soc_alvo,
        st.session_state.potencia_max_veiculo_kw,
        st.session_state.potencia_solar_kw,
        st.session_state.tarifa_kwh,
        st.session_state.eficiencia_percentual,
    )


def salvar_e_encerrar_sessao(sessao, motivo):
    database.salvar_sessao(sessao)
    st.session_state.ativa = False
    st.session_state.ultima_concluida = sessao
    st.session_state.motivo_finalizacao = motivo


# ==================================================
# SIDEBAR E CABEÇALHO
# ==================================================

with st.sidebar:
    render_html(
        '<div class="sidebar-brand">'
        f'<div class="sidebar-brand__logo-wrap"><img class="sidebar-brand__logo" src="{GOODWE_LOGO_URI}" alt="GoodWe"></div>'
        '<div class="sidebar-brand__eyebrow">Energia &amp; mobilidade</div>'
        '<div class="sidebar-brand__name">ChargeGrid Intelligence</div>'
        '<div class="sidebar-brand__copy">Simulação e inteligência para recarga elétrica</div></div>'
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
        '<div class="sidebar-footer"><div class="sidebar-footer__label">Projeto acadêmico</div>'
        '<div class="sidebar-footer__title">FIAP · Sprint 3</div>'
        '<div class="sidebar-footer__copy">Pensamento Computacional com Python<br>'
        'Soluções de Energias Renováveis e Sustentáveis</div></div>'
    )

render_html(HERO_HTML)


# ==================================================
# TELA: SIMULAÇÃO
# ==================================================

def tela_simulacao():
    if st.session_state.ativa:
        atual = calcular_estado_sessao()
        if atual["concluida"]:
            salvar_e_encerrar_sessao(atual, "Carga-alvo atingida automaticamente")
            st.rerun()

        render_screen_header(
            "Monitoramento da recarga",
            "Acompanhe o estado da bateria, as fontes de energia e o custo da operação.",
        )
        render_simulation_steps(2)
        render_status("RECARGA EM ANDAMENTO", "live")
        render_html(
            '<div class="session-strip">'
            f'<div class="session-strip__item"><div class="session-strip__label">Carregador</div><div class="session-strip__value">{atual["modelo_carregador"]}</div></div>'
            f'<div class="session-strip__item"><div class="session-strip__label">Instalação</div><div class="session-strip__value">{atual["fases"]} · {atual["tensao_v"]} V</div></div>'
            f'<div class="session-strip__item"><div class="session-strip__label">Limite do veículo</div><div class="session-strip__value">{formatar_numero(st.session_state.potencia_max_veiculo_kw, 1)} kW CA</div></div>'
            f'<div class="session-strip__item"><div class="session-strip__label">Eficiência estimada</div><div class="session-strip__value">{formatar_numero(atual["eficiencia_percentual"], 0)}%</div></div>'
            '</div>'
        )

        render_section_title("Indicadores da sessão", "Monitoramento")
        c1, c2, c3 = st.columns(3)
        c1.metric("🔋 Estado da bateria", f"{formatar_numero(atual['soc_atual'], 1)}%")
        c2.metric("⏱ Tempo restante", simulator.formatar_duracao(atual["tempo_restante_minutos"]))
        c3.metric("⚡ Potência efetiva", f"{formatar_numero(atual['potencia_kw'], 1)} kW")

        c4, c5, c6 = st.columns(3)
        c4.metric("🔌 Energia fornecida", f"{formatar_numero(atual['energia_total_kwh'])} kWh")
        c5.metric("🔋 Armazenada na bateria", f"{formatar_numero(atual['energia_bateria_kwh'])} kWh")
        c6.metric("💳 Custo da rede", formatar_moeda(atual["custo_estimado"]))

        progresso_soc = (
            (atual["soc_atual"] - atual["soc_inicial"])
            / (atual["soc_alvo"] - atual["soc_inicial"])
        )
        st.progress(max(0.0, min(1.0, progresso_soc)))
        st.caption(
            f"Bateria em {formatar_numero(atual['soc_atual'], 1)}% de uma meta de "
            f"{formatar_numero(atual['soc_alvo'], 0)}%."
        )

        st.write("")
        render_section_title("Fluxo operacional", "Energia em tempo real")

        f1, f2, f3 = st.columns(3)
        with f1:
            render_energy_card(
                "☀️",
                "Geração Solar",
                f"{formatar_numero(atual['potencia_solar_kw'], 1)} kW",
                f"{formatar_numero(atual['energia_solar_kwh'])} kWh acumulados",
                "solar",
            )
        with f2:
            render_energy_card(
                "🔌",
                atual["modelo_carregador"],
                f"{formatar_numero(atual['potencia_kw'], 1)} kW",
                f"Nominal de {formatar_numero(atual['potencia_nominal_kw'], 0)} kW",
                "station",
            )
        with f3:
            render_energy_card(
                "🚗",
                "Veículo Elétrico",
                f"{formatar_numero(atual['soc_atual'], 1)}%",
                f"{formatar_numero(atual['energia_bateria_kwh'])} kWh armazenados",
                "vehicle",
            )

        render_html(
            '<div class="network-note"><div><div class="network-note__label">Complemento instantâneo da rede elétrica</div>'
            f'<div class="network-note__value">{formatar_numero(atual["potencia_rede_kw"], 1)} kW · {formatar_numero(atual["energia_rede_kwh"])} kWh</div></div>'
            f'<div class="network-note__label">Perdas estimadas: {formatar_numero(atual["perdas_kwh"])} kWh<br>'
            f'Tarifa informada: {formatar_moeda(atual["tarifa_kwh"])}/kWh</div></div>'
        )

        if len(st.session_state.pontos) > 1:
            st.write("")
            with st.container(border=True):
                render_section_title("Evolução da energia acumulada", "Série temporal")
                dados_grafico = {
                    "Tempo (min)": [p["min"] for p in st.session_state.pontos],
                    "Fornecida": [p["total"] for p in st.session_state.pontos],
                    "Armazenada": [p["bateria"] for p in st.session_state.pontos],
                    "Solar": [p["solar"] for p in st.session_state.pontos],
                    "Rede": [p["rede"] for p in st.session_state.pontos],
                }
                st.line_chart(
                    dados_grafico,
                    x="Tempo (min)",
                    y=["Fornecida", "Armazenada", "Solar", "Rede"],
                    color=["#F4F6F8", "#43D17D", SOLAR, REDE],
                    height=320,
                )

        st.write("")
        if st.button("FINALIZAR E SALVAR SESSÃO", width="stretch"):
            salvar_e_encerrar_sessao(atual, "Finalizada pelo operador")
            st.rerun()

        st.session_state.tempo_min = min(
            st.session_state.tempo_min + PASSO_MINUTOS,
            atual["duracao_estimada_minutos"],
        )
        novo = calcular_estado_sessao()
        st.session_state.pontos.append(
            {
                "min": st.session_state.tempo_min,
                "total": novo["energia_total_kwh"],
                "bateria": novo["energia_bateria_kwh"],
                "solar": novo["energia_solar_kwh"],
                "rede": novo["energia_rede_kwh"],
            }
        )
        time.sleep(INTERVALO_SEG)
        st.rerun()

    elif st.session_state.ultima_concluida is not None:
        s = st.session_state.ultima_concluida
        render_simulation_steps(3)
        render_status("SESSÃO SALVA NO HISTÓRICO", "success")
        st.write("")
        render_screen_header(
            "Resumo da sessão",
            f"{s['modelo_carregador']} · {st.session_state.motivo_finalizacao}.",
        )

        d1, d2, d3 = st.columns(3)
        d1.metric("⏱ Duração", simulator.formatar_duracao(s["duracao_minutos"]))
        d2.metric("🔋 Carga final", f"{formatar_numero(s['soc_atual'], 1)}%")
        d3.metric("🔌 Energia fornecida", f"{formatar_numero(s['energia_total_kwh'])} kWh")

        d4, d5, d6 = st.columns(3)
        d4.metric("🔋 Energia armazenada", f"{formatar_numero(s['energia_bateria_kwh'])} kWh")
        d5.metric("☀️ Participação solar", f"{formatar_numero(s['percentual_renovavel'], 1)}%")
        d6.metric("💳 Custo da rede", formatar_moeda(s["custo_estimado"]))

        render_html(
            '<div class="completion-note">'
            f'<div class="completion-note__copy">A estação forneceu {formatar_numero(s["energia_total_kwh"])} kWh; '
            f'{formatar_numero(s["energia_bateria_kwh"])} kWh chegaram à bateria e '
            f'{formatar_numero(s["perdas_kwh"])} kWh representam as perdas estimadas do processo.</div>'
            f'<div class="completion-note__value">{s["soc_inicial"]:.0f}% → {s["soc_atual"]:.1f}%</div></div>'
        )

        st.write("")
        if st.button("NOVA SIMULAÇÃO", width="stretch"):
            st.session_state.ultima_concluida = None
            st.session_state.motivo_finalizacao = None
            st.session_state.pontos = []
            st.session_state.tempo_min = 0
            st.rerun()

    else:
        render_screen_header(
            "Planeje uma recarga GoodWe HCA",
            "Configure o carregador, o veículo e as condições energéticas do eletroposto.",
        )
        render_simulation_steps(1)

        coluna_configuracao, coluna_previa = st.columns([1.35, 0.85], gap="large")

        with coluna_configuracao:
            with st.container(border=True):
                render_section_title("Configure a sessão", "Etapa 1 de 3")
                render_html(
                    '<div class="config-helper">A potência real será o menor valor entre o carregador HCA e o limite CA aceito pelo veículo.</div>'
                )

                modelos = list(simulator.CARREGADORES_GOODWE)
                modelo = st.selectbox(
                    "Carregador GoodWe",
                    modelos,
                    index=1,
                    help="Modelos oficiais da linha HCA disponíveis no Brasil.",
                )
                carregador = simulator.CARREGADORES_GOODWE[modelo]
                render_html(
                    '<div class="charger-profile"><div class="charger-profile__icon">⚡</div><div>'
                    f'<div class="charger-profile__title">{modelo} · {formatar_numero(carregador["potencia_kw"], 0)} kW</div>'
                    '<div class="charger-profile__copy">Carregador CA com conector Tipo 2 e proteção IP66.</div>'
                    '<div class="charger-profile__specs">'
                    f'<span>{carregador["fases"]}</span><span>{carregador["tensao_v"]} V</span>'
                    f'<span>{carregador["corrente_a"]} A</span><span>50/60 Hz</span></div></div></div>'
                )

                veiculo_1, veiculo_2 = st.columns(2)
                with veiculo_1:
                    capacidade_bateria = st.select_slider(
                        "Capacidade útil da bateria",
                        options=[40.0, 50.0, 60.0, 75.0, 90.0, 100.0],
                        value=60.0,
                        format_func=lambda valor: f"{valor:.0f} kWh",
                    )
                with veiculo_2:
                    potencia_veiculo = st.selectbox(
                        "Limite do carregador interno",
                        [3.7, 7.4, 11.0, 22.0],
                        index=2,
                        format_func=lambda valor: f"{valor} kW CA",
                        help="O veículo pode aceitar menos potência do que a estação oferece.",
                    )

                soc_1, soc_2 = st.columns(2)
                with soc_1:
                    soc_inicial = st.slider("Carga inicial da bateria (%)", 0, 90, 20, 5)
                with soc_2:
                    soc_alvo = st.slider("Carga desejada (%)", 20, 100, 80, 5)

                energia_1, energia_2 = st.columns(2)
                with energia_1:
                    potencia_solar = st.slider(
                        "Potência solar disponível",
                        0.0,
                        float(carregador["potencia_kw"]),
                        min(5.0, float(carregador["potencia_kw"])),
                        0.5,
                        format="%.1f kW",
                    )
                with energia_2:
                    tarifa = st.number_input(
                        "Tarifa da rede (R$/kWh)",
                        min_value=0.0,
                        value=1.0,
                        step=0.05,
                        format="%.2f",
                    )

                eficiencia = st.select_slider(
                    "Eficiência estimada entre a estação e a bateria",
                    options=[85.0, 90.0, 93.0, 95.0],
                    value=90.0,
                    format_func=lambda valor: f"{valor:.0f}%",
                    help="Inclui perdas no carregador interno do veículo e no processo de recarga CA.",
                )

                configuracao_valida = soc_alvo > soc_inicial
                plano = None
                if configuracao_valida:
                    plano = simulator.calcular_plano_recarga(
                        modelo,
                        capacidade_bateria,
                        soc_inicial,
                        soc_alvo,
                        potencia_veiculo,
                        potencia_solar,
                        tarifa,
                        eficiencia,
                    )
                else:
                    st.error("A carga desejada deve ser maior que a carga inicial.")

                render_html(
                    '<div class="simulation-note"><span class="simulation-note__icon">ⓘ</span>'
                    '<span>A simulação avança em intervalos de 5 minutos e é salva automaticamente ao atingir a carga desejada. A tarifa é informada pelo operador.</span></div>'
                )

                if st.button(
                    "INICIAR OPERAÇÃO DE RECARGA",
                    width="stretch",
                    disabled=not configuracao_valida,
                ):
                    st.session_state.modelo_carregador = modelo
                    st.session_state.capacidade_bateria_kwh = float(capacidade_bateria)
                    st.session_state.soc_inicial = float(soc_inicial)
                    st.session_state.soc_alvo = float(soc_alvo)
                    st.session_state.potencia_max_veiculo_kw = float(potencia_veiculo)
                    st.session_state.potencia_solar_kw = float(potencia_solar)
                    st.session_state.tarifa_kwh = float(tarifa)
                    st.session_state.eficiencia_percentual = float(eficiencia)
                    st.session_state.tempo_min = PASSO_MINUTOS

                    primeiro = calcular_estado_sessao()
                    st.session_state.pontos = [
                        {
                            "min": PASSO_MINUTOS,
                            "total": primeiro["energia_total_kwh"],
                            "bateria": primeiro["energia_bateria_kwh"],
                            "solar": primeiro["energia_solar_kwh"],
                            "rede": primeiro["energia_rede_kwh"],
                        }
                    ]
                    st.session_state.ativa = True
                    st.session_state.ultima_concluida = None
                    st.rerun()

        with coluna_previa:
            if plano is None:
                render_html(
                    '<div class="preview-panel" style="--solar-share:0%">'
                    '<div class="preview-panel__eyebrow">Previsão da sessão</div>'
                    '<div class="preview-panel__title">Ajuste o estado da bateria</div>'
                    '<div class="preview-panel__copy">A carga desejada precisa ser maior que a carga inicial.</div></div>'
                )
            else:
                limite_operacional = (
                    f'O veículo limita a operação a {formatar_numero(plano["potencia_efetiva_kw"], 1)} kW, '
                    f'abaixo dos {formatar_numero(plano["potencia_nominal_kw"], 0)} kW nominais do HCA.'
                    if plano["potencia_efetiva_kw"] < plano["potencia_nominal_kw"]
                    else f'O conjunto pode operar na potência nominal de {formatar_numero(plano["potencia_nominal_kw"], 0)} kW.'
                )
                participacao_solar = plano["percentual_renovavel_previsto"]
                render_html(
                    f'<div class="preview-panel" style="--solar-share:{participacao_solar}%">'
                    '<div class="preview-panel__eyebrow">Previsão da sessão</div>'
                    f'<div class="preview-panel__title">Carga de {soc_inicial}% até {soc_alvo}%</div>'
                    '<div class="preview-panel__copy">Estimativa operacional com potência constante e perdas configuradas.</div>'
                    '<div class="preview-panel__total"><div class="preview-panel__total-label">Tempo estimado</div>'
                    f'<div class="preview-panel__total-value">{simulator.formatar_duracao(plano["duracao_estimada_minutos"])}</div></div>'
                    '<div class="preview-grid">'
                    f'<div class="preview-stat"><div class="preview-stat__label">Potência efetiva</div><div class="preview-stat__value">{formatar_numero(plano["potencia_efetiva_kw"], 1)} kW</div></div>'
                    f'<div class="preview-stat"><div class="preview-stat__label">Energia da estação</div><div class="preview-stat__value">{formatar_numero(plano["energia_total_necessaria_kwh"])} kWh</div></div>'
                    f'<div class="preview-stat"><div class="preview-stat__label">Energia na bateria</div><div class="preview-stat__value">{formatar_numero(plano["energia_bateria_necessaria_kwh"])} kWh</div></div>'
                    f'<div class="preview-stat"><div class="preview-stat__label">Perdas estimadas</div><div class="preview-stat__value">{formatar_numero(plano["perdas_previstas_kwh"])} kWh</div></div>'
                    f'<div class="preview-stat"><div class="preview-stat__label">Energia solar</div><div class="preview-stat__value preview-stat__value--solar">{formatar_numero(plano["energia_solar_prevista_kwh"])} kWh</div></div>'
                    f'<div class="preview-stat"><div class="preview-stat__label">Custo da rede</div><div class="preview-stat__value preview-stat__value--grid">{formatar_moeda(plano["custo_previsto"])}</div></div></div>'
                    '<div class="preview-split"><div class="preview-split__head"><span>Solar</span><span>Rede elétrica</span></div>'
                    f'<div class="preview-split__bar"><div class="preview-split__solar"></div><div class="preview-split__grid"></div></div></div>'
                    f'<div class="preview-limit">{limite_operacional}</div></div>'
                )


# ==================================================
# TELA: HISTÓRICO
# ==================================================

def tela_historico():
    render_screen_header(
        "Histórico de Recargas",
        "Acompanhe as sessões concluídas e consulte os dados armazenados localmente.",
    )
    sessoes = database.listar_sessoes()

    if not sessoes:
        render_html(
            '<div class="history-empty"><div>'
            '<div class="history-empty__icon">🕘</div>'
            '<div class="history-empty__title">Nenhuma recarga concluída</div>'
            '<div class="history-empty__copy">Inicie uma simulação e use o botão Finalizar Recarga para registrar a primeira sessão neste histórico.</div>'
            '</div></div>'
        )
        return

    resumo = database.calcular_resumo()
    ultima = sessoes[0]
    total_sessoes = resumo["total_sessoes"]
    duracao_total = sum(sessao[3] for sessao in sessoes)
    duracao_media = duracao_total / total_sessoes
    percentual_rede = max(0, 100 - resumo["percentual_medio"])
    rotulo_sessoes = "sessão armazenada" if total_sessoes == 1 else "sessões armazenadas"
    modelo_ultima = ultima[8] or "Registro anterior"
    soc_ultima = (
        f"{ultima[10]:.0f}% → {ultima[11]:.1f}%"
        if ultima[10] is not None and ultima[11] is not None
        else "Não informado"
    )
    custo_ultima = formatar_moeda(ultima[14]) if ultima[14] is not None else "Não informado"

    render_html(
        '<div class="history-context"><div class="history-context__status">'
        '<span class="history-context__dot"></span>Base local disponível</div>'
        f'<div class="history-context__meta">Última atualização: {ultima[1]} · '
        f'{total_sessoes} {rotulo_sessoes}</div></div>'
    )

    render_html(
        '<div class="history-kpis">'
        '<div class="history-kpi"><div class="history-kpi__head"><span>Sessões concluídas</span><span class="history-kpi__icon">✓</span></div>'
        f'<div class="history-kpi__value">{total_sessoes}</div><div class="history-kpi__meta">Registros disponíveis para consulta</div></div>'
        '<div class="history-kpi history-kpi--energy"><div class="history-kpi__head"><span>Energia entregue</span><span class="history-kpi__icon">⚡</span></div>'
        f'<div class="history-kpi__value">{formatar_numero(resumo["energia_total"])} kWh</div><div class="history-kpi__meta">Consumo acumulado das recargas</div></div>'
        '<div class="history-kpi history-kpi--solar"><div class="history-kpi__head"><span>Energia solar</span><span class="history-kpi__icon">☀️</span></div>'
        f'<div class="history-kpi__value">{formatar_numero(resumo["energia_solar"])} kWh</div><div class="history-kpi__meta">Energia fornecida por fonte renovável</div></div>'
        '<div class="history-kpi history-kpi--green"><div class="history-kpi__head"><span>Participação renovável</span><span class="history-kpi__icon">♻</span></div>'
        f'<div class="history-kpi__value">{formatar_numero(resumo["percentual_medio"], 1)}%</div><div class="history-kpi__meta">Média ponderada de todas as sessões</div></div>'
        '</div>'
    )

    coluna_ultima, coluna_resumo = st.columns([1.35, 0.85], gap="large")

    with coluna_ultima:
        render_html(
            '<div class="history-panel"><div class="latest-session__head"><div>'
            '<div class="history-panel__eyebrow">Última recarga</div>'
            f'<div class="history-panel__title">Sessão #{ultima[0]} · {modelo_ultima}</div>'
            f'<div class="history-panel__copy">Concluída em {ultima[1]}</div></div>'
            '<div class="latest-session__status">Concluída</div></div>'
            f'<div class="latest-session__energy">{formatar_numero(ultima[4])} <span>kWh entregues</span></div>'
            '<div class="latest-session__details">'
            f'<div class="latest-session__detail"><div class="latest-session__label">Potência</div><div class="latest-session__value">{formatar_numero(ultima[2], 1)} kW</div></div>'
            f'<div class="latest-session__detail"><div class="latest-session__label">Duração</div><div class="latest-session__value">{simulator.formatar_duracao(ultima[3])}</div></div>'
            f'<div class="latest-session__detail"><div class="latest-session__label">Carga da bateria</div><div class="latest-session__value">{soc_ultima}</div></div>'
            f'<div class="latest-session__detail"><div class="latest-session__label">Custo da rede</div><div class="latest-session__value">{custo_ultima}</div></div></div>'
            '<div class="history-source"><div class="history-source__head"><span>Distribuição da energia</span>'
            f'<span>{formatar_numero(ultima[7], 1)}% solar</span></div>'
            '<div class="history-source__bar">'
            f'<div class="history-source__solar" style="width:{ultima[7]}%"></div>'
            f'<div class="history-source__grid" style="width:{100 - ultima[7]}%"></div></div>'
            '<div class="history-source__legend">'
            f'<span>Solar · {formatar_numero(ultima[5])} kWh</span>'
            f'<span>Rede · {formatar_numero(ultima[6])} kWh</span></div></div></div>'
        )

    with coluna_resumo:
        render_html(
            '<div class="history-panel"><div class="history-panel__eyebrow">Visão acumulada</div>'
            '<div class="history-panel__title">Resumo do histórico</div>'
            '<div class="history-panel__copy">Indicadores calculados a partir das sessões concluídas.</div>'
            '<div class="history-summary">'
            f'<div class="history-summary__row"><span class="history-summary__label">Tempo total de recarga</span><span class="history-summary__value">{simulator.formatar_duracao(duracao_total)}</span></div>'
            f'<div class="history-summary__row"><span class="history-summary__label">Duração média</span><span class="history-summary__value">{simulator.formatar_duracao(round(duracao_media))}</span></div>'
            f'<div class="history-summary__row"><span class="history-summary__label">Média por sessão</span><span class="history-summary__value">{formatar_numero(resumo["consumo_medio"])} kWh</span></div>'
            f'<div class="history-summary__row"><span class="history-summary__label">Dependência da rede</span><span class="history-summary__value">{formatar_numero(percentual_rede, 1)}%</span></div>'
            '</div><div class="history-local-note"><span class="history-local-note__icon">ⓘ</span>'
            '<span>Este histórico está armazenado no banco local deste computador.</span></div></div>'
        )

    render_html(
        '<div class="history-table-head"><div>'
        '<div class="section-kicker">Base local</div><div class="section-title">Todas as sessões</div></div>'
        f'<div class="history-table-head__meta">{total_sessoes} registros · ordenados do mais recente para o mais antigo</div></div>'
    )

    linhas = pd.DataFrame(
        [
            {
                "Sessão": sessao[0],
                "Data e hora": sessao[1],
                "Carregador": sessao[8] or "Registro anterior",
                "Potência": sessao[2],
                "Duração": simulator.formatar_duracao(sessao[3]),
                "Carga da bateria": (
                    f"{sessao[10]:.0f}% → {sessao[11]:.1f}%"
                    if sessao[10] is not None and sessao[11] is not None
                    else "—"
                ),
                "Energia total": sessao[4],
                "Energia solar": sessao[5],
                "Energia da rede": sessao[6],
                "Custo": formatar_moeda(sessao[14]) if sessao[14] is not None else "—",
                "Renovável": sessao[7],
            }
            for sessao in sessoes
        ]
    )
    altura_tabela = max(145, min(70 + len(linhas) * 35, 520))
    st.dataframe(
        linhas,
        width="stretch",
        height=altura_tabela,
        hide_index=True,
        column_config={
            "Sessão": st.column_config.NumberColumn("Sessão", format="#%d"),
            "Data e hora": st.column_config.TextColumn("Data e hora", width="medium"),
            "Carregador": st.column_config.TextColumn("Carregador", width="medium"),
            "Potência": st.column_config.NumberColumn("Potência", format="%.1f kW"),
            "Duração": st.column_config.TextColumn("Duração"),
            "Carga da bateria": st.column_config.TextColumn("Carga da bateria", width="medium"),
            "Energia total": st.column_config.NumberColumn("Energia total", format="%.2f kWh"),
            "Energia solar": st.column_config.NumberColumn("Energia solar", format="%.2f kWh"),
            "Energia da rede": st.column_config.NumberColumn("Energia da rede", format="%.2f kWh"),
            "Custo": st.column_config.TextColumn("Custo"),
            "Renovável": st.column_config.ProgressColumn(
                "Renovável",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
        },
    )


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
