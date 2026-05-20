import os 
from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from common.config import settings
from common.chunking import text_split
from common.document_loader import load_document
from common.embedding import load_colbert_model, embed_colbert

from labs.lab_06_colbert_multivector.create_colbert_collection import ensure_colbert_collection

def ingest_colbert(client, 
                    path, 
                    colbert_model,
                    lang="vi"):
    pages=load_document(path)
    chunks=text_split(pages)
    chunks_content=[x.page_content for x in chunks]
    chunks_embedded=list(embed_colbert(colbert_model, chunks_content))
    print(chunks_embedded[1].shape)

    points=[]
    for i, (chunk, embedd) in enumerate(zip(chunks, chunks_embedded)):
        doc_type=os.path.splitext(path)[-1]
        page = chunk.metadata.get("page")
        total_pages = chunk.metadata.get("total_pages")

        point=PointStruct(
            id=str(uuid4()),
            vector={
                "colbert": embedd
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
        collection_name=settings.colbert_collection_name,
        points=points, 
        wait=True
    )
    print(f"Uploaded {len(points)} points from {path}")
    
if __name__=="__main__":
    BASE_DIR="data/raw/sample_docs"
    client = QdrantClient(path=settings.qdrant_path)
    
    ensure_colbert_collection(client)
    
    colbert_model=load_colbert_model()
    for file in os.listdir(BASE_DIR):
        path=os.path.join(BASE_DIR,file)
        if not os.path.isfile(path):
            continue
        ingest_colbert(client, path, colbert_model)

    client.close()