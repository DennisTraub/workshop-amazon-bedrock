import chromadb

from chromadb.utils import embedding_functions

from app.config import vector_db_folder, travel_info


# Helper function to initialize the vector DB with data
def initialize_vector_db():
    # Initialize with PersistentClient
    chrome_client = chromadb.PersistentClient(path=vector_db_folder)

    # Define embedding function
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Create or get the collection with the embedding function
    collection = chrome_client.get_or_create_collection(
        name="travel_info",
        embedding_function=embedding_function
    )

    ids = [f"doc_{i}" for i in range(len(travel_info))]
    metadatas = [{"source": "travel_info"} for _ in travel_info]

    # Add documents to the collection
    collection.add(
        ids=ids,
        documents=travel_info,
        metadatas=metadatas
    )

# Helper function to retrieve relevant data from the vector DB
def retrieve_from_vector_db(query):
    # Create a ChromaDB client
    chroma_client = chromadb.PersistentClient(path=vector_db_folder)

    # Define embedding function (default is OpenAI's text-embedding-ada-002)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Get or create the collection with the embedding function
    collection = chroma_client.get_or_create_collection(
        name="travel_info",
        embedding_function=embedding_function
    )

    # Query the collection
    results = collection.query(query_texts=[query], n_results=3)

    # Combine the retrieved chunks into a single context
    if results and "documents" in results and len(results["documents"]) > 0:
        items = []
        for result in results["documents"][0]:
            items.append(f"<travel-info>{result}</travel-info>")
        return "\n".join(items)
    return "No relevant travel info found"
