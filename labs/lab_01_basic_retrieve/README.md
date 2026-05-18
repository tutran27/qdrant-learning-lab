# Lab 01 - Basic Retrieve

Lab nÃ y thá»±c hÃ nh luá»“ng retrieval cÆ¡ báº£n vá»›i Qdrant: táº¡o collection, ingest tÃ i liá»‡u, táº¡o dense embedding vÃ  query semantic search.

## ðŸŽ¯ Má»¥c tiÃªu

- Táº¡o collection dense vector trong Qdrant.
- Load tÃ i liá»‡u PDF tá»« `data/raw/sample_docs`.
- Chunk ná»™i dung tÃ i liá»‡u.
- Encode chunk báº±ng model embedding tiáº¿ng Viá»‡t.
- Upsert points vÃ o Qdrant kÃ¨m payload metadata.
- Scroll dá»¯ liá»‡u vÃ  query theo ngá»¯ nghÄ©a.

## ðŸ§© File chÃ­nh

| File | Vai trÃ² |
| --- | --- |
| `create_collection.py` | Táº¡o láº¡i collection `documents` |
| `ingest.py` | Load tÃ i liá»‡u, chunk, embed vÃ  upsert vÃ o Qdrant |
| `search.py` | Scroll thá»­ dá»¯ liá»‡u vÃ  query dense vector |

## ðŸš€ CÃ¡ch cháº¡y

Cháº¡y ingest trÆ°á»›c Ä‘á»ƒ táº¡o collection vÃ  náº¡p dá»¯ liá»‡u:

```bash
python -m labs.lab_01_basic_retrieve.ingest
```

Sau Ä‘Ã³ cháº¡y search:

```bash
python -m labs.lab_01_basic_retrieve.search
```

## ðŸ§  Kiáº¿n thá»©c chÃ­nh

- `PointStruct` gá»“m `id`, `vector`, `payload`.
- `vector` lÃ  dense embedding cá»§a chunk.
- `payload` lÆ°u metadata nhÆ° `text`, `title`, `source`, `doc_type`, `page`, `lang`.
- `client.query_points()` dÃ¹ng Ä‘á»ƒ tÃ¬m cÃ¡c point gáº§n query vector nháº¥t.
- `client.scroll()` dÃ¹ng Ä‘á»ƒ duyá»‡t dá»¯ liá»‡u trong collection.

## ðŸ“Œ LÆ°u Ã½

- Collection dÃ¹ng trong lab nÃ y lÃ  `documents`.
- Cháº¡y `ingest.py` sáº½ táº¡o láº¡i collection, dá»¯ liá»‡u cÅ© trong `documents` sáº½ bá»‹ xÃ³a.
- Láº§n Ä‘áº§u cháº¡y embedding model cÃ³ thá»ƒ máº¥t thá»i gian vÃ¬ pháº£i táº£i/load weight.
