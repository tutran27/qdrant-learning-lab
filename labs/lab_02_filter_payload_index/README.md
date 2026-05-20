# 🧭 Lab 02 - Filter Payload Index

Lab này mở rộng từ Lab 01 bằng cách thực hành filter theo payload, tạo payload index và thao tác update/delete dữ liệu trong Qdrant.

## 🎯 Mục tiêu

- Tạo collection riêng cho lab 02.
- Ingest tài liệu kèm metadata.
- Tạo payload index cho các field hay filter.
- Scroll hoặc search theo điều kiện metadata.
- Update payload hàng loạt.
- Delete point theo filter.

## 🧩 File chính

| File | Vai trò |
| --- | --- |
| `create_collection.py` | Tạo lại collection `documents_lab02` |
| `ingest.py` | Ingest tài liệu vào collection lab 02 |
| `payload_index.py` | Tạo payload index cho `source`, `page`, `is_delete` |
| `search_with_filter.py` | Scroll/search dữ liệu bằng filter |
| `scroll_update_delete.py` | Demo set payload, scroll và delete bằng filter |

## 🚀 Cách chạy

Chạy ingest:

```bash
python -m labs.lab_02_filter_payload_index.ingest
```

Tạo payload index:

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

## 🔎 Ví dụ filter

Filter theo file nguồn và trang:

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

## 🧠 Kiến thức chính

- `MatchValue` dùng cho exact match, phù hợp với `source`, `page`, `doc_type`, boolean flag.
- `PayloadSchemaType.KEYWORD` phù hợp với field dạng định danh hoặc giá trị cần match chính xác.
- `set_payload()` có thể update payload cho nhiều point theo filter.
- `delete()` với `FilterSelector` có thể xóa point theo điều kiện metadata.

## 📌 Lưu ý

- Collection dùng trong lab này là `documents_lab02`.
- Chạy `ingest.py` sẽ tạo lại collection.
- Sau khi tạo lại collection, cần chạy lại `payload_index.py` nếu muốn có index.
- Field trong filter phải đúng tên và đúng giá trị payload thật, nếu không kết quả sẽ rỗng.
