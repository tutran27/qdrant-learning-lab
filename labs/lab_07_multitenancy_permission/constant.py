from common.config import settings
from qdrant_client import models

COLLECTION_NAME = f"{settings.dense_collection_name}_law_tenant"

TENANT_INDEX = [
    ("tenant_id", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True))
]

PAYLOAD_INDEX = [
    ("user_id", models.PayloadSchemaType.KEYWORD),
    ("access_roles", models.PayloadSchemaType.KEYWORD),
    ("visibility", models.PayloadSchemaType.KEYWORD),
    ("file_name", models.PayloadSchemaType.KEYWORD),
    ("source", models.PayloadSchemaType.KEYWORD),
    ("doc_type", models.PayloadSchemaType.KEYWORD),
    ("lang", models.PayloadSchemaType.KEYWORD),
    ("title", models.PayloadSchemaType.TEXT),
    ("is_deleted", models.PayloadSchemaType.BOOL),
]

BASE_DIR="data/raw/sample_docs"