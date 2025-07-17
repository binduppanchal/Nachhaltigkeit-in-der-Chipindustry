# pages/4_🌎_Umwelt_Waferrechner.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# -------------------
# Seiteneinstellungen
# -------------------
st.set_page_config(
    page_title="Umwelt Wafer",
    page_icon="🌎",
    layout="wide"
)

st.title("🌱 Umwelt-Auswirkungen der Wafer-Produktion")
st.markdown("""
Gib die gewünschte Anzahl von 8-Zoll-Wafern, das Produktionsland und den Technologie-Node ein,
um den geschätzten Wasserverbrauch, Stromverbrauch und CO2-Ausstoß zu sehen.
Diese Schätzung basiert auf Node-spezifischen Durchschnittswerten pro Land.
""")

st.markdown("---")

# ----------------------
# Übersetzungs-Dictionary Englisch -> Deutsch
# ----------------------
translation_dict = {
    "Australia": "Australien",
    "Austria": "Österreich",
    "Belarus": "Weißrussland",
    "Belgium": "Belgien",
    "Brazil": "Brasilien",
    "Bulgaria": "Bulgarien",
    "Canada": "Kanada",
    "China": "China",
    "Czech Republic": "Tschechien",
    "Denmark": "Dänemark",
    "England": "England",
    "Finland": "Finnland",
    "France": "Frankreich",
    "Germany": "Deutschland",
    "India": "Indien",
    "Ireland": "Irland",
    "Israel": "Israel",
    "Italy": "Italien",
    "Japan": "Japan",
    "Latvia": "Lettland",
    "Malaysia": "Malaysia",
    "Netherlands": "Niederlande",
    "Norway": "Norwegen",
    "Russia": "Russland",
    "Scotland": "Schottland",
    "Singapore": "Singapur",
    "Slovakia": "Slowakei",
    "Slovenia": "Slowenien",
    "South Korea": "Südkorea",
    "Sweden": "Schweden",
    "Switzerland": "Schweiz",
    "Taiwan": "Taiwan",
    "Thailand": "Thailand",
    "Turkey": "Türkei",
    "United Arab Emirates": "Vereinigte Arabische Emirate",
    "US": "USA",
    "Wales": "Wales"
}

# Umkehr-Dict Deutsch -> Englisch für Lookup
translation_dict_rev = {v: k for k, v in translation_dict.items()}

