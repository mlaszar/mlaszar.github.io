import pandas as pd
import json
import os
import plotly.graph_objects as go

# JSON fájl beolvasása
file_path = r"C:\\Users\\moraa\\Desktop\\Aronegyetem\\Mesteri\\II. felev\\Adat vizualizacio\\Cursor\\San Francisco\\San_Francisco.json"

with open(file_path, "r") as file:
    data = json.load(file)

# Az adatokat pandas DataFrame-be töltjük
df = pd.DataFrame(data)

# "Activity Period Start Date" mezőt datetime típusra konvertáljuk
df['Activity Period Start Date'] = pd.to_datetime(df['Activity Period Start Date'], format='%m/%d/%y')

# A hónap és év extrakciója
df['Year'] = df['Activity Period Start Date'].dt.year
df['Month'] = df['Activity Period Start Date'].dt.month

# A 'Passenger Count' mezőt egész számra konvertáljuk
df['Passenger Count'] = df['Passenger Count'].replace(',', '', regex=True).astype(int)

# 2025-ös év adatainak eltávolítása
df = df[df['Year'] != 2025]

# Csoportosítás év és hónap szerint, és összesítés
monthly_totals = df.groupby(['Year', 'Month'])['Passenger Count'].sum().reset_index()

# A legforgalmasabb hónap keresése évenként
max_months = monthly_totals.loc[monthly_totals.groupby('Year')['Passenger Count'].idxmax()]

# Biztosítjuk, hogy a hónapok egész számok legyenek
max_months['Month'] = max_months['Month'].astype(int)

# A hónapok magyar nevei
months = ['Január', 'Február', 'Március', 'Április', 'Május', 'Június', 'Július', 'Augusztus', 'Szeptember', 'Október', 'November', 'December']

# A hónapok neveinek beállítása
max_months['Month Name'] = max_months['Month'].apply(lambda x: months[x-1])

# Színek hozzárendelése hónapokhoz
# Nyári hónapok (Június, Július, Augusztus) különböző színekkel
color_map = {
    1: 'rgb(100, 100, 255)',  # Január (téli)
    2: 'rgb(100, 100, 255)',  # Február (téli)
    3: 'rgb(0, 255, 255)',    # Március (tavaszi)
    4: 'rgb(0, 255, 255)',    # Április (tavaszi)
    5: 'rgb(0, 255, 0)',      # Május (tavaszi)
    6: 'rgb(255, 255, 0)',    # Június (nyári - sárga)
    7: 'rgb(255, 165, 0)',    # Július (nyári - narancs)
    8: 'rgb(255, 0, 0)',      # Augusztus (nyári - piros)
    9: 'rgb(255, 255, 0)',    # Szeptember (őszi)
    10: 'rgb(255, 255, 0)',   # Október (őszi)
    11: 'rgb(255, 165, 0)',   # November (őszi)
    12: 'rgb(0, 0, 255)'      # December (téli)
}

# Színek alkalmazása az adatokra
max_months['Color'] = max_months['Month'].map(color_map)

# Interaktív bar chart készítése plotly-val
fig = go.Figure(go.Bar(
    x=max_months['Year'].astype(str),
    y=max_months['Passenger Count'],
    text=max_months['Month Name'],
    hoverinfo='text+y',
    marker=dict(
        color=max_months['Color'],
        showscale=False  # Nem szükséges színskála
    )
))

# Címek és tengelyek hozzáadása
fig.update_layout(
    title='Legforgalmasabb hónapok évenkénti trendje',
    xaxis_title='Év',
    yaxis_title='Utasszám',
    xaxis_tickangle=45
)

# A HTML fájl elmentése ugyanabban a könyvtárban, mint a JSON fájl
html_file_path = os.path.join(os.path.dirname(file_path), "interactive_monthly_trends_v3.html")

# Grafikon mentése HTML fájlként
fig.write_html(html_file_path)

print(f"Eredmény sikeresen elmentve: {html_file_path}")
