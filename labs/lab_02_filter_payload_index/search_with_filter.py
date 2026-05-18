import json
from qdrant_client import QdrantClient, models

from common.config import settings
if __name__=="__main__":
    client=QdrantClient(path=settings.qdrant_path)
    collection_name=settings.dense_collection_name + "_lab02"

    flt=models.Filter(
        must=[
            models.FieldCondition(
                key="source",
                match=models.MatchValue(value="data/raw/sample_docs/Complete Roadmap to Become an Agentic AI Engineer.pdf")
            ),
            models.FieldCondition(
                key="page",
                match=models.MatchValue(value="11/23")
            )
        ]
    )
    res, nextpage=client.scroll(
        collection_name=collection_name,
        limit=4,
        with_payload=True,
        with_vectors=False,
        scroll_filter=flt
    )

    for x in res:
        print(json.dumps(x.payload, indent=2, ensure_ascii=False))

    client.close()