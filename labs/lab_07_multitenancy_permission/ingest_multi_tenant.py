from qdrant_client import QdrantClient, models
from uuid import uuid4
import json
import os

from labs.lab_07_multitenancy_permission.create_tenant_index import ensure_collection, create_payload_index, create_tenant_index
from labs.lab_07_multitenancy_permission.constant import (
    COLLECTION_NAME,
    TENANT_INDEX,
    PAYLOAD_INDEX,
    BASE_DIR
)

from common.config import settings
from common.document_loader import load_document
from common.chunking import text_split
from common.embedding import (
    load_dense_model,
    embed_dense
)

def ingest_multi_tenant(client: QdrantClient, 
                        path: str,
                        tenant_id: str,
                        user_id: str,
                        access_roles: list,
                        visibility: str,
                        dense_model,
                        lang: str="vi",
                        ):
    # Load document
    pages=load_document(path)

    # Chunk document
    chunks=text_split(pages)
    chunks_content=[x.page_content for x in chunks]

    # Embed document
    dense_vectors=embed_dense(dense_model, chunks_content)

    points=[]
    for i, (chunk, dense_emb) in enumerate(zip(chunks, dense_vectors)):
        page = chunk.metadata.get("page")
        total_pages = chunk.metadata.get("total_pages")
        doc_type=os.path.splitext(path)[-1]

        point=models.PointStruct(
        id=str(uuid4()),
        vector=dense_emb.tolist(),
        payload={
            "tenant_id": tenant_id,
            "user_id": user_id,
            "access_roles": access_roles,
            "visibility": visibility,
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

if __name__=="__main__":
    
    client=QdrantClient(path=settings.qdrant_path)

    ensure_collection(client)
    create_payload_index(client, TENANT_INDEX)
    create_payload_index(client, PAYLOAD_INDEX)
    
    dense_model=load_dense_model()
    
    for file in os.listdir(BASE_DIR):
        path=os.path.join(BASE_DIR,file)
        if not os.path.isfile(path):
            continue
        ingest_multi_tenant(client, path, "qdrant_labs", "tutran", ["viewer", "editor", "admin"], "private", dense_model)
    client.close()