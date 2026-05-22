from datetime import datetime
from qdrant_client import QdrantClient, models
from uuid import uuid4
from labs.lab_08_agent_memory.config import settings
from common.embedding import load_dense_model, embed_dense

class MemoryService:
    def __init__(self, user_id: str, client: QdrantClient, dense_model):
        self.user_id=user_id
        self.client=client
        self.dense_model=dense_model

    def ensure_collection(self, collection_name: str):
        if self.client.collection_exists(collection_name=collection_name):
            print(f"Collection {collection_name} already exists")
            return
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=settings.vector_size,
                distance=models.Distance.COSINE,
            )
        )
        print(f"Created collection {collection_name}")

    def create_payload_index(self, collection_name: str, index: list):
        for key, index_params in index:
            try:
                self.client.create_payload_index(
                    collection_name=collection_name,
                    field_name=key,
                    field_schema=index_params,
                )
                print(f"Created payload index for field: {key}")
            except Exception as e:
                print(f"Skip index {key}: {e}")

    def add_memory(self, memory: dict):
        points=[]
        user_id=self.user_id
        print(f"Adding memory for user {user_id}")
        memories=memory.get("memories", []) if memory else []
        if len(memories)==0:
            print("No memories to add")
            return

        for item in memories:
            text=item.get("text", "")
            if not text.strip():
                continue
            memory_type=item.get("memory_type", "other")
            text_emb=embed_dense(self.dense_model, text)
            point=models.PointStruct(
                id=str(uuid4()),
                vector=text_emb.tolist(),
                payload={
                    "user_id": user_id,
                    "text": text,
                    "memory_type": memory_type,
                    "is_deleted": False,
                    "created_at": datetime.now().isoformat()
                }
            )
            points.append(point)
        if len(points)==0:
            print("No valid memories to add")
            return
        self.client.upsert(
            collection_name=settings.COLLECTION_NAME,
            points=points,
            wait=True
        )
        print(f"Added {len(points)} memories")
    
    def search_memory(self, query: str, limit: int=3, threshold: float=0.7):
        query_vector=embed_dense(self.dense_model, query)
        flt=models.Filter(
            must=[
                models.FieldCondition(
                    key="user_id",
                    match=models.MatchValue(value=self.user_id)
                ),
                models.FieldCondition(
                    key="is_deleted",
                    match=models.MatchValue(value=False)
                )
            ]
        )
        res=self.client.query_points(
            collection_name=settings.COLLECTION_NAME,
            query=query_vector.tolist(),
            query_filter=flt,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
        
        return [x.payload for x in res.points if x.score>=threshold]
    
    def delete_memory(self, memory_id: str):
        self.client.set_payload(
            collection_name=settings.COLLECTION_NAME,
            points=[memory_id],
            payload={
                "is_deleted": True
            },
            wait=True
        )
        print(f"Deleted memory {memory_id}")

if __name__=="__main__":
    dense_model=load_dense_model()
    client=QdrantClient(path=settings.qdrant_path)
    memory_service=MemoryService("user_1",client,dense_model)
    memory_service.ensure_collection(settings.COLLECTION_NAME)
    memory_service.create_payload_index(settings.COLLECTION_NAME, settings.PAYLOAD_INDEX)
    client.close()
