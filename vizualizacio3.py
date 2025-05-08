import plotly.express as px
import pandas as pd
import json

# JSON fájl beolvasása
file_path = r"C:\\Users\\moraa\\Desktop\\Aronegyetem\\Mesteri\\II. felev\\Adat vizualizacio\\Cursor\\San Francisco\\San_Francisco.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Adatok dataframe-be konvertálása
df = pd.DataFrame(data)

# A 'Passenger Count' oszlop numerikus értékre konvertálása
df["Passenger Count"] = pd.to_numeric(df["Passenger Count"], errors="coerce")

# Az adatok aggregálása (célállomás, szélesség, hosszúság, és utasszám alapján)
df_map = df.groupby(["Destination", "Latitude", "Longitude"], as_index=False)["Passenger Count"].sum()

# Térkép létrehozása
fig = px.scatter_geo(
    df_map,
    lat="Latitude",
    lon="Longitude",
    hover_name="Destination",
    size="Passenger Count",
    projection="natural earth",  # Különböző vetületek próbálhatók ki
    title="San Francisco-ból induló járatok célállomásai",
    color="Passenger Count",
    color_continuous_scale="Viridis",  # Szép színskála a pontokhoz
    scope="world"  # Globális térkép
)

# Térkép finomhangolása: geográfiai beállítások
fig.update_geos(
    visible=True,
    projection_type="natural earth",  # Különböző vetületek próbálhatók ki
    center={"lat": 0, "lon": 0},  # A térkép középpontját a Föld középpontjára állítjuk
    projection_scale=1,  # Ez biztosítja, hogy a teljes Föld látszódjon
    showland=True,  # A szárazföldek láthatóak legyenek
    landcolor="white",  # Szárazföldek fehérek legyenek
    oceancolor="lightgray",  # Óceán színe világos szürke legyen
    showcoastlines=True,  # Tengerpartok láthatósága
    coastlinecolor="white",  # Tengerpartok fehérek legyenek
    coastlinewidth=2,  # Tengerpartok szélessége
    showcountries=True,  # Országhatárok láthatóak legyenek
    countrycolor="white",  # Országhatárok színe fehér
    showocean=True,  # Óceánok legyenek láthatóak
)

# A hoverban ne jelenjenek meg a latitude, longitude, csak a Passenger Count
fig.update_traces(
    hovertemplate="<b>Destination</b>: %{hovertext}<br><b>Utasok száma</b>: %{marker.size}<extra></extra>"
)

# HTML fájlba mentés
fig.write_html("san_francisco_jaratok_terkep_normalis_szinezes_v2.html")

print("HTML fájl sikeresen létrehozva: san_francisco_jaratok_terkep_normalis_szinezes_v2.html")
