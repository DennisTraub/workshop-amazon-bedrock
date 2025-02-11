import chromadb

from chromadb.utils import embedding_functions


# Helper function to initialize the vector DB with data
def initialize_vector_db():
    # Initialize with PersistentClient
    chrome_client = chromadb.PersistentClient(path="./data/vector_db")

    # Define embedding function
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Create or get the collection with the embedding function
    collection = chrome_client.get_or_create_collection(
        name="travel_info",
        embedding_function=embedding_function
    )

    travel_info = [
        "New York - January: High 4°C/39°F, Low -3°C/27°F, Precipitation 86mm/3.4in. Cold with snow and rain likely",
        "New York - February: High 6°C/43°F, Low -2°C/28°F, Precipitation 78mm/3.1in. Cold winter weather continues, mix of snow and rain",
        "New York - March: High 10°C/50°F, Low 2°C/36°F, Precipitation 101mm/4.0in. Milder temperatures, frequent rain showers",
        "New York - April: High 16°C/61°F, Low 7°C/45°F, Precipitation 106mm/4.2in. Spring weather with regular rainfall",
        "New York - May: High 22°C/72°F, Low 13°C/55°F, Precipitation 111mm/4.4in. Warm spring temperatures, occasional thunderstorms",
        "New York - June: High 27°C/81°F, Low 18°C/64°F, Precipitation 104mm/4.1in. Warm and humid, afternoon thunderstorms possible",
        "New York - July: High 29°C/84°F, Low 21°C/70°F, Precipitation 116mm/4.6in. Hot and humid, frequent thunderstorms",
        "New York - August: High 28°C/82°F, Low 20°C/68°F, Precipitation 111mm/4.4in. Hot and humid, thunderstorms common",
        "New York - September: High 24°C/75°F, Low 16°C/61°F, Precipitation 109mm/4.3in. Warm early fall weather, occasional rain",
        "New York - October: High 18°C/64°F, Low 10°C/50°F, Precipitation 96mm/3.8in. Mild fall temperatures, moderate rainfall",
        "New York - November: High 12°C/54°F, Low 5°C/41°F, Precipitation 91mm/3.6in. Cooling temperatures, mix of rain and occasional snow",
        "New York - December: High 6°C/43°F, Low 0°C/32°F, Precipitation 94mm/3.7in. Cold with mix of rain and snow",
        "New York - Events: Broadway Shows, schedule: Various, mostly Tuesday to Sunday",
        "New York - Events: Central Park Tours, schedule: Daily",
        "New York - Events: New York Fashion Week, schedule: September and February",
        "New York - Attractions: Statue of Liberty",
        "New York - Attractions: Empire State Building",
        "New York - Attractions: Metropolitan Museum of Art",
        "New York - Attractions: Times Square",
        "Barcelona - January: High 14°C/57°F, Low 5°C/41°F, Precipitation 41mm/1.6in. Mild winter temperatures, occasional rain",
        "Barcelona - February: High 15°C/59°F, Low 6°C/43°F, Precipitation 29mm/1.1in. Mild days, cool nights, lower rainfall",
        "Barcelona - March: High 17°C/63°F, Low 8°C/46°F, Precipitation 40mm/1.6in. Spring begins, moderate temperatures",
        "Barcelona - April: High 19°C/66°F, Low 10°C/50°F, Precipitation 48mm/1.9in. Pleasant spring weather, occasional showers",
        "Barcelona - May: High 22°C/72°F, Low 13°C/55°F, Precipitation 47mm/1.9in. Warm days, comfortable evenings",
        "Barcelona - June: High 26°C/79°F, Low 17°C/63°F, Precipitation 29mm/1.1in. Warm and sunny, low rainfall",
        "Barcelona - July: High 29°C/84°F, Low 20°C/68°F, Precipitation 22mm/0.9in. Hot and dry, perfect beach weather",
        "Barcelona - August: High 29°C/84°F, Low 20°C/68°F, Precipitation 62mm/2.4in. Hot with occasional thunderstorms",
        "Barcelona - September: High 26°C/79°F, Low 17°C/63°F, Precipitation 81mm/3.2in. Warm, highest rainfall of the year",
        "Barcelona - October: High 22°C/72°F, Low 14°C/57°F, Precipitation 91mm/3.6in. Mild temperatures, frequent rainfall",
        "Barcelona - November: High 17°C/63°F, Low 9°C/48°F, Precipitation 58mm/2.3in. Cooling temperatures, moderate rainfall",
        "Barcelona - December: High 14°C/57°F, Low 6°C/43°F, Precipitation 40mm/1.6in. Mild winter weather, occasional rain",
        "Barcelona - Events: La Mercè Festival, schedule: September",
        "Barcelona - Events: Primavera Sound, schedule: Late May/Early June",
        "Barcelona - Events: Sagrada Familia Tours, schedule: Daily",
        "Barcelona - Attractions: Sagrada Familia",
        "Barcelona - Attractions: Park Güell",
        "Barcelona - Attractions: Casa Batlló",
        "Barcelona - Attractions: La Rambla"
    ]

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
    chroma_client = chromadb.PersistentClient(path="./data/vector_db")

    # Define embedding function (default is OpenAI's text-embedding-ada-002)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Get or create the collection with the embedding function
    collection = chroma_client.get_or_create_collection(
        name="travel_info",
        embedding_function=embedding_function
    )

    # Query the collection
    results = collection.query(query_texts=[query], n_results=5)

    # Combine the retrieved chunks into a single context
    if results and "documents" in results and len(results["documents"]) > 0:
        items = []
        for result in results["documents"][0]:
            items.append(f"<travel-info>{result}</travel-info>")
        return "\n".join(items)
    return "No relevant travel info found"
