import torch
from sentence_transformers import CrossEncoder

from common.config import settings

def load_cross_encoder_model():
    return CrossEncoder(settings.cross_encoder_name,
                        device=settings.use_cuda,
                        activation_fn=torch.nn.Sigmoid())

def rerank(model, query, candidates, top_n=5, threshold:float = 0.5):

    if len(candidates) ==0:
        return {
            "status" : "No candidates",
            "results": []
        }

    pairs=[(query, x.payload.get("text", "")) for x in candidates]

    scores=model.predict(pairs, batch_size=8, show_progress_bar=True)

    for item, score in zip(candidates, scores):
        item.payload["rerank_score"] = float(score)
        item.payload['final_score'] = item.score * 0.2 + item.payload["rerank_score"] * 0.8
    
    candidates_sorted = sorted(candidates, key=lambda x: x.payload['final_score'], reverse=True)
    final_rerank_results = [x for x in candidates_sorted[:top_n] ]
    if threshold:
        final_rerank_results = [x for x in final_rerank_results if x.payload['final_score'] > threshold]
        print(f"after rerank filter : {len(final_rerank_results)}")

    if len(final_rerank_results) > top_n:
        final_rerank_results = final_rerank_results[:top_n]
    elif len(final_rerank_results) == 0:
        return {
            "status": "No candidates after rerank filter",
            "results": []
        }
    return {
        "status": "success",
        "results": final_rerank_results
    }