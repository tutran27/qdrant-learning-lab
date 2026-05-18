from sentence_transformers import SentenceTransformer
from qdrant_client import models
from fastembed import SparseTextEmbedding
from common.config import settings


def load_dense_model():
    return SentenceTransformer(settings.embedding_model)

def embed_dense(model, chunks):
    return model.encode(chunks, normalize_embeddings=True)

def load_sparse_model():
    return SparseTextEmbedding(settings.sparse_embedding_model)

def embed_sparse(model, chunks):
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
    chunks = ["Hello World!!!", "Python is great!"]

    model=load_dense_model()
    dense_vectors=embed_dense(model, chunks)
    print(f"Dense vector: {dense_vectors}")

    sparse_model=load_sparse_model()
    sparse_vectors=embed_sparse(sparse_model, chunks)
    print(f"Sparse vector: {sparse_vectors}")