wafer_data = {
    "Australia": {
        "65": {
            "CO2": 358.61,
            "Water": 1229.92,
            "Electricity": 166.71
        }
    },
    "Austria": {
        "65": {
            "CO2": 358.61,
            "Water": 6896.47,
            "Electricity": 471.0
        }
    },
    "Belarus": {
        "65": {
            "CO2": 358.61,
            "Water": 3067.05,
            "Electricity": 354.25
        }
    },
    "Belgium": {
        "5": {
            "CO2": 832.72,
            "Water": 81346.15,
            "Electricity": 1139.02
        },
        "65": {
            "CO2": 358.61,
            "Water": 34868.17,
            "Electricity": 455.91
        }
    },
    "Brazil": {
        "65": {
            "CO2": 358.61,
            "Water": 11703.3,
            "Electricity": 603.87
        }
    },
    "Bulgaria": {
        "65": {
            "CO2": 358.61,
            "Water": 1792.8,
            "Electricity": 28.38
        }
    },
    "Canada": {
        "45": {
            "CO2": 410.63,
            "Water": 10678.29,
            "Electricity": 273.62
        },
        "65": {
            "CO2": 358.61,
            "Water": 16615.78,
            "Electricity": 410.51
        }
    },
    "China": {
        "20": {
            "CO2": 580.34,
            "Water": 1083260.38,
            "Electricity": 15153.48
        },
        "28": {
            "CO2": 581.2,
            "Water": 121250.31,
            "Electricity": 1275.47
        },
        "40": {
            "CO2": 488.26,
            "Water": 111934.28,
            "Electricity": 2169.11
        },
        "45": {
            "CO2": 479.82,
            "Water": 29743.76,
            "Electricity": 1279.99
        },
        "65": {
            "CO2": 417.66,
            "Water": 14191.62,
            "Electricity": 187.81
        }
    },
    "Czech Republic": {
        "65": {
            "CO2": 358.61,
            "Water": 40047.27,
            "Electricity": 603.87
        }
    },
    "Denmark": {
        "7": {
            "CO2": 775.34,
            "Water": 1548.52,
            "Electricity": 182.41
        }
    },
    "England": {
        "65": {
            "CO2": 358.61,
            "Water": 13636.23,
            "Electricity": 305.9
        }
    },
    "Finland": {
        "65": {
            "CO2": 358.61,
            "Water": 15010.1,
            "Electricity": 215.18
        }
    },
    "France": {
        "7": {
            "CO2": 177.12,
            "Water": 219630.24,
            "Electricity": 1548.38
        },
        "10": {
            "CO2": 133.16,
            "Water": 97613.43,
            "Electricity": 688.17
        },
        "14": {
            "CO2": 117.02,
            "Water": 219630.24,
            "Electricity": 1548.38
        },
        "65": {
            "CO2": 83.37,
            "Water": 49185.84,
            "Electricity": 336.69
        }
    },
    "Germany": {
        "10": {
            "CO2": 424.59,
            "Water": 26812.05,
            "Electricity": 865.4
        },
        "20": {
            "CO2": 355.31,
            "Water": 47299.42,
            "Electricity": 1548.38
        },
        "65": {
            "CO2": 257.52,
            "Water": 16961.38,
            "Electricity": 499.74
        }
    },
    "India": {
        "65": {
            "CO2": 358.61,
            "Water": 5075.66,
            "Electricity": 334.3
        }
    },
    "Ireland": {
        "14": {
            "CO2": 342.5,
            "Water": 8020.01,
            "Electricity": 1548.38
        },
        "45": {
            "CO2": 265.32,
            "Water": 3358.34,
            "Electricity": 486.44
        },
        "65": {
            "CO2": 234.2,
            "Water": 3150.21,
            "Electricity": 990.97
        }
    },
    "Israel": {
        "20": {
            "CO2": 497.12,
            "Water": 8232.23,
            "Electricity": 1548.38
        },
        "65": {
            "CO2": 358.61,
            "Water": 4644.34,
            "Electricity": 387.73
        }
    },
    "Italy": {
        "45": {
            "CO2": 410.63,
            "Water": 3923.37,
            "Electricity": 669.82
        },
        "65": {
            "CO2": 358.61,
            "Water": 3316.74,
            "Electricity": 322.96
        }
    },
    "Japan": {
        "7": {
            "CO2": 701.09,
            "Water": 3773.81,
            "Electricity": 324.29
        },
        "14": {
            "CO2": 474.39,
            "Water": 53816.72,
            "Electricity": 11708.05
        },
        "20": {
            "CO2": 446.81,
            "Water": 7907.36,
            "Electricity": 729.66
        },
        "28": {
            "CO2": 448.04,
            "Water": 9478.4,
            "Electricity": 1261.64
        },
        "40": {
            "CO2": 376.44,
            "Water": 13284.74,
            "Electricity": 2169.11
        },
        "65": {
            "CO2": 322.56,
            "Water": 4874.37,
            "Electricity": 417.53
        }
    },
    "Latvia": {
        "65": {
            "CO2": 358.61,
            "Water": 1050.37,
            "Electricity": 113.5
        }
    },
    "Malaysia": {
        "65": {
            "CO2": 358.61,
            "Water": 6242.4,
            "Electricity": 502.94
        }
    },
    "Netherlands": {
        "65": {
            "CO2": 358.61,
            "Water": 4818.25,
            "Electricity": 332.92
        }
    },
    "Norway": {
        "65": {
            "CO2": 358.61,
            "Water": 2381.61,
            "Electricity": 150.75
        }
    },
    "Russia": {
        "65": {
            "CO2": 358.61,
            "Water": 12409.15,
            "Electricity": 296.64
        }
    },
    "Scotland": {
        "10": {
            "CO2": 592.77,
            "Water": 16118.01,
            "Electricity": 387.1
        },
        "65": {
            "CO2": 358.61,
            "Water": 21380.25,
            "Electricity": 471.26
        }
    },
    "Singapore": {
        "14": {
            "CO2": 415.9,
            "Water": 10181.23,
            "Electricity": 4817.19
        },
        "40": {
            "CO2": 329.32,
            "Water": 8582.35,
            "Electricity": 3493.15
        },
        "65": {
            "CO2": 283.11,
            "Water": 3645.74,
            "Electricity": 445.94
        }
    },
    "Slovakia": {
        "65": {
            "CO2": 358.61,
            "Water": 12174.88,
            "Electricity": 113.5
        }
    },
    "Slovenia": {
        "65": {
            "CO2": 358.61,
            "Water": 8551.91,
            "Electricity": 113.5
        }
    },
    "South Korea": {
        "7": {
            "CO2": 716.4,
            "Water": 1402613.86,
            "Electricity": 25489.78
        },
        "10": {
            "CO2": 547.68,
            "Water": 418126.68,
            "Electricity": 7533.73
        },
        "14": {
            "CO2": 487.4,
            "Water": 835243.86,
            "Electricity": 15153.48
        },
        "20": {
            "CO2": 459.1,
            "Water": 1024367.19,
            "Electricity": 18598.92
        },
        "28": {
            "CO2": 459.71,
            "Water": 19920.18,
            "Electricity": 324.29
        },
        "40": {
            "CO2": 385.99,
            "Water": 267873.86,
            "Electricity": 4817.18
        },
        "65": {
            "CO2": 331.43,
            "Water": 19325.39,
            "Electricity": 312.26
        }
    },
    "Sweden": {
        "10": {
            "CO2": 592.77,
            "Water": 13666.5,
            "Electricity": 182.41
        },
        "65": {
            "CO2": 358.61,
            "Water": 25002.01,
            "Electricity": 338.66
        }
    },
    "Switzerland": {
        "20": {
            "CO2": 497.12,
            "Water": 27434.69,
            "Electricity": 387.1
        },
        "65": {
            "CO2": 358.61,
            "Water": 23608.22,
            "Electricity": 323.41
        }
    },
    "Taiwan": {
        "10": {
            "CO2": 639.88,
            "Water": 41623.32,
            "Electricity": 1548.38
        },
        "14": {
            "CO2": 569.58,
            "Water": 203106.39,
            "Electricity": 8388.78
        },
        "20": {
            "CO2": 536.7,
            "Water": 418417.16,
            "Electricity": 17509.31
        },
        "28": {
            "CO2": 537.84,
            "Water": 101565.7,
            "Electricity": 4114.56
        },
        "40": {
            "CO2": 452.1,
            "Water": 39753.12,
            "Electricity": 1507.09
        },
        "45": {
            "CO2": 443.48,
            "Water": 70181.92,
            "Electricity": 2774.09
        },
        "65": {
            "CO2": 386.09,
            "Water": 8410.17,
            "Electricity": 270.97
        }
    },
    "Thailand": {
        "65": {
            "CO2": 358.61,
            "Water": 3119.07,
            "Electricity": 358.69
        }
    },
    "Turkey": {
        "65": {
            "CO2": 358.61,
            "Water": 797.12,
            "Electricity": 88.67
        }
    },
    "United Arab Emirates": {
        "65": {
            "CO2": 358.61,
            "Water": 5185.94,
            "Electricity": 603.86
        }
    },
    "US": {
        "7": {
            "CO2": 597.08,
            "Water": 55563.25,
            "Electricity": 1050.64
        },
        "10": {
            "CO2": 453.77,
            "Water": 19912.19,
            "Electricity": 607.94
        },
        "14": {
            "CO2": 403.28,
            "Water": 133743.25,
            "Electricity": 5168.69
        },
        "20": {
            "CO2": 379.69,
            "Water": 127128.95,
            "Electricity": 3319.55
        },
        "28": {
            "CO2": 380.57,
            "Water": 398279.27,
            "Electricity": 7146.64
        },
        "40": {
            "CO2": 319.71,
            "Water": 68149.2,
            "Electricity": 4817.18
        },
        "45": {
            "CO2": 312.74,
            "Water": 19362.6,
            "Electricity": 433.23
        },
        "65": {
            "CO2": 274.38,
            "Water": 14972.03,
            "Electricity": 338.09
        }
    },
    "Wales": {
        "65": {
            "CO2": 358.61,
            "Water": 21060.94,
            "Electricity": 527.4
        }
    }
}

