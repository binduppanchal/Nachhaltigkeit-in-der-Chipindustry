# pages/2_💰_Umsatz_Mitarbeiterrechner
import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Umsatz-Mitarbeiter-Rechner", page_icon="💰", layout="wide")

# --- Währungsdefinitionen und Hilfsfunktionen ---
USD_TO_OTHER_RATES = {
    'USD': 1.0,
    'EUR': 0.93,
    'GBP': 0.79,
    'CNY': 7.25,
    'JPY': 156.00
}

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'CNY': '¥',
    'JPY': '¥'
}

CURRENCY_DECIMALS = {
    'USD': 2,
    'EUR': 2,
    'GBP': 2,
    'CNY': 2,
    'JPY': 0
}

def convert_usd_to_display_currency(value_usd, target_currency):
    rate = USD_TO_OTHER_RATES.get(target_currency, 1.0)
    return value_usd * rate

def convert_display_currency_to_usd(value_display, source_currency):
    rate = USD_TO_OTHER_RATES.get(source_currency, 1.0)
    return value_display / rate

def format_currency_value(value, currency_code):
    if pd.isna(value):
        return "N/A"
    symbol = CURRENCY_SYMBOLS.get(currency_code, '$')
    decimals = CURRENCY_DECIMALS.get(currency_code, 2)
    return f"{symbol}{value:,.{decimals}f}"

# --- Fit-Funktionen ---
region_models = {
    "Amerika": {"a": 1.20, "b": -4.13},
    "Europa": {"a": 1.07, "b": -3.73},
    "Japan": {"a": 0.90, "b": -3.05},
    "Asien-Pazifik": {"a": 1.16, "b": -3.94}
}

def revenue_prediction(employees, a, b):
    return 10**b * (employees ** a)

def employee_prediction(revenue, a, b):
    return (revenue / (10**b)) ** (1/a)

# --- Seiteneinstellungen ---

st.title("💰 Jahresumsatz-Mitarbeiter-Rechner")
st.markdown("""
Nutze dieses Tool, um abzuschätzen, wie viele Mitarbeiter für einen gewünschten Jahresumsatz
in einer bestimmten Region der Halbleiterindustrie benötigt werden, oder wie viel Jahresumsatz
mit einer bestimmten Mitarbeiteranzahl erwartet werden kann. Beide Berechnungen basieren
auf Daten einer Analyse von Companies Market Cap.
""")

st.subheader("Währung auswählen:")
display_currency = st.selectbox("Wähle die Anzeigewährung:", list(USD_TO_OTHER_RATES.keys()), index=0)
st.markdown("---")

# --- Region ---
regions = list(region_models.keys())
st.subheader("Region auswählen:")
selected_region = st.selectbox("Region für Berechnung:", regions)
a = region_models[selected_region]["a"]
b = region_models[selected_region]["b"]
st.markdown("---")

# --- Rechner 1 ---
input_key_umsatz = "desired_revenue_billion_display"
if input_key_umsatz not in st.session_state:
    st.session_state[input_key_umsatz] = 100.0  # Default 100 Mrd.

desired_revenue_billion_display = st.number_input(
    f"Gewünschter Jahresumsatz in Mrd. {display_currency}:",
    min_value=0.0,
    step=10.0,
    format="%.2f",
    key=input_key_umsatz,
)

# Umrechnung: Display (Mrd.) → USD (Mrd.)
desired_revenue_billion_usd = convert_display_currency_to_usd(
    desired_revenue_billion_display, display_currency)

required_employees = math.ceil(employee_prediction(desired_revenue_billion_usd, a, b))

st.success(f"Für **{format_currency_value(desired_revenue_billion_display, display_currency)} Mrd.** Umsatz in **{selected_region}** benötigst du etwa **{required_employees} Angestellte**.")

# Vergleichstabelle Rechner 1
st.markdown("---")
st.subheader("Vergleich: Angestellte für diesen Jahresumsatz in anderen Regionen")
data = []
for reg, params in region_models.items():
    emp = math.ceil(employee_prediction(desired_revenue_billion_usd, params["a"], params["b"]))
    data.append({"Region": reg, "Angestellte": emp})
df_employees = pd.DataFrame(data).set_index("Region")
df_employees = df_employees.sort_values(by="Angestellte")
st.dataframe(df_employees.style.apply(
    lambda x: ['background-color: lightblue' if x.name == selected_region else '' for i in x], axis=1
).format("{:}"))

# --- Rechner 2 ---
input_key_mitarbeiter = "desired_employees"
if input_key_mitarbeiter not in st.session_state:
    st.session_state[input_key_mitarbeiter] = 1000

desired_employees = st.number_input(
    "Anzahl Angestellte:",
    min_value=1,
    value=st.session_state[input_key_mitarbeiter],
    step=100,
    key=input_key_mitarbeiter,
)

predicted_revenue_usd = revenue_prediction(desired_employees, a, b)
predicted_revenue_display = convert_usd_to_display_currency(predicted_revenue_usd, display_currency)

st.success(f"Mit **{desired_employees:} Angestellten** in **{selected_region}** wird ein Jahresumsatz von etwa **{format_currency_value(predicted_revenue_display, display_currency)} Mrd.** erwartet.")

# Vergleichstabelle Rechner 2
st.markdown("---")
st.subheader("Vergleich: Jahresumsatz für diese Mitarbeiterzahl in anderen Regionen")
data = []
for reg, params in region_models.items():
    rev = revenue_prediction(desired_employees, params["a"], params["b"])
    rev_disp = convert_usd_to_display_currency(rev, display_currency)
    data.append({"Region": reg, "Jahresumsatz in Mrd.": rev_disp})
df_revenue = pd.DataFrame(data).set_index("Region")
df_revenue = df_revenue.sort_values(by="Jahresumsatz in Mrd.", ascending=False)
st.dataframe(df_revenue.style.apply(
    lambda x: ['background-color: lightblue' if x.name == selected_region else '' for i in x], axis=1
).format({"Jahresumsatz in Mrd.": lambda x: format_currency_value(x, display_currency)}))

# --- Verdopplungseffekt anzeigen ---
st.markdown("---")
st.subheader("Verdopplungseffekt auf Jahresumsatz")
for region, params in region_models.items():
    a = params["a"]
    factor = 2 ** a
    st.markdown(f"In **{region}** führt eine Verdopplung der Mitarbeiterzahl zu einem **{factor:.2f}-fachen** Umsatz.")

# Hinweis
st.sidebar.markdown("---")
st.sidebar.info("Alle Berechnungen basieren auf Modellfunktionen und dienen nur der Schätzung.")
