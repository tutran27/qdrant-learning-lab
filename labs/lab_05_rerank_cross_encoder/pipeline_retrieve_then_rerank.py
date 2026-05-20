import json
from qdrant_client import QdrantClient

from labs.lab_04_hybrid_dense_sparse.constants import DEFAULT_PREFETCH_LIMIT, DEFAULT_LIMIT

from common.config import settings
from common.embedding import load_dense_model, load_sparse_model

from labs.lab_05_rerank_cross_encoder.retrieve_candidates import hybrid_search
from labs.lab_05_rerank_cross_encoder.rerank import load_cross_encoder_model, rerank

def retrieve_then_rerank(client: QdrantClient, 
                        query: str, 
                        k: int = DEFAULT_PREFETCH_LIMIT, 
                        top_k: int=DEFAULT_LIMIT,
                        threshold: float = 0,
                        alpha: float = 0.5):
    
    dense_model=load_dense_model()
    sparse_model=load_sparse_model()
    reranker_model=load_cross_encoder_model()

    search_result=hybrid_search(client, query, dense_model, sparse_model,k=k,top_k=top_k)
    rerank_result=rerank(reranker_model, query, search_result,top_n=top_k, threshold=threshold)
    return rerank_result
    
if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    query="Làm sao để vector hóa dữ liệu sau khi đã chunk xong "
    rerank_result=retrieve_then_rerank(client, query)
    for res in rerank_result.get('results'):
        print(f"ID: {res.id}")
        print(f"Final_score: {res.payload.get('final_score')}")
        print(f"Rerank_score: {res.payload.get('rerank_score')}")
        print(f"Original_score: {res.score}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print("----------")
        
    client.close()