# --- Materialpreise (EUR) ---
raw_material_prices = {
    "Europa":       {"water": 3.0225, "electricity": 0.186,  "silicon": 1.928},
    "Amerika":      {"water": 1.1625, "electricity": 0.1349, "silicon": 2.5575},
    "Japan":        {"water": 0.3953, "electricity": 0.1581, "silicon": 1.302},
    "Asien-Pazifik":{"water": 0.558,  "electricity": 0.2558, "silicon": 1.953},
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

#Kosten pro Wafer je Region in Euro
kosten_übersicht = {
    "Europa": {
        "Wasser": 63.14,
        "Elektrizität": 80.57,
        "Gesamt": 143.7
    },
    "Amerika": {
        "Wasser": 80.16,
        "Elektrizität": 133.66,
        "Gesamt": 213.83
    },
    "Japan": {
        "Wasser": 2.33,
        "Elektrizität": 101.88,
        "Gesamt": 104.21
    },
    "Asien-Pazifik": {
        "Wasser": 179.87,
        "Elektrizität": 260.89,
        "Gesamt": 440.76
    }
}
# --- Länder zu Regionen Mapping ---
country_to_region = {
    "Norway": "Europa",
    "Norwegen": "Europa",
    "Finland": "Europa",
    "Finnland": "Europa",
    "Sweden": "Europa",
    "Schweden": "Europa",
    "Russia": "Europa",
    "Russland": "Europa",
    "Latvia": "Europa",
    "Lettland": "Europa",
    "Scotland": "Europa",
    "Schottland": "Europa",
    "Denmark": "Europa",
    "Dänemark": "Europa",
    "Ireland": "Europa",
    "Irland": "Europa",
    "England": "Europa",
    "Germany": "Europa",
    "Deutschland": "Europa",
    "Switzerland": "Europa",
    "Schweiz": "Europa",
    "Wales": "Europa",
    "Netherlands": "Europa",
    "Niederlande": "Europa",
    "Belgium": "Europa",
    "Belgien": "Europa",
    "France": "Europa",
    "Frankreich": "Europa",
    "Belarus": "Europa",
    "Weißrussland": "Europa",
    "Italy": "Europa",
    "Italien": "Europa",
    "Austria": "Europa",
    "Österreich": "Europa",
    "Slovakia": "Europa",
    "Slowakei": "Europa",
    "Slovenia": "Europa",
    "Slowenien": "Europa",
    "Czech Republic": "Europa",
    "Tschechien": "Europa",
    "Turkey": "Europa",
    "Türkei": "Europa",
    "Israel": "Europa",
    "Canada": "Amerika",
    "Kanada": "Amerika",
    "US": "Amerika",
    "USA": "Amerika",
    "Japan": "Japan",
    "China": "Asien-Pazifik",
    "Südchina": "Asien-Pazifik",
    "South Korea": "Asien-Pazifik",
    "Südkorea": "Asien-Pazifik",
    "Malaysia": "Asien-Pazifik",
    "Taiwan": "Asien-Pazifik",
    "United Arab Emirates": "Asien-Pazifik",
    "Vereinigte Arabische Emirate": "Asien-Pazifik",
    "India": "Asien-Pazifik",
    "Indien": "Asien-Pazifik",
    "Thailand": "Asien-Pazifik",
    "Singapore": "Asien-Pazifik",
    "Singapur": "Asien-Pazifik",
    "Brazil": "Amerika",
    "Brasilien": "Amerika",
    "Australia": "Asien-Pazifik",
    "Australien": "Asien-Pazifik",
    "Bulgaria": "Europa",
    "Bulgarien": "Europa"
}

# --- Annahmen zur Sonneneinstrahlung (kWh/m²/Jahr) je Land ---
# (Werte aus PVGIS, grob gerundet)
solar_radiation = {
    "Australia": 1800,
    "Austria": 1150,
    "Belarus": 1100,
    "Belgium": 1000,
    "Brazil": 1700,
    "Bulgaria": 1400,
    "Canada": 1200,
    "China": 1200,
    "Czech Republic": 1150,
    "Denmark": 1000,
    "England": 950,
    "Finland": 900,
    "France": 1200,
    "Germany": 1050,
    "India": 1700,
    "Ireland": 950,
    "Israel": 1900,
    "Italy": 1350,
    "Japan": 1100,
    "Latvia": 950,
    "Malaysia": 1600,
    "Netherlands": 1000,
    "Norway": 850,
    "Russia": 1000,
    "Scotland": 900,
    "Singapore": 1650,
    "Slovakia": 1150,
    "Slovenia": 1250,
    "South Korea": 1150,
    "Sweden": 900,
    "Switzerland": 1100,
    "Taiwan": 1400,
    "Thailand": 1650,
    "Turkey": 1600,
    "United Arab Emirates": 2000,
    "US": 1300,
    "Wales": 950
}

# Dictionary für die beste Strategie
anteil_fossil_23 = {
    "Australia": 0.6629,
    "Austria": 0.1452,
    "Belgium": 0.2411,
    "Canada": 0.1883,
    "Chile": 0.3558,
    "Colombia": 0.3174,
    "Costa Rica": 0.0498,
    "Czech Republic": 0.4474,
    "Denmark": 0.1130,
    "Estonia": 0.4530,
    "Finland": 0.0514,
    "France": 0.0769,
    "Germany": 0.4509,
    "Greece": 0.4914,
    "Hungary": 0.2767,
    "Iceland": 0.0002,
    "Ireland": 0.5454,
    "Israel": 0.8844,
    "Italy": 0.5464,
    "Japan": 0.6456,
    "Korea": 0.6089,
    "Latvia": 0.2230,
    "Lithuania": 0.1468,
    "Luxembourg": 0.0678,
    "Mexico": 0.7407,
    "Netherlands": 0.4799,
    "New Zealand": 0.1226,
    "Norway": 0.0110,
    "Poland": 0.7239,
    "Portugal": 0.2522,
    "Slovak Republic": 0.1509,
    "Slovenia": 0.2384,
    "Spain": 0.2799,
    "Sweden": 0.0061,
    "Switzerland": 0.0057,
    "Republic of Turkiye": 0.5787,
    "United Kingdom": 0.3632,
    "United States": 0.5971,
    "OECD Total": 0.4942,
    "Argentina": 0.6126,
    "Brazil": 0.0873,
    "People's Republic of China": 0.6470,
    "Egypt": 0.8802,
    "India": 0.7705,
    "Indonesia": 0.8196,
    "Kenya": 0.1028,
    "Morocco": 0.7632,
    "Senegal": 0.8507,
    "Singapore": 0.9483,
    "South Africa": 0.8705,
    "Thailand": 0.8114,
    "Ukraine": 0.3220,
    "Non-OECD Total": 0.6678,
    "Africa": 0.7528,
    "Non-OECD Americas": 0.2430,
    "Non-OECD Asia (including China)": 0.6781,
    "Non-OECD Europe and Eurasia": 0.6216,
    "Middle East": 0.9506,
    "IEA Total": 0.4960,
    "IEA and Accession/Association countries": 0.5881,
    "World": 0.6098
}

# --- Daten aus vorheriger Seite übernehmen (falls vorhanden) ---
#wafer_kosten = st.session_state.get("wafer_kosten", {})
#region_default = st.session_state.get("region", "Europa")
anzahl_wafer = st.session_state.get("num_wafers", 1000)
#gesamt_wafer_kosten = st.session_state.get("total_cost", 0)
#stromkosten = st.session_state.get("power_cost", 0)
currency_code = st.session_state.get("currency_code", "EUR")
#st.markdown(f"**Aktuelle Region:** {region_default} | **Anzahl Wafer:** {anzahl_wafer:,} | **Kosten/Wafer:** {gesamt_wafer_kosten:.6f} € | **Stromkosten pro Wafer:** {stromkosten:.6f} €")
# ----------------------
# Eingabefelder nebeneinander
# ----------------------
col1, col2, col3 = st.columns(3)

with col1:
    country_list_de = sorted([translation_dict.get(c, c) for c in wafer_data.keys()])
    selected_country_de = st.selectbox("Wähle ein Produktionsland:", country_list_de)

with col2:
    # Englischer Ländername für Zugriff auf wafer_data
    selected_country = translation_dict_rev.get(selected_country_de, selected_country_de)
    node_list = sorted(list(wafer_data[selected_country].keys()), key=lambda x: int(x))
    selected_node = st.selectbox("Wähle den Technologie-Node:", node_list)

with col3:
    desired_wafers = st.number_input("Produzierte Wafer", min_value=1, step=1, value=anzahl_wafer)

#Eingabedaten speichern
st.session_state["land"] = selected_country
st.session_state["wafer"] = desired_wafers


# ----------------------
# Berechnung & Ausgabe
# ----------------------
metrics = wafer_data[selected_country][selected_node]

co2 = desired_wafers * metrics["CO2"]
water = desired_wafers * metrics["Water"]
electricity = desired_wafers * metrics["Electricity"]

kosten_baum = 24 #€/t CO2 Kompensation
kosten_pv = 40 
kosten_zertifikat = 80
    
gesamt_t = co2 / 1000
anzahl_baeume = co2 / 10 # Einsparung CO2 Baum: 10kgeq/baum
anzahl_baeume_gerundet = math.ceil(anzahl_baeume)
sonne = solar_radiation.get(selected_country, 1000)
jahresertrag_pro_m2 = sonne
flaeche_pv = electricity / (jahresertrag_pro_m2 * 0.015) #PV-Wirkungsgrad ca. 15%
# --- Kostenberechnung ---
kosten_baeume = gesamt_t * kosten_baum 
kosten_pv_gesamt = gesamt_t * kosten_pv 
kosten_zertifikat = gesamt_t * kosten_zertifikat
kosten_pro_wafer_baeume = kosten_baeume / desired_wafers
kosten_pro_wafer_pv = kosten_pv_gesamt / desired_wafers
kosten_pro_wafer_zertifikat = kosten_zertifikat / desired_wafers

#Vergleichsgröße
fussballfeld_m2 = 7140  # durchschnittliche Fläche eines Fußballfelds in m²
anzahl_felder = flaeche_pv / fussballfeld_m2
badewanne_l = 150 # durchschnittliche Badewannenfüllmenge in Litern
anzahl_badewannen = water / badewanne_l  

#co2 zwischenspeichern
st.session_state["co2_eq_pro_wafer"] = co2 / desired_wafers  # CO2 pro Wafer in kg

st.success(f"Für **{desired_wafers} Wafer** in **{selected_country_de} ({solar_radiation.get(selected_country, 1000)}kWh/m²**, Node **{selected_node})** wird pro Jahr berechnet:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("CO2-Ausstoß", f"{co2:.0f} kg")
    st.metric("Stromverbrauch", f"{electricity:.0f} kWh")
    st.metric("Wasserverbrauch", f"{water:.0f} Liter")
            
with col2:
    st.metric("Benötigte Bäume", f"{anzahl_baeume_gerundet:} Bäume")
    st.metric("Benötigte PV-Fläche", f"{flaeche_pv:.0f} m²")
    st.metric("gefüllte Badewannen", f"{anzahl_badewannen:.1f}")

    
with col3:
    st.metric("Kosten Bäume", f"{kosten_baeume:.2f} €")
    st.metric("Fußballfelder" , f"{anzahl_felder:.1f}")
    
    
with col4:
    st.metric("Kosten Zertifikat", f"{kosten_zertifikat:.2f} €")
    st.metric("Kosten PV-Fläche", f"{kosten_pv_gesamt:.2f} €")

            
st.markdown("---")
st.subheader("Vergleich: Andere Länder für denselben Node-Typ")

comparison = []
for country, nodes in wafer_data.items():
    if selected_node in nodes:
        m = nodes[selected_node]
        country_de = translation_dict.get(country, country)
        comparison.append({
            "Land": country_de,
            "CO2 (kg)": desired_wafers * m["CO2"],
            "Wasser (L)": desired_wafers * m["Water"],
            "Strom (kWh)": desired_wafers * m["Electricity"]
        })

comparison_df = (
    pd.DataFrame(comparison)
    .sort_values("CO2 (kg)")
    .set_index("Land")
)

st.dataframe(
comparison_df.style.apply(
lambda x: ['background-color: lightblue' if x.name == selected_country_de else '' for _ in x], axis=1
).format("{:.0f}"), 
use_container_width=True
)



# Hinweis in Sidebar
st.sidebar.markdown("---")
st.sidebar.info("Diese Werte basieren auf historischen Daten und Durchschnittswerten pro Node und Land. Tatsächliche Werte können je nach Fertigung variieren.")

# ----------------------
# Kompensationsrechner 
# ----------------------

# --- BASISDATEN aus Session ---
basis_zwischen = kosten_übersicht.get(country_to_region.get(selected_country_de, "Australien"))
basis_kosten_pro_wafer = basis_zwischen.get("Gesamt", 0)
basis_kosten_strom_pro_wafer = basis_zwischen.get("Elektrizität", 0)


# st.markdown(f"Gesamtkosten für {anzahl_wafer:,} Wafer: {gesamt_wafer_kosten:.2f} €") # überprüfung Übergabe
# st.markdown(f"Basis-Kosten pro Wafer: {basis_kosten_pro_wafer} €")



# --- Standard-Gestehungskosten (€/kWh) PV ---
# Grobe Annahme: 0.04 €/kWh bei Eigenverbrauch (konstant)
pv_kosten_kwh = 0.04

# --- Stromkosten aus Session laden (€/kWh) ---
stromkosten_wafer = basis_kosten_strom_pro_wafer  # €/Wafer

# Hole die Region basierend auf dem ausgewählten Land
region = country_to_region.get(selected_country_de, "Europa")  # Fallback auf "Europa"

# Hole den Verbrauch aus dem entsprechenden Regionseintrag
stromverbrauch_kwh = verbrauch_daten_pro_wafer.get(region, {}).get("electricity_kwh", 0)

# --- Übergabevariablen ---
anzahl_wafer = desired_wafers
land = st.session_state.get("land", "Germany")
co2_eq_wafer = st.session_state.get("co2_eq_pro_wafer", 359)
co2_gesamt = co2_eq_wafer * anzahl_wafer

# --- Diagramm: Gesamtkosten mit Kompensationsmix ---
st.subheader("Vergleich: Kompensationskosten")

strategien = ["🪙 Zertifikate", "☀️ PV", "🌳 Bäume", "⚖️ Mix"]
zeige_basis_mix = st.checkbox(
    "Basis-Waferkosten aus Wafer Kostenrechner übernehmen und im Diagramm mit anzeigen", value=False
)

# Einzelkosten pro Wafer
kosten_bäume_100_wafer = gesamt_t * kosten_baum / anzahl_wafer
kosten_pv_100_wafer = gesamt_t * kosten_pv / anzahl_wafer
# kosten_mix_pv = kosten_pv_100_wafer * (strategie / 100)
# kosten_mix_baum = kosten_bäume_100_wafer * ((100 - strategie) / 100)
# kosten_mix_pro_wafer = kosten_mix_pv + kosten_mix_baum

# Schritt 1: Daten sammeln
data = [
    {"Strategie": "🪙 Zertifikate", "Wert": kosten_pro_wafer_zertifikat, "Typ": "einzeln", "Farbe": "red"},
    {"Strategie": "☀️ PV", "Wert": kosten_pv_100_wafer, "Typ": "einzeln", "Farbe": "#F4D35E"},
    {"Strategie": "🌳 Bäume", "Wert": kosten_bäume_100_wafer, "Typ": "einzeln", "Farbe": "seagreen"},
]

df = pd.DataFrame(data).sort_values(by="Wert", ascending=False)

# Schritt 2: Balkendiagramm erstellen
fig_mixed = go.Figure()

# Optional: Basis-Waferkosten
if zeige_basis_mix:
    fig_mixed.add_trace(go.Bar(
        name="Basis-Waferkosten",
        y=df["Strategie"],
        x=[basis_kosten_pro_wafer] * len(df),
        orientation='h',
        marker_color='lightgray'
    ))

# Schritt 3: Balken hinzufügen
for _, row in df.iterrows():
    if row["Typ"] == "mix":
        # Mix als gestapelten Balken aus PV + Baum
        fig_mixed.add_trace(go.Bar(
            name="Mix - PV",
            y=[row["Strategie"]],
            x=[kosten_mix_pv],
            orientation='h',
            marker_color='#F4D35E',
            showlegend=False
        ))
        fig_mixed.add_trace(go.Bar(
            name="Mix - Bäume",
            y=[row["Strategie"]],
            x=[kosten_mix_baum],
            orientation='h',
            marker_color='seagreen',
            showlegend=False
        ))
    else:
        fig_mixed.add_trace(go.Bar(
            name=row["Strategie"],
            y=[row["Strategie"]],
            x=[row["Wert"]],
            orientation='h',
            marker_color=row["Farbe"]
        ))

# Layout
fig_mixed.update_layout(
    barmode='stack',
    xaxis_title="€ / Wafer",
    yaxis_title="Kompensationsstrategie",
    height=420
)

st.plotly_chart(fig_mixed, use_container_width=True)

# --- Strategie-Slider ---
st.title(f"CO₂-Kompensation Strategie Empfehlung")
st.markdown(f"für {selected_country_de} und Node **{selected_node}**")
# Test Übergabe
# st.markdown(f"**Basis-Kosten pro Wafer in {selected_country_de}**")
# st.markdown(f"**{country_to_region.get(selected_country_de, 'Europa')}:**")
# st.markdown(f"**{basis_zwischen}**")
# st.markdown(f"**{basis_kosten_pro_wafer:.2f} €**")
# st.markdown(f"**Basis-Kosten Strom pro Wafer {basis_kosten_strom_pro_wafer:.2f} €**")
# st.markdown(f"Stromverbrauch {stromverbrauch_kwh}")



#strategie = st.slider("Wähle deinen Kompensationsmix", 0, 100, 50, step=5, help="0% = Nur Bäume | 100% = Nur PV-Fläche")
# st.markdown("""
#     <div style='display: flex; justify-content: space-between; font-size: 18px;'>
#         <span>🌳 100% Bäume</span>
#         <span>⚖️ Mix</span>
#         <span>☀️ 100% PV</span>
#     </div>
#     """, unsafe_allow_html=True)

# anteil_pv = strategie
# anteil_baum = 100 - strategie

# --- Kostenparameter ---
# kosten_baum = 24 #€/t CO2 Kompensation
# kosten_pv = 40 
# kosten_zertifikat = 80


# --- Kostenberechnung ---
# kosten_baeume = gesamt_t * kosten_baum * ((100 - strategie) / 100)
# kosten_pv_gesamt = gesamt_t * kosten_pv * (strategie / 100)
#kosten_zertifikat = gesamt_t * kosten_zertifikat

# kosten_pro_wafer_baeume = kosten_baeume / anzahl_wafer
# kosten_pro_wafer_pv = kosten_pv_gesamt / anzahl_wafer
# kosten_pro_wafer_zertifikat = kosten_zertifikat / anzahl_wafer

# --- Anzeigeoptionen ---
# zeige_pro_wafer = st.checkbox("💡 Kosten pro Wafer anzeigen", value=True)

# col1, col2, col3 = st.columns(3)
# col1.metric("🌳 Bäume nötig", f"{anzahl_baeume_gerundet} Stück")
# col2.metric("☀️ PV-Fläche", f"{flaeche_pv:.0f} m²")

# col1, col2, col3 = st.columns(3)
# if zeige_pro_wafer:
#     col1.metric("🌳 Bäume", f"{kosten_pro_wafer_baeume:.2f}".replace(".", ",") + " €")
#     col2.metric("☀️ PV", f"{kosten_pro_wafer_pv:.2f}".replace(".", ",") + " €")
#     col3.metric("🪙 Zertifikate", f"{kosten_pro_wafer_zertifikat:.2f}".replace(".", ",") + " €")
# else:
#     col1.metric("🌳 Bäume", f"{kosten_baeume:.2f}".replace(".", ",") + " €")
#     col2.metric("☀️ PV", f"{kosten_pv_gesamt:.2f}".replace(".", ",") + " €")
#     col3.metric("🪙 Zertifikate", f"{kosten_zertifikat:.2f}".replace(".", ",") + " €")

# --- Eigenverbrauch PV-Rechnung ---
sonne = solar_radiation.get(land, 1000)
jahresertrag_pro_m2 = sonne * 0.8
waferbedarf_pv_kwh = stromverbrauch_kwh * anzahl_wafer
benötigte_flaeche_m2 = waferbedarf_pv_kwh / jahresertrag_pro_m2

neue_stromkosten_total = waferbedarf_pv_kwh * pv_kosten_kwh
neue_stromkosten_pro_wafer = neue_stromkosten_total / anzahl_wafer
einsparung_wafer = stromkosten_wafer - neue_stromkosten_pro_wafer


#st.caption(f"Basierend auf einer jährlichen Globalstrahlung von **{sonne} kWh/m²** in {translation_dict.get(land)}.")

# --- Fossilen Stromanteil ersetzen (zielgerichtete Strategie) ---
strahlung = solar_radiation.get(land)

if strahlung:
    strombedarf_total = anzahl_wafer * stromverbrauch_kwh
    fossil_anteil = anteil_fossil_23.get(land, anteil_fossil_23["World"])
    fossil_strom_kwh = strombedarf_total * fossil_anteil

    strom_ertrag_pro_m2 = strahlung * 0.15
    pv_flaeche = fossil_anteil * flaeche_pv / anzahl_wafer
    co2_durch_fossil = fossil_strom_kwh * (co2_eq_wafer / stromverbrauch_kwh)
    kosten_fossil_pv = (co2_durch_fossil / 1000) * (kosten_pv/1000 )

    rest_co2 = co2_eq_wafer * anzahl_wafer - co2_durch_fossil
    kosten_fossil_baum = (rest_co2 / 1000) * kosten_baum
    anzahl_baeume = rest_co2 / 10 / anzahl_wafer
    kosten_gesamt = kosten_fossil_pv + kosten_fossil_baum
    kosten_pv_kompensation = pv_flaeche * (kosten_pv_gesamt/flaeche_pv)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔌 Fossiler Stromanteil", f"{fossil_anteil*100:.1f} %")
    col2.metric("☀️ Benötigte PV-Fläche/Wafer", f"{pv_flaeche:.2f} m²")
    col3.metric("Kosten PV-Kompensation", f"{kosten_pv_kompensation:.2f} €")

    col1, col2, col3 = st.columns(3)


    #st.success(f"💶 Gesamtkosten der zielgerichteten Kompensation: **{kosten_gesamt:.2f} €**")

# --- Berechnung neuer Stromkosten & Kompensation ---
if strahlung:
    fossil_anteil = anteil_fossil_23.get(land, anteil_fossil_23["World"])
    strombedarf_total = anzahl_wafer * stromverbrauch_kwh
    fossil_strom_kwh = strombedarf_total * fossil_anteil
    power_cost_per_wafer = stromkosten_wafer
    stromkosten_alt = power_cost_per_wafer * anzahl_wafer

    strom_ertrag_pro_m2 = strahlung * 0.15
    pv_flaeche_fossil = fossil_strom_kwh / strom_ertrag_pro_m2

    co2_fossil = fossil_strom_kwh * (co2_eq_wafer / stromverbrauch_kwh)
    kosten_pv_fossil = (co2_fossil / 1000) * kosten_pv

    strombedarf_kauf_rest = strombedarf_total - fossil_strom_kwh
    stromkosten_neu = strombedarf_kauf_rest * (power_cost_per_wafer / stromverbrauch_kwh)
    kosten_strom_gesamt_neu = stromkosten_neu + (kosten_pv_fossil / 30)

    co2_total = co2_eq_wafer * anzahl_wafer
    co2_rest = co2_total - co2_fossil
    anzahl_baeume_rest = co2_rest / 10
    kosten_baeume_rest = (co2_rest / 1000) * kosten_baum

    kosten_gesamt_kompensation = kosten_pv_fossil + kosten_baeume_rest
    gesparte_kosten_pv = stromkosten_alt - stromkosten_neu

    zeige_pro_wafer = st.checkbox("💡 Kosten & CO₂ pro Wafer anzeigen", value=True)

    if zeige_pro_wafer:
        stromkosten_alt_anzeige = stromkosten_alt / anzahl_wafer
        kosten_strom_gesamt_neu_anzeige = kosten_strom_gesamt_neu / anzahl_wafer
        co2_fossil_anzeige = co2_fossil / anzahl_wafer
        co2_rest_anzeige = co2_rest / anzahl_wafer
        kosten_gesamt_kompensation_anzeige = kosten_gesamt_kompensation / anzahl_wafer
        einheit = "pro Wafer"
    else:
        stromkosten_alt_anzeige = stromkosten_alt
        kosten_strom_gesamt_neu_anzeige = kosten_strom_gesamt_neu
        co2_fossil_anzeige = co2_fossil
        co2_rest_anzeige = co2_rest
        kosten_gesamt_kompensation_anzeige = kosten_gesamt_kompensation
        einheit = f"{anzahl_wafer} Wafer"

    st.markdown(f"""
 **Optimale Strategie**: Ersetze den **fossilen Anteil ({fossil_anteil*100:.1f} % in {translation_dict[land]})** des Stroms durch PV.

🔌 **Alte Stromkosten ({einheit})**: {stromkosten_alt_anzeige:.2f} €  
☀️ **Neue Stromkosten ({einheit})**: {kosten_strom_gesamt_neu_anzeige:.2f} € (inkl. Investition PV, 30 Jahre Lebensdauer)
""")
     
wafer_kosten_nach_kompensation = basis_kosten_pro_wafer - (gesparte_kosten_pv/desired_wafers)
kosten_ersparnis = 1- (wafer_kosten_nach_kompensation/basis_kosten_pro_wafer )
st.markdown(f""" {wafer_kosten_nach_kompensation:.2f} € **Kosten pro Wafer nach PV-Kompensation**""")
st.markdown(f"""💰 Kostenreduktion pro Wafer {kosten_ersparnis*100:.2f} %""")