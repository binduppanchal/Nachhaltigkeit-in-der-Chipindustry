# pages/3_💸_Wafer_Kostenrechner
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Seiteneinstellungen ---
st.set_page_config(page_title="Wafer-Kostenrechner", layout="wide")

# --- Materialpreise (USD) ---
raw_material_prices = {
    "Europa":       {"water": 3.25, "electricity": 0.20,  "silicon": 2.075},
    "Amerika":      {"water": 1.25, "electricity": 0.145, "silicon": 2.75},
    "Japan":        {"water": 0.425,"electricity": 0.17,  "silicon": 1.4},
    "Asien-Pazifik":{"water": 0.60, "electricity": 0.275, "silicon": 2.10},
}
verbrauch_daten_pro_wafer = {
    "Amerika": {
        "co2_kg": 301.10,
        "water_l": 26521.35,
        "electricity_kwh": 718.62
    },
    "Asien-Pazifik": {
        "co2_kg": 407.45,
        "water_l": 59511.81,
        "electricity_kwh": 1402.64
    },
    "Europa": {
        "co2_kg": 316.50,
        "water_l": 20890.70,
        "electricity_kwh": 433.13
    },
    "Japan": {
        "co2_kg": 330.58,
        "water_l": 5897.49,
        "electricity_kwh": 644.44
    },
    "Global Average": {
        "co2_kg": 349.40,
        "water_l": 33784.76,
        "electricity_kwh": 908.97
    }
}

# --- Währungen ---
EXCHANGE_RATES = {"USD": 1.0, "EUR": 0.93, "GBP": 0.79, "CNY": 7.25, "JPY": 158.0}
CURRENCY_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£", "CNY": "¥", "JPY": "¥"}

# --- Hilfsfunktionen ---
def convert_to_currency(value_usd, currency): return value_usd * EXCHANGE_RATES[currency]
def format_currency(value, currency): return f"{CURRENCY_SYMBOLS[currency]}{value:.2f}"


# --- App Titel ---
st.title("💸 Wafer-Kostenrechner: Produktionskosten nach Region")
st.markdown("""
Berechne die **Kosten pro 8-Zoll-Wafer** auf Basis typischer Verbrauchswerte der jeweiligen Region.
""")
st.markdown("---")

# --- Benutzereingaben ---
col1, col2, col3 = st.columns(3)
region = col1.selectbox("🌍 Region wählen:", list(raw_material_prices.keys()))
num_wafers = col2.number_input("🔢 Anzahl Wafer:", min_value=1, value=1000, step=100)
currency = col3.selectbox("💱 Zielwährung:", list(EXCHANGE_RATES.keys()))
st.markdown("---")

def calc_costs(region):
    """
    Berechnet die Materialkosten pro Wafer basierend auf regionalspezifischen
    Verbrauchsdaten (Liter, kWh, kg) und Preisen (€ pro Einheit).
    
    Regionale Verbrauchsdaten = aus 'verbrauch_daten_pro_wafer'
    Regionale Preise = aus 'raw_material_prices'
    
    Gibt ein Dict mit Einzelkosten und Gesamtkosten zurück.
    """
    
    # Region-Mapping von Verbrauch auf Preis-Region
    region_mapping = {
        "America": "Amerika",
        "Asia Pacific": "Asien-Pazifik",
        "Europe": "Europa",
        "Japan": "Japan"
    }
    
    # Verbrauch und Preis abrufen (mit Fallback auf Global Average / Europa)
    verbrauch = verbrauch_daten_pro_wafer.get(region, verbrauch_daten_pro_wafer["Global Average"])
    preis_region = region_mapping.get(region, "Europa")
    preise = raw_material_prices.get(preis_region, raw_material_prices["Europa"])
    
    # Einzelverbräuche
    wasser_m3 = verbrauch["water_l"] / 1000  # Liter → m³
    strom_kwh = verbrauch["electricity_kwh"]
    silizium_kg = 0  # bleibt konstant (für 8 Zoll-Wafer)
    
    # Kosten berechnen
    kosten_wasser = wasser_m3 * preise["water"]
    kosten_strom = strom_kwh * preise["electricity"]
    kosten_silizium = silizium_kg * preise["silicon"]
    
    return {
        "water": kosten_wasser,
        "electricity": kosten_strom,
        "silicon": kosten_silizium,
        "total": kosten_wasser + kosten_strom + kosten_silizium
    }

st.session_state['num_wafers']= num_wafers
# --- Berechnung ---
# Übergib nur den Namen der Region
unit_costs = calc_costs(region)  # nicht raw_material_prices[region]!

# Einzelne Kosten (bereits korrekt berechnet)
total_per_wafer = unit_costs['total']
total_all = total_per_wafer * num_wafers

# Nur Stromkosten (für spätere Vergleiche etc.)
power_cost = unit_costs['electricity']

# unit_costs = calc_costs(raw_material_prices[region])
# total_per_wafer = sum(unit_costs.values())
# total_all = total_per_wafer * num_wafers
# power_cost = unit_costs['electricity'] 

#Daten zwischen speichern
st.session_state["total_cost"] = convert_to_currency(total_all / num_wafers, "EUR")
st.session_state["power_cost"] = convert_to_currency(power_cost , "EUR")

# Umrechnung in Zielwährung
converted = {k: convert_to_currency(v * num_wafers, currency) for k, v in unit_costs.items()}
converted_total = convert_to_currency(total_all, currency)
converted_per_wafer = convert_to_currency(total_per_wafer, currency)

# --- Anzeige: Gesamtkostenübersicht ---
st.subheader(f"💰 Gesamtkosten für {num_wafers} Wafer in {region}")
col1, col2, col3 = st.columns(3)
col1.metric("💵 Gesamtkosten", format_currency(converted_total, currency))
col2.metric("📊 Kosten pro Wafer", format_currency(converted_per_wafer, currency))

