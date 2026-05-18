import os
import json
from uuid import uuid4
from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embed_dense, load_dense_model, embed_sparse, load_sparse_model
from common.document_loader import load_document
from common.chunking import text_split

from labs.lab_04_hybrid_dense_sparse.create_hybrid_collection import ensure_collection_exists

def ingest(client: QdrantClient,
           dense_model,
           sparse_model,
           path: str,
           lang: str="vi"):
    collection_name=settings.dense_collection_name + "_lab04"

    pages = load_document(path)
    chunks = text_split(pages)

    chunks_content=[x.page_content for x in chunks]
    chunks_embedded = embed_dense(dense_model, chunks_content)
    sparse_chunks = embed_sparse(sparse_model, chunks_content)

    points=[]
    for i, (chunk, embedd, sparse_chunk) in enumerate(zip(chunks, chunks_embedded, sparse_chunks)):
        page = chunk.metadata.get("page")
        total_pages = chunk.metadata.get("total_pages")
        doc_type=os.path.splitext(path)[-1]
        
        point = models.PointStruct(
            id=str(uuid4()),
            vector={
                "dense": embedd.tolist(),
                "sparse": sparse_chunk
            },
            payload={
                "chunk_id": i,
                "file_name": os.path.basename(path),
                "text": chunk.page_content,
                "title": chunk.metadata.get("title", os.path.basename(path)),
                "source": path,
                "doc_type": doc_type,
                "page": f"{page}/{total_pages}",
                "metadata": chunk.metadata,
                "lang": lang,
                "is_deleted": False
            }
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )
    print(f"Uploaded {len(points)} points from {path}")
 

if __name__ == "__main__":
    BASE_DIR="data/raw/sample_docs"
    collection_name=settings.dense_collection_name + "_lab06"
    
    client = QdrantClient(path=settings.qdrant_path)
    ensure_collection_exists(client)

    client.create_payload_index(
        collection_name=collection_name,
        field_name="file_name",
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            lowercase=True
        ),
        wait=True
)

    dense_model=load_dense_model()
    sparse_model=load_sparse_model()

    for file in os.listdir(BASE_DIR):
        path=os.path.join(BASE_DIR,file)
        if not os.path.isfile(path):
            continue
        ingest(client, dense_model, sparse_model, path)

    client.close()