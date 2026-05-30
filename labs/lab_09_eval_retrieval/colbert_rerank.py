import numpy as np

from common.embedding import embed_colbert


def rerank_colbert(query: str, colbert_model, candidates: list, top_n: int = 5):
    if not candidates:
        return []

    query_vectors = list(embed_colbert(colbert_model, [query]))
    if not query_vectors:
        return []

    q = np.asarray(query_vectors[0])

    reranked = []

    for item in candidates:
        if item.vector is None or "colbert" not in item.vector:
            continue

        d = np.asarray(item.vector["colbert"])
        sim = q @ d.T
        score = sim.max(axis=1).sum()

        item.payload["colbert_score"] = float(score)
        reranked.append(item)

    reranked.sort(
        key=lambda x: x.payload["colbert_score"],
        reverse=True,
    )

    return reranked[:top_n]