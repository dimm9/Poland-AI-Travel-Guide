import json
import os
import sys

# __file__ - sciezka do biezacego pliku
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vector_db import vector_db

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "raw_trips.json")

    if not os.path.exists(json_path):
        print(f"Plik {json_path} nie istnieje")
        return 
    
    with open(json_path, "r", encoding="utf-8") as f:
        trips = json.load(f)
    vector_db.add_trips(trips)
    print("dane wczytane z jsona i zapisane w bazie chromaDB")

    # test
    print("Test wyszukiwania w bazie wektorowej:")
    query = "Gdzie pojechać z psem, żeby było blisko natury?"
    results = vector_db.search(query, n_results=3)
    print("QUERY:", query)
    if results and results['metadatas'][0]:
        best_match = results['metadatas'][0][0]
        print(f"\nNajlepsze dopasowanie: {best_match['title']} ({best_match['location']})")
    else:
        print("Nie znaleziono wynikow")

if __name__ == "__main__":
    load_data()