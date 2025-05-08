import pandas as pd
import plotly.express as px
import json

# Fájl elérési út
file_path = r"C:\Users\moraa\Desktop\Aronegyetem\Mesteri\II. felev\Adat vizualizacio\Cursor\San Francisco\San_Francisco.json"

# JSON beolvasása
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# DataFrame létrehozása
df = pd.DataFrame(data)

# Utasszám formázás (vesszők eltávolítása, konvertálás)
df['Passenger Count'] = df['Passenger Count'].str.replace(',', '')
df['Passenger Count'] = pd.to_numeric(df['Passenger Count'], errors='coerce')

# Érvényes adatok kiszűrése
df = df.dropna(subset=['Passenger Count', 'Operating Airline'])

# Kumulált utasszám számítása
agg = df.groupby('Operating Airline', as_index=False)['Passenger Count'].sum()

# Top 20 légitársaság
top20 = agg.sort_values(by='Passenger Count', ascending=False).head(20)

# Interaktív bar chart készítése
fig = px.bar(
    top20,
    x='Operating Airline',
    y='Passenger Count',
    title='Top 20 légitársaság kumulált utasszám alapján',
    labels={'Operating Airline': 'Légitársaság', 'Passenger Count': 'Kumulált utasszám'},
    color='Passenger Count',
    color_continuous_scale='Plasma'
)

fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title='Légitársaság',
    yaxis_title='Utasok száma',
    plot_bgcolor='white',
    height=600
)

# HTML fájlba mentés
output_html_path = r"C:\Users\moraa\Desktop\top20_legitarsasagok.html"
fig.write_html(output_html_path)

print(f"Az interaktív diagram sikeresen elmentve ide: {output_html_path}")
