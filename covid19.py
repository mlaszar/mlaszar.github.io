import pandas as pd
import plotly.express as px
import json

# Bemeneti fájl útvonala
file_path = r"C:\\Users\\moraa\\Desktop\\Aronegyetem\\Mesteri\\II. felev\\Adat vizualizacio\\Cursor\\San Francisco\\San_Francisco.json"

# Kimeneti HTML fájl útvonala
output_path = r"C:\\Users\\moraa\\Desktop\\Aronegyetem\\Mesteri\\II. felev\\Adat vizualizacio\\Cursor\\San Francisco\\passenger_comparison.html"

# JSON beolvasása
with open(file_path, 'r') as f:
    data = json.load(f)

# DataFrame létrehozása
df = pd.DataFrame(data)

# Dátum konvertálása
df['Activity Period Start Date'] = pd.to_datetime(
    df['Activity Period Start Date'], format='%m/%d/%y', errors='coerce'
)

# Év kivonása
df['Év'] = df['Activity Period Start Date'].dt.year

# Utasszám konvertálása számmá
df['Utasszám'] = df['Passenger Count'].replace(',', '', regex=True).astype(float)

# Éves összesítés
yearly_data = df.groupby('Év')['Utasszám'].sum().reset_index()

# Időszak címkézése
yearly_data['Időszak'] = yearly_data['Év'].apply(
    lambda x: 'Covid előtti' if 2015 <= x <= 2019 else 'Covid utáni' if 2020 <= x <= 2022 else 'Egyéb'
)

# Csak a kívánt évek megtartása
yearly_data = yearly_data[yearly_data['Időszak'].isin(['Covid előtti', 'Covid utáni'])]

# Interaktív vonaldiagram készítése
fig = px.line(
    yearly_data,
    x='Év',
    y='Utasszám',
    color='Időszak',
    markers=True,
    title='Covid előtti és utáni utasforgalom',
    hover_data={'Utasszám': ':.0f'}
)

fig.update_traces(mode='lines+markers')
fig.update_layout(
    xaxis_title='Év',
    yaxis_title='Utasszám',
    hovermode='x unified'
)

# HTML mentés
fig.write_html(output_path)
fig.show()
