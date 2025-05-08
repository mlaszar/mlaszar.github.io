import pandas as pd
import plotly.graph_objects as go
import json
import os

# Fájl útvonala
file_path = r"C:\\Users\\moraa\\Desktop\\Aronegyetem\\Mesteri\\II. felev\\Adat vizualizacio\\Cursor\\San Francisco\\San_Francisco.json"

# JSON betöltése
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Csak belföldi
df = df[df["Destination"] == "US"]

# Dátum feldolgozás
df["Date"] = pd.to_datetime(df["Activity Period Start Date"], format="%m/%d/%y")
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month Name"] = df["Date"].dt.strftime('%B')
df["Passenger Count"] = df["Passenger Count"].replace(",", "", regex=True).astype(int)

# Csak 2024-ig
df = df[df["Year"] < 2025]

# Hónap sorrend
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df["Month Name"] = pd.Categorical(df["Month Name"], categories=month_order, ordered=True)

# Aggregált adatok
agg_df = df.groupby(["Year", "Month Name"], as_index=False)["Passenger Count"].sum()

# Színskála: hideg -> meleg
color_map = {
    "January": "#1f77b4",     # Kék
    "February": "#17becf",    # Türkiz
    "March": "#2ca02c",       # Zöld
    "April": "#bcbd22",       # Sárgászöld
    "May": "#ffbb78",         # Világos narancs
    "June": "#ff7f0e",        # Narancs
    "July": "#d62728",        # Piros
    "August": "#e377c2",      # Rózsaszín
    "September": "#9467bd",   # Lila
    "October": "#8c564b",     # Barna
    "November": "#7f7f7f",    # Szürke
    "December": "#1f77b4"     # Hideg kék (mint Január)
}

# Interaktív vonaldiagram létrehozása
fig = go.Figure()

# Egy vonal minden hónapra: y = utasszám, x = év
for month in month_order:
    month_df = agg_df[agg_df["Month Name"] == month]
    fig.add_trace(go.Scatter(
        x=month_df["Year"],
        y=month_df["Passenger Count"],
        mode="lines+markers",
        name=month,
        line=dict(width=1.5, color=color_map.get(month, "gray")),
        visible=True
    ))

# Dropdown szűrő hónapok szerint
buttons = []
for i, month in enumerate(month_order):
    visible = [j == i for j in range(len(month_order))]
    buttons.append(dict(
        label=month,
        method="update",
        args=[{"visible": visible},
              {"title": f"{month} – éves utasforgalom"}]
    ))

# Összes hónap visszaállítása gomb
buttons.insert(0, dict(
    label="Összes hónap",
    method="update",
    args=[{"visible": [True]*len(month_order)},
          {"title": "Havi utasforgalom – Évek szerint"}]
))

# Layout beállítása
fig.update_layout(
    title="Havi utasforgalom – Évek szerint",
    xaxis_title="Év",
    yaxis_title="Utasok száma",
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        showactive=True,
        x=1.1,
        y=1.15,
        xanchor="right",
        yanchor="top"
    )],
    height=600
)

# HTML mentés
output_html_path = os.path.splitext(file_path)[0] + "_vonaldiagram_ev_honap.html"
fig.write_html(output_html_path)

print(f"Vonaldiagram elmentve ide:\n{output_html_path}")
