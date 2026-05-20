from qdrant_client import QdrantClient
from qdrant_client.http.models import MultiVectorConfig, PointStruct
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from common.config import settings
from common.chunking import text_split
from common.document_loader import load_document

COLBERT_MODEL_NAME=settings.colbert_model_name

def ingest_colbert_model():
    tokenizer=AutoTokenizer.from_pretrained(COLBERT_MODEL_NAME)
    model=AutoModelForSequenceClassification.from_pretrained(COLBERT_MODEL_NAME)
    return tokenizer, model

def generate_multivector():
    pass