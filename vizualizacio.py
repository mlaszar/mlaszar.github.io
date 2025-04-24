import json
import pandas as pd
import matplotlib.pyplot as plt

# JSON beolvasása
with open(r"C:\\Users\\Vand golf 4\\Downloads\\data\\San_Francisco.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Átalakítás DataFrame-re
df = pd.DataFrame(data)

# Dátum átalakítása időformátumra
df["Activity Period Start Date"] = pd.to_datetime(df["Activity Period Start Date"])

# Szűrés 1999. júliusra
july_data = df[df["Activity Period Start Date"] == "1999-07-01"]

# Utasszám összegzése régió szerint
grouped = july_data.groupby("GEO Region")["Passenger Count"].sum().sort_values(ascending=False)

# Diagram kirajzolása
plt.figure(figsize=(10, 6))
grouped.plot(kind="bar", color="skyblue")
plt.title("Utasok száma régiónként - 1999. július")
plt.xlabel("Régió")
plt.ylabel("Utasok száma")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
