# Lab 04 - Hybrid Dense Sparse Search

Lab nÃ y thá»±c hÃ nh hybrid retrieval vá»›i Qdrant báº±ng cÃ¡ch lÆ°u cÃ¹ng lÃºc dense vector vÃ  sparse vector, sau Ä‘Ã³ tÃ¬m kiáº¿m riÃªng tá»«ng loáº¡i hoáº·c fusion báº±ng RRF.

## ðŸŽ¯ Má»¥c tiÃªu

- Táº¡o collection cÃ³ named dense vector vÃ  sparse vector.
- Ingest tÃ i liá»‡u vá»›i cáº£ dense embedding vÃ  sparse embedding.
- TÃ¬m kiáº¿m báº±ng dense vector.
- TÃ¬m kiáº¿m báº±ng sparse vector.
- Gá»™p káº¿t quáº£ báº±ng RRF trong hybrid search.
- Filter káº¿t quáº£ hybrid báº±ng metadata.

## ðŸ§© File chÃ­nh

| File | Vai trÃ² |
| --- | --- |
| `create_hybrid_collection.py` | Táº¡o collection `documents_lab06` vá»›i vector `dense` vÃ  sparse vector `sparse` |
| `ingest_dense_sparse.py` | Load tÃ i liá»‡u, táº¡o dense/sparse vector vÃ  upsert |
| `dense_search.py` | Query báº±ng dense vector |
| `sparse_search.py` | Query báº±ng sparse vector |
| `hybrid_rrf.py` | Hybrid search báº±ng `Prefetch` + `Fusion.RRF` |
| `scroll.py` | Scroll dá»¯ liá»‡u kÃ¨m filter metadata |
| `compare_results.py` | Placeholder Ä‘á»ƒ so sÃ¡nh káº¿t quáº£ dense/sparse/hybrid |

## ðŸš€ CÃ¡ch cháº¡y

Táº¡o collection vÃ  ingest dá»¯ liá»‡u:

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
```

Cháº¡y dense search:

```bash
python -m labs.lab_04_hybrid_dense_sparse.dense_search
```

Cháº¡y sparse search:

```bash
python -m labs.lab_04_hybrid_dense_sparse.sparse_search
```

Cháº¡y hybrid RRF:

```bash
python -m labs.lab_04_hybrid_dense_sparse.hybrid_rrf
```

Scroll dá»¯ liá»‡u theo filter:

```bash
python -m labs.lab_04_hybrid_dense_sparse.scroll
```

## ðŸ§  Dense, Sparse vÃ  Hybrid

### Dense search

Dense vector dÃ¹ng embedding model Ä‘á»ƒ báº¯t Ã½ nghÄ©a ngá»¯ nghÄ©a cá»§a cÃ¢u há»i vÃ  ná»™i dung.

PhÃ¹ há»£p khi query khÃ´ng trÃ¹ng tá»« khÃ³a chÃ­nh xÃ¡c vá»›i tÃ i liá»‡u nhÆ°ng cÃ¹ng Ã½ nghÄ©a.

### Sparse search

Sparse vector dÃ¹ng mÃ´ hÃ¬nh kiá»ƒu BM25 Ä‘á»ƒ báº¯t keyword/token.

PhÃ¹ há»£p vá»›i query cÃ³ thuáº­t ngá»¯ rÃµ rÃ ng nhÆ° `NotebookLM`, `Qdrant`, `HNSW`, `RAG`.

### Hybrid RRF

Hybrid search trong lab nÃ y dÃ¹ng:

```python
models.FusionQuery(fusion=models.Fusion.RRF)
```

RRF lÃ  Reciprocal Rank Fusion. CÆ¡ cháº¿ nÃ y gá»™p káº¿t quáº£ tá»« dense vÃ  sparse dá»±a trÃªn thá»© háº¡ng, thay vÃ¬ phá»¥ thuá»™c trá»±c tiáº¿p vÃ o score gá»‘c cá»§a tá»«ng phÆ°Æ¡ng phÃ¡p.

## ðŸ”Ž Filter trong hybrid search

Filter nÃªn Ä‘Æ°á»£c Ä‘Æ°a vÃ o tá»«ng `Prefetch` Ä‘á»ƒ giá»›i háº¡n candidate ngay tá»« dense vÃ  sparse search:

```python
models.Prefetch(
    query=dense_vectors[0].tolist(),
    limit=k,
    filter=flt,
    using="dense"
)
```

Vá»›i metadata nhÆ° `file_name`, nÃªn dÃ¹ng `MatchValue` Ä‘á»ƒ match chÃ­nh xÃ¡c:

```python
models.FieldCondition(
    key="file_name",
    match=models.MatchValue(
        value="[Description]-Building-Simple-NotebookLM.pdf"
    )
)
```

## ðŸ“Œ LÆ°u Ã½

- Collection dÃ¹ng trong lab nÃ y lÃ  `documents_lab06`.
- Cháº¡y `ingest_dense_sparse.py` sáº½ táº¡o láº¡i collection vÃ  ingest láº¡i dá»¯ liá»‡u.
- `file_name` vÃ  `is_deleted` chá»‰ cÃ³ sau khi ingest báº±ng báº£n lab 04 hiá»‡n táº¡i.
- `MatchText` khÃ´ng pháº£i contains string Ä‘Æ¡n giáº£n; nÃ³ phá»¥ thuá»™c vÃ o text index vÃ  tokenizer.
- Dense model vÃ  sparse model Ä‘Ã£ Ä‘Æ°á»£c tÃ¡ch thÃ nh `load_*_model()` vÃ  `embed_*()` trong `common/embedding.py` Ä‘á»ƒ háº¡n cháº¿ load weight láº·p láº¡i.
