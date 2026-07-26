import os
import fitz
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

PDF_FOLDER = "data/medical_books"
VECTOR_FOLDER = "vector_db"

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append(
            {
                "page": page_number + 1,
                "text": text
            }
        )

    document.close()

    return pages


def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(text[i:i + chunk_size])

    return chunks


def create_vector_database():

    metadata = []

    print("\nLoading Medical PDFs...\n")

    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            print("Reading:", file)

            pdf_path = os.path.join(PDF_FOLDER, file)

            pages = extract_text(pdf_path)

            for page in pages:

                chunks = split_text(page["text"])

                for chunk in chunks:

                    metadata.append(
                        {
                            "text": chunk,
                            "source": file,
                            "page": page["page"]
                        }
                    )

    print("\nTotal Chunks :", len(metadata))

    print("\nCreating Embeddings...")

    texts = [item["text"] for item in metadata]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    os.makedirs(VECTOR_FOLDER, exist_ok=True)

    faiss.write_index(
        index,
        os.path.join(VECTOR_FOLDER, "medical.index")
    )

    with open(
        os.path.join(VECTOR_FOLDER, "metadata.pkl"),
        "wb"
    ) as f:

        pickle.dump(metadata, f)

    print("\n✅ Vector Database Created Successfully")


if __name__ == "__main__":

    create_vector_database()