# --- Anzeige: Aufgeschlüsselte Kostenbestandteile ---
st.markdown("### 📦 Aufschlüsselung der Einzelkosten")
col1, col2, col3 = st.columns(3)
col1.metric("💧 Wasserkosten", format_currency(converted['water'], currency))
col2.metric("⚡ Stromkosten", format_currency(converted['electricity'], currency))
#col3.metric("💎 Siliziumkosten", format_currency(converted['silicon'], currency))


# --- Donut-Chart Hauptregion (Kosten pro Wafer) ---
# Annahme: raw_material_prices[region] enthält Input für calc_costs,
# das die Kosten pro Wafer zurückgibt
c = calc_costs(region)
kosten_df = pd.DataFrame({
    "Ressource": ["Wasser", "Elektrizität"],
    "Kosten": [
        round(convert_to_currency(c['water'], currency), 2),
        round(convert_to_currency(c['electricity'], currency), 2),
        #round(convert_to_currency(c['silicon'], currency), 2)
    ]
})
fig = px.pie(
    kosten_df,
    names="Ressource",
    values="Kosten",
    hole=0.4,
    title=f"📟 Ressourcen-Kostenverteilung pro Wafer in {region}",
    color="Ressource",
    color_discrete_map={
        "Wasser": "#1f77b4",
        "Elektrizität": "#f0e68c"
        #"Silizium": "#aaaaaa"
    }
)
fig.update_traces(
    textinfo="percent",
    texttemplate="%{percent:.1%}",
    hovertemplate="%{label}: %{value:.2f} " + currency + "<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)


# --- Vergleichsübersicht ---
st.markdown("---")
summary_data = []


for region_name in raw_material_prices.keys():
    kosten = calc_costs(region_name)
    summary_data.append({
        "Region": region_name,
        "Wasser": round(convert_to_currency(kosten['water'], currency), 2),
        "Elektrizität": round(convert_to_currency(kosten['electricity'], currency), 2),
       # "Silizium": round(convert_to_currency(kosten['silicon'], currency), 2),
        "Gesamt": round(convert_to_currency(kosten['total'], currency), 2)
    })

df = pd.DataFrame(summary_data).set_index("Region")
#st.dataframe(df)


# --- Vergleichs-Donuts für andere Regionen ---
other_regions = [r for r in df.index if r != region]
cols = st.columns(len(other_regions))

for i, r in enumerate(other_regions):
    werte = df.loc[r]
    vergleich_df = pd.DataFrame({
        "Ressource": ["Wasser", "Elektrizität"],
        "Kosten": [werte["Wasser"], werte["Elektrizität"]]
    })
    fig = px.pie(
        vergleich_df,
        names="Ressource",
        values="Kosten",
        hole=0.4,
        title=f"📟 {r} – Kostenverteilung pro Wafer",
        color="Ressource",
        color_discrete_map={
            "Wasser": "#1f77b4",
            "Elektrizität": "#f0e68c",
            #"Silizium": "#aaaaaa"
        }
    )
    fig.update_traces(
        textinfo="percent",
        texttemplate="%{percent:.1%}",
        hovertemplate="%{label}: %{value:.2f} " + currency + "<extra></extra>",
        showlegend=False
    )
    cols[i].plotly_chart(fig, use_container_width=True)



# --- Tabelle anzeigen ---

st.markdown("📟 Kostenverteilung pro Wafer für alle Regionen")


st.dataframe(
    df.style
      .apply(lambda x: ['background-color: lightblue' if x.name == region else '' for _ in x], axis=1)
      .format({
          "Wasser": lambda x: format_currency(x, currency),
          "Elektrizität": lambda x: format_currency(x, currency),
         # "Silizium": lambda x: format_currency(x, currency),
          "Gesamt": lambda x: format_currency(x, currency)
      }),
    use_container_width=True
)


# --- Gesamtkosten für die gewählte Anzahl an Wafern berechnen ---
wafer_count = num_wafers  # Annahme: stammt von vorheriger Eingabe
df_total = df.copy()
df_total["Gesamtkosten"] = df_total["Gesamt"] * wafer_count

# --- Balkendiagramm: Gesamtkosten pro Region bei X Wafern ---

# Sortiere DataFrame nach Gesamtkosten aufsteigend (damit höchster Wert oben erscheint)
df_total_sorted = df_total.reset_index().sort_values(by="Gesamtkosten", ascending=True)

# Farbe definieren: Hauptregion hellblau, andere grau
colors = ["#ADD8E6" if r == region else "#cccccc" for r in df_total_sorted["Region"]]

fig_total = px.bar(
    df_total_sorted,
    y="Region",
    x="Gesamtkosten",
    text="Gesamtkosten",
    orientation='h',
    labels={"Gesamtkosten": f"Kosten ({currency})", "Region": "Region"},
    title=f"📦 Gesamtkostenvergleich bei {wafer_count} Wafern"
)

# Farbe über marker_color setzen (überschreibt automatische Farben)
fig_total.update_traces(
    marker_color=colors,
    texttemplate="%{text:.2s}",
    textposition="outside"
)

fig_total.update_layout(
    yaxis=dict(autorange="reversed"),  # Größte Werte oben
    showlegend=False,
    margin=dict(l=100, r=20, t=50, b=50)
)

st.plotly_chart(fig_total, use_container_width=True)


# --- Sidebar Hinweis ---
st.sidebar.markdown("---")
st.sidebar.info("Alle Kosten basieren auf Mittelwerten fester Preisbereiche und dienen nur der Schätzung.")

