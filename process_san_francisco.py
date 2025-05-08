import json

file_path = r"C:\Users\moraa\Desktop\Aronegyetem\Mesteri\II. felev\Adat vizualizacio\Cursor\San Francisco\San_Francisco.json"

# Új Dél-Amerika rekord
south_america_record = {
    "GEO Region": "South America",
    "Destination": "South America",
    "Latitude": -25.2637,
    "Longitude": -57.5759,
    "Passenger Count": 125095
}

# Fájl betöltése
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Hozzáadás
data.append(south_america_record)

# Mentés
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Dél-Amerika rekord hozzáadva.")
