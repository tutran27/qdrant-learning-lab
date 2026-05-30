from uuid import uuid4

from qdrant_client import QdrantClient, models
from common.embedding import load_colbert_model, load_dense_model, load_sparse_model, embed_colbert, embed_dense, embed_sparse
from common.config import settings
from common.document_loader import load_document
from common.chunking import text_split

from labs.lab_09_eval_retrieval.ensure_collection import ensure_colbert_collection

COLLECTION_NAME = f"{settings.dense_collection_name}_lab09"
def ingest_multi_vector(client, path, dense_model, sparse_model, colbert_model, collection_name=COLLECTION_NAME, lang:str="vi"):
    pages=load_document(path)
    chunks=text_split(pages)
    print(f"Loaded {len(chunks)} chunks")
    
    chunks_content = [chunk.page_content for chunk in chunks ]
    dense_embeddings = embed_dense(dense_model, chunks_content)
    sparse_embeddings = embed_sparse(sparse_model, chunks_content)
    colbert_embeddings = list(embed_colbert(colbert_model, chunks_content))
    points=[]
    for i, (chunk, dense_emb) in enumerate(zip(chunks, dense_embeddings)):
        page = chunk.metadata.get("page")
        total_pages = chunk.metadata.get("total_pages")
        doc_type=os.path.splitext(path)[-1]

        point=models.PointStruct(
        id=str(uuid4()),
        vector={
            "dense": dense_emb.tolist(),
            "sparse": sparse_embeddings[i],
            "colbert": colbert_embeddings[i]
            },
        payload={
            "file_name": os.path.basename(path),
            "source": path,
            "text": chunk.page_content,
            "title": chunk.metadata.get("title", os.path.basename(path)),
            "doc_type": doc_type,
            "page": f"{page}/{total_pages}",
            "metadata": chunk.metadata,
            "lang": lang,
            "is_deleted": False
            }
        )
        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )
    print(f"Uploaded {len(points)} points from {path}")
    

if __name__ == "__main__":
    import os
    
    BASE_DIR="data/raw/sample_docs"
    
    client = QdrantClient(path=settings.qdrant_path)
    ensure_colbert_collection(client)

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
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
    colbert_model=load_colbert_model()
    
    for file in os.listdir(BASE_DIR):
        path=os.path.join(BASE_DIR,file)
        if not os.path.isfile(path):
            continue
        ingest_multi_vector(client, path, dense_model, sparse_model, colbert_model, COLLECTION_NAME)

    client.close()