import uuid
import chromadb
from services.embedding_service import get_embedding

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="resume_collection")

def store_resume_chunks(resume_id, candidate_name, chunks):
    ids, docs, embeddings, metadata = [], [], [], []

    for i, chunk in enumerate(chunks):
        ids.append(f"{resume_id}_{i}_{uuid.uuid4()}")
        docs.append(chunk["content"])
        embeddings.append(get_embedding(chunk["content"]))
        metadata.append({
            "resume_id": str(resume_id),
            "candidate_name": candidate_name,
            "section": chunk["section"]
        })

    if not docs:
        raise ValueError("No chunks found.")

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadata
    )

def retrieve_resume_chunks(resume_id, query, n_results=8):
    embedding = get_embedding(query)
    result = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={"resume_id": str(resume_id)}
    )
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]

    return [{"section": m["section"], "content": d} for d, m in zip(docs, metas)]
