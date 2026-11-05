
import chromadb
import ollama

from pathlib import Path
import memory

# Configurações
BASE_DIR = Path(__file__).parent
CHROMA_DIR = BASE_DIR / "database" / "chroma"

EMBEDDING_MODEL = "embeddinggemma"

# Banco vetorial persistente
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Coleção de memórias
collection = client.get_or_create_collection(
    name="user_memories",
    metadata={"hnsw:space": "cosine"}
)


def generate_embedding(text, is_query=False):

    if is_query:
        prepared_text = (
            f"task: search result | query: {text}"
        )
    else:
        prepared_text = (
            f"title: none | text: {text}"
        )

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=prepared_text
    )

    return response.embeddings[0]

def index_memory(memory_id, content, created_at=None):

    embedding = generate_embedding(content)

    collection.upsert(
        ids=[str(memory_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{
            "created_at": created_at or ""
        }]
    )


def search_memories(query, limit=5, max_distance=0.45):

    if collection.count() == 0:
        return []

    query_embedding = generate_embedding(
        query,
        is_query=True
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(limit, collection.count()),
        include=["documents", "distances", "metadatas"]
    )

    memories = []

    for i, document in enumerate(results["documents"][0]):

        distance = results["distances"][0][i]

        # Filtra resultados pouco relevantes
        if distance > max_distance:
            continue

        memories.append({
            "content": document,
            "distance": distance,
            "metadata": results["metadatas"][0][i]
        })

    return memories


def sync_sqlite_memories():

    saved_memories = memory.get_memories()

    if not saved_memories:
        return

    # Identifica quais memórias já foram indexadas
    ids = [str(item[0]) for item in saved_memories]

    existing = set(
        collection.get(
            ids=ids,
            include=[]
        )["ids"]
    )

    # Indexa somente as memórias que ainda não existem
    for item in saved_memories:

        memory_id, content, created_at = item

        if str(memory_id) in existing:
            continue

        index_memory(
            memory_id,
            content,
            created_at
        )

    print("[VECTOR] Sincronização concluída.")


def delete_vector_memory(memory_id):

    collection.delete(
        ids=[str(memory_id)]
    )
