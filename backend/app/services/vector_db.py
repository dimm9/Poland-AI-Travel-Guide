import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.embedding_func = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="trips_collection",
            embedding_function=self.embedding_func
        )

    def add_trips(self, trips: list):
        # dodaje listwe wycieczek do bazy wektorowej
        ids = []
        documents = []
        metadatas = []

        for trip in trips:
            ids.append(trip["id"])
            doc_text = f"Tytul: {trip['title']}, Opis: {trip['description']}, Tagi: {', '.join(trip['tags'])})"
            documents.append(doc_text)
            metadatas.append({
                "title": trip["title"],
                "price_pln": trip["price_pln"],
                "location": trip["location"],
                "lat": trip["lat"],
                "lng": trip["lng"],
            })
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Dodano {len(ids)} wycieczek do bazy wektorowej.")

    def search(self, query: str, n_results: int = 3):
        # szuka wycieczek na podstawie jezyka naturalnego
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
vector_db = VectorDB()