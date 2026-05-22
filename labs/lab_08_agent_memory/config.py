from qdrant_client import models
from common.config import settings
class Settings:
    COLLECTION_NAME=f"agents_memory"
    qdrant_path=settings.qdrant_path
    dense_model=settings.embedding_model
    vector_size=settings.vector_size
    distance=models.Distance.COSINE
    PAYLOAD_INDEX=[
        ("user_id", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True)),
        ("memory_type", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("is_deleted", models.BoolIndexParams(type=models.BoolIndexType.BOOL)),
    ]

settings=Settings()