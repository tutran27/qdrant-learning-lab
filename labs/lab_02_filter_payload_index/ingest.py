import os
from uuid import uuid4

from qdrant_client import models, QdrantClient

from common.document_loader import load_document
from common.chunking import text_split
from common.embedding import embed_dense, load_dense_model
from common.config import settings

from labs.lab_02_filter_payload_index.create_collection import ensure_collection_exists


def ingest_file(client, path, lang="vi"):
    collection_name=settings.dense_collection_name + "_lab02"

    pages = load_document(path)
    chunks = text_split(pages)

    chunks_content=[x.page_content for x in chunks]
    model = load_dense_model()
    chunks_embedded = embed_dense(model, chunks_content)

    doc_type = os.path.splitext(path)[-1]
    points = []
    for i, (chunk, embedd) in enumerate(zip(chunks, chunks_embedded)):
        page = chunk.metadata.get("page")
        total_pages = chunk.metadata.get("total_pages")

        point = models.PointStruct(
            id=str(uuid4()),
            vector=embedd.tolist(),
            payload={
                "chunk_id": i,
                "text": chunk.page_content,
                "title": chunk.metadata.get("title", os.path.basename(path)),
                "source": path,
                "doc_type": doc_type,
                "page": f"{page}/{total_pages}",
                "metadata": chunk.metadata,
                "lang": lang
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
    PATH = r'data/raw/sample_docs'
    client = QdrantClient(path=settings.qdrant_path)
    ensure_collection_exists(client)
    files = os.listdir(PATH)

    try:
        for file in files:
            path = os.path.join(PATH, file)
            if not os.path.isfile(path):
                continue

            ingest_file(client, path)
    finally:
        client.close()
