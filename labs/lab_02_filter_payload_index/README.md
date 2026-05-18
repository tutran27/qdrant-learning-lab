# Lab 02 - Filter Payload Index

Lab nÃ y má»Ÿ rá»™ng tá»« Lab 01 báº±ng cÃ¡ch thá»±c hÃ nh filter theo payload, táº¡o payload index vÃ  thao tÃ¡c update/delete dá»¯ liá»‡u trong Qdrant.

## ðŸŽ¯ Má»¥c tiÃªu

- Táº¡o collection riÃªng cho lab 02.
- Ingest tÃ i liá»‡u kÃ¨m metadata.
- Táº¡o payload index cho cÃ¡c field hay filter.
- Scroll/search theo Ä‘iá»u kiá»‡n metadata.
- Update payload hÃ ng loáº¡t.
- Delete point theo filter.

## ðŸ§© File chÃ­nh

| File | Vai trÃ² |
| --- | --- |
| `create_collection.py` | Táº¡o láº¡i collection `documents_lab02` |
| `ingest.py` | Ingest tÃ i liá»‡u vÃ o collection lab 02 |
| `payload_index.py` | Táº¡o payload index cho `source`, `page`, `is_delete` |
| `search_with_filter.py` | Scroll/search dá»¯ liá»‡u báº±ng filter |
| `scroll_update_delete.py` | Demo set payload, scroll vÃ  delete báº±ng filter |

## ðŸš€ CÃ¡ch cháº¡y

Cháº¡y ingest:

```bash
python -m labs.lab_02_filter_payload_index.ingest
```

Táº¡o payload index:

```bash
python -m labs.lab_02_filter_payload_index.payload_index
```

Test filter:

```bash
python -m labs.lab_02_filter_payload_index.search_with_filter
```

Test update/delete:

```bash
python -m labs.lab_02_filter_payload_index.scroll_update_delete
```

## ðŸ”Ž VÃ­ dá»¥ filter

Filter theo file nguá»“n vÃ  trang:

```python
models.Filter(
    must=[
        models.FieldCondition(
            key="source",
            match=models.MatchValue(
                value="data/raw/sample_docs/Complete Roadmap to Become an Agentic AI Engineer.pdf"
            )
        ),
        models.FieldCondition(
            key="page",
            match=models.MatchValue(value="11/23")
        )
    ]
)
```

## ðŸ§  Kiáº¿n thá»©c chÃ­nh

- `MatchValue` dÃ¹ng cho exact match, phÃ¹ há»£p vá»›i `source`, `page`, `doc_type`, boolean flag.
- `PayloadSchemaType.KEYWORD` phÃ¹ há»£p vá»›i field dáº¡ng Ä‘á»‹nh danh hoáº·c giÃ¡ trá»‹ cáº§n match chÃ­nh xÃ¡c.
- `set_payload()` cÃ³ thá»ƒ update payload cho nhiá»u point theo filter.
- `delete()` vá»›i `FilterSelector` cÃ³ thá»ƒ xÃ³a point theo Ä‘iá»u kiá»‡n metadata.

## ðŸ“Œ LÆ°u Ã½

- Collection dÃ¹ng trong lab nÃ y lÃ  `documents_lab02`.
- Cháº¡y `ingest.py` sáº½ táº¡o láº¡i collection.
- Sau khi táº¡o láº¡i collection, cáº§n cháº¡y láº¡i `payload_index.py` náº¿u muá»‘n cÃ³ index.
- Field trong filter pháº£i Ä‘Ãºng tÃªn vÃ  Ä‘Ãºng giÃ¡ trá»‹ payload tháº­t, náº¿u khÃ´ng káº¿t quáº£ sáº½ rá»—ng.
