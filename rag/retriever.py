
import streamlit as st
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_FOLDER = "vector_db"


@st.cache_resource
def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(f"{VECTOR_FOLDER}/medical.index")

    with open(f"{VECTOR_FOLDER}/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    return model, index, metadata


model, index, metadata = load_resources()


def retrieve_context(question, top_k=5, distance_threshold=1.0):

    embedding = model.encode([question]).astype("float32")

    distances, indices = index.search(embedding, top_k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # Ignore unrelated chunks
        if distance > distance_threshold:
            continue

        results.append(metadata[idx])

    return results


if __name__ == "__main__":

    question = input("Ask : ")

    docs = retrieve_context(question)

    print()

    if len(docs) == 0:

        print("No relevant medical document found.")

    else:

        for doc in docs:

            print("=" * 60)

            print(doc["source"])

            print("Page :", doc["page"])

            print()

            print(doc["text"])

            print()



