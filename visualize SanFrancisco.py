
import pandas as pd
import matplotlib.pyplot as plt

# JSON fájl betöltése
df = pd.read_json(r'C:\Users\moraa\Desktop\Aronegyetem\Mesteri\II. felev\Adat vizualizacio\Cursor\San Francisco\San_Francisco.json')

# Az adatok első pár sorának megjelenítése
print(df.head())

# Diagram megjelenítése
df.plot(kind='bar', x='Operating Airline', y='Passenger Count')
plt.show()
