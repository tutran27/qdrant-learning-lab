import json

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embed_dense, load_dense_model, embed_sparse, load_sparse_model
from common.document_loader import load_document
from common.chunking import text_split
from labs.lab_04_hybrid_dense_sparse.create_hybrid_collection import ensure_collection_exists

def hybrid_search(client: QdrantClient, 
                dense_model, 
                sparse_model, 
                query, 
                flt = None,
                k=40):
    collection_name=settings.dense_collection_name + "_lab04"
    dense_vectors=embed_dense(dense_model, [query])
    sparse_vectors=embed_sparse(sparse_model, [query])

    result=client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=dense_vectors[0].tolist(),
                limit=k,
                filter=flt,
                using="dense"
            ),
            models.Prefetch(
                query=sparse_vectors[0],
                limit=k,
                filter=flt,
                using="sparse"
            ),
        ],
        query=models.FusionQuery(
            fusion=models.Fusion.RRF
        ),
        limit=5,
        query_filter=flt,
        with_payload=True,
        with_vectors=False
    )
    return result.points


if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    dense_model=load_dense_model()
    sparse_model=load_sparse_model()
    query="notebooklm cÃ³ thá»ƒ lÃ m gÃ¬?"
    flt=models.Filter(
        must=[
            models.FieldCondition(
                key="file_name",
                match=models.MatchValue(
                    value="[Description]-Building-Simple-NotebookLM.pdf"
                )
            ),
            models.FieldCondition(
                key="is_deleted",
                match=models.MatchValue(value=False)
            )
        ]
    )
    
    results=hybrid_search(client, dense_model, sparse_model, query, flt)
    print("======== Hybrid Search ========")
    for res in results:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print(f"Score: {res.score}")
        print("----------")
    client.close()
    
    
    
    
    