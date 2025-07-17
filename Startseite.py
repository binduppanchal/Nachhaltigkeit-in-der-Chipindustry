# Startseite.py

import streamlit as st

# Titel und das Icon für die Browser-Registerkarte
st.set_page_config(
    page_title="Halbleiterindustrie Projekt",
    page_icon="💡",
    layout="wide"
)

st.title("Chips, aber nachhaltig: Umwelt- und Kostenanalyse der globalen Chipproduktion")

# Cover Image
st.image("front_page_cover.jpg", width=800)

st.markdown("""
Bindu, Indujan, Moritz und Alex heißen Dich willkommen zu unserem Abschlussprojekt. Dieses Projekt beleuchtet die globale Halbleiterindustrie und präsentiert wichtige Erkenntnisse
durch Datenvisualisierungen und Tools zur Optimierung in der Herstellung.
""")

st.info("""
### Einleitung:
Die Halbleiterindustrie ist zentral für moderne technologische Innovationen – doch ihre Produktion hat einen erheblichen ökologischen Fußabdruck:

- **Hoher Energieverbrauch**
- **Hoher Wasserverbrauch**
- **Hohe CO2-Emissionen**

Die steigende Chipnachfrage erhöht die Verantwortung für eine **nachhaltige und wirtschaftlich tragfähige Produktion**.

---

### Ziele des Projekts:
- Übersicht über historische Entwicklung und Status Quo
- Verknüpfung von Technologie & Umweltschutz
- Entwicklung interaktiver Tools
- Förderung datenbasierter Entscheidungen

---

### Verwendete Tools:
- 📊 Excel  
- 🐍 Python  
- 📈 Tableau
""")

st.subheader("Navigiere durch unser Projekt:")

st.info("""
Nutze die Navigation auf der linken Seite, um zwischen den verschiedenen Abschnitten unseres Projekts zu wechseln:
* **📈 Tableau-Visualisierungen:** Eine Zusammenfassung unserer wichtigsten Datenvisualisierungen.
* **💰 Umsatz-Mitarbeiter-Rechner:** Ein Tool, um das Verhältnis von Umsatz und benötigten Mitarbeitern in verschiedenen Regionen abzuschätzen.
* **💸 Wafer-Kostenrechner:** Ermittelt geschätzte Kosten für Wasser, Elektrizität und Silizium basierend auf Wafer-Anzahl und Produktionsland.
* **🌎 Umwelt-Waferrechner:**  Berechnet den geschätzten Wasser- und Stromverbrauch, den CO₂-Ausstoß sowie die Kompensationskosten mit PV- und Baummethoden.
* **📌 Fazit und Ausblick:** Fasst zentrale Ergebnisse zusammen, benennt Limitationen der App und zeigt Perspektiven für die weitere Entwicklung auf.


""")

# Wafer Image
st.image("igor-shalyminov-wR4Q9r7KWBU-unsplash.jpg", width=800)
st.markdown(
    """
    <div style='text-align: left; font-size: 0.8em; color: gray;'>
        Foto von <a href="https://unsplash.com/de/@ishalyminov?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash" target="_blank">Igor Shalyminov</a>
        auf <a href="https://unsplash.com/de/fotos/eine-nahaufnahme-eines-spiegels-mit-einer-reflexion-einer-person-wR4Q9r7KWBU?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash" target="_blank">Unsplash</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.write("Vielen Dank für Dein Interesse an unserem Projekt! Wenn Du ganz genau wissen möchtest wie Halbleiter hergestellt werden, schaue Dir gerne das folgende Video an.")

st.subheader("Einführung in die Halbleiterherstellung (Video)")
st.video("https://youtu.be/IkRXpFIRUl4?si=HqjOUIX8XV6fGvjM")



