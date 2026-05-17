from sentence_transformers import SentenceTransformer
from qdrant_client import models
from fastembed import SparseTextEmbedding
from common.config import settings

def embedding(chunks, model_bembedding = settings.embedding_model):
    model=SentenceTransformer(model_bembedding)
    vectors=model.encode(chunks, normalize_embeddings=True)
    return vectors

def sparse_embedding(chunks, sparse_embedding= settings.sparse_embedding_model):
    model=SparseTextEmbedding(sparse_embedding)
    sparse_vectors=list(model.embed(chunks))

    chunks_sparse_embedded=[]

    for chunk in sparse_vectors:
        sparse_vector=models.SparseVector(
            indices=chunk.indices.tolist(),
            values=chunk.values.tolist()
        )
        chunks_sparse_embedded.append(sparse_vector)

    return chunks_sparse_embedded

if __name__=="__main__":
    chunks = "Hello World!!!"
    dense_vector=embedding(chunks)
    print(f"Dense vector: {dense_vector}")

    sparse_vectors=sparse_embedding(chunks)
    print(f"Sparse vector: {sparse_vectors}")

