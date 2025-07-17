# pages/1_📈_Tableau_Visualisierungen.py

import streamlit as st
from pathlib import Path

# ----------------------------
# Seiteneinstellungen
# ----------------------------
st.set_page_config(
    page_title="Tableau Visualisierungen",
    page_icon="📈",
    layout="wide"
)

st.title("Unsere Schlüssel-Visualisierungen zur Halbleiterindustrie")
st.markdown("""
Hier präsentieren wir die wichtigsten Erkenntnisse und Trends aus unseren Datenanalysen,
visualisiert mit Tableau.
""")

# ----------------------------
# Pfade vorbereiten
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # eine Ebene hoch
IMAGE_DIR = BASE_DIR / "Screenshots"

# ----------------------------
# Hilfsfunktion: Abschnitt mit Screenshot
# ----------------------------
def show_section(title, image_filename, description=""):
    st.subheader(title)
    if description:
        st.write(description)

    image_path = IMAGE_DIR / f"{image_filename}.png"
    if not image_path.exists():
        st.error(f"❌ Bild nicht gefunden: {image_path}")
    else:
        st.image(str(image_path), use_container_width=True)

    st.markdown("---")

# ----------------------------
# Tableau-Dashboard-Link
# ----------------------------
st.subheader("🔗 Interaktives Tableau Dashboard")
st.markdown("""
👉 Für interaktive Versionen aller Diagramme:
[➡️ Zum Tableau-Dashboard](https://public.tableau.com/app/profile/indujan.sivanesarajah/viz/Semiconductor_Dashboard/DashboardAdditionalinformation?publish=yes)
""")

# ----------------------------
# 1. Marktüberblick
# ----------------------------
show_section(
    "1. Top-Unternehmen nach Umsatz",
    "Semiconductor_revenue",
    "Ranking der Halbleiterunternehmen nach Gesamtumsatz."
)

show_section(
    "2. Top-Unternehmen nach Mitarbeiteranzahl",
    "Semiconductor_employees",
    "Anzahl der Beschäftigten in führenden Halbleiterunternehmen."
)

show_section(
    "3. Umsatzentwicklung über die Zeit",
    "Revenue_over_time",
    "Globale Umsatzentwicklung der Halbleiterindustrie im Zeitverlauf."
)

show_section(
    "4. Jährliche Wachstumsrate des Umsatzes",
    "Revenue_growth_rate_over_time",
    "Prozentuales Umsatzwachstum im Vergleich zum Vorjahr – pro Land."
)

# ----------------------------
# 2. Produktionsverteilung
# ----------------------------
show_section(
    "5. Waferproduktion nach Land",
    "Wafer_production",
    "Produktionsvolumen von 8-Zoll-Wafern weltweit nach Ländern."
)

# ----------------------------
# 3. Umweltwirkungen gesamt
# ----------------------------
show_section(
    "6. Gesamte CO₂-Emissionen nach Land",
    "CO2_emission",
    "Diese Grafik zeigt die gesamten CO₂-Emissionen durch die Waferproduktion pro Land."
)

show_section(
    "7. Gesamter Wasserverbrauch nach Land",
    "Sum_water_withdrawal",
    "Kumulierte Wasserentnahmen durch Waferfertigung je Land."
)

# ----------------------------
# 4. Umweltwirkungen pro Node
# ----------------------------
show_section(
    "8. Durchschnittliche CO₂-Emissionen pro Technologie-Node",
    "CO2_emission_technology_node",
    "Vergleich der Umweltbelastung verschiedener Fertigungstechnologien (Nodes)."
)

# ----------------------------
# 5. Globaler Footprint kombiniert
# ----------------------------
show_section(
    "9. Globaler Footprint: Wasserverbrauch und Knappheit",
    "Global_footprint_water_use_scarcity",
    "Kombinierte Darstellung von Wasserentnahmen und Knappheitsfaktor (AWaRe) weltweit."
)

# ----------------------------
# Hinweis
# ----------------------------
st.info("Die Screenshots zeigen ausgewählte statische Darstellungen. Für vollständige Interaktivität siehe das eingebettete Tableau-Dashboard oben.")
