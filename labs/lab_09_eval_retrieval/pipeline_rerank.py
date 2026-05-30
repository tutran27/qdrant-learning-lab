from qdrant_client import QdrantClient
from common.config import settings
from common.embedding import load_dense_model, load_sparse_model, load_colbert_model, embed_dense, embed_sparse, embed_colbert
from labs.lab_09_eval_retrieval.retrieve import hybrid_retrieve
from labs.lab_09_eval_retrieval.cross_encoder_rerank import load_cross_encoder_model, rerank
from labs.lab_09_eval_retrieval.colbert_rerank import rerank_colbert

def pipeline_rerank(client, query: str, dense_model, sparse_model, colbert_model, top_k: int = 5):
    # Retrieve documents
    candidates = hybrid_retrieve(client, dense_model, sparse_model, query)
    
    # Rerank with cross-encoder
    cross_encoder_model = load_cross_encoder_model()
    reranked = rerank(cross_encoder_model, query, candidates, top_n=top_k)
    reranked = reranked["results"]
    # ============= SHOW RERANKED RESULTS =============
    print("\n=== RERANKED RESULTS ===")
    for i, doc in enumerate(reranked):
        print(f"{i+1}. {doc.payload['title']}")
        print(f"   Search Score: {doc.score:.4f}")
        print(f"   Rerank Score: {doc.payload['rerank_score']:.4f}")
        print(f"   Final Score: {doc.payload['final_score']:.4f}")
        print(f"   Content: {doc.payload['text'][:100]}...")
        print("------------------")
    
    # Rerank with ColBERT
    colbert_reranked = rerank_colbert(query, colbert_model, candidates, top_n=top_k)
    
    # ============= SHOW COLBERT RERANKED RESULTS =============
    print("\n=== COLBERT RERANKED RESULTS ===")
    for i, doc in enumerate(colbert_reranked):
        print(f"{i+1}. {doc.payload['title']}")
        print(f"   Search Score: {doc.score:.4f}")
        print(f"   ColBERT Score: {doc.payload['colbert_score']:.4f}")
        print(f"   Content: {doc.payload['text'][:100]}...")
        print("------------------")
    
    return {
        "cross_encoder": reranked,
        "colbert": colbert_reranked
    }
    
if __name__ == "__main__":
    try:
        client = QdrantClient(path=settings.qdrant_path)
    
        # Load models
        dense_model = load_dense_model()
        sparse_model = load_sparse_model()
        colbert_model = load_colbert_model()
        
        # Run pipeline
        query = " Đảng Cộng sản là sản phẩm của "
        results = pipeline_rerank(client, query, dense_model, sparse_model, colbert_model)
        print("Pipeline rerank completed successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client.close()