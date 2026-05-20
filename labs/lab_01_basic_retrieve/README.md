# 🔎 Lab 01 - Basic Retrieve

Lab này thực hành luồng retrieval cơ bản với Qdrant: tạo collection, ingest tài liệu, tạo dense embedding và query semantic search.

## 🎯 Mục tiêu

- Tạo collection dense vector trong Qdrant.
- Load tài liệu PDF từ `data/raw/sample_docs`.
- Chunk nội dung tài liệu.
- Encode chunk bằng model embedding tiếng Việt.
- Upsert points vào Qdrant kèm payload metadata.
- Scroll dữ liệu và query theo ngữ nghĩa.

## 🧩 File chính

| File | Vai trò |
| --- | --- |
| `create_collection.py` | Tạo lại collection `documents` |
| `ingest.py` | Load tài liệu, chunk, embed và upsert vào Qdrant |
| `search.py` | Scroll thử dữ liệu và query dense vector |

## 🚀 Cách chạy

Chạy ingest trước để tạo collection và nạp dữ liệu:

```bash
python -m labs.lab_01_basic_retrieve.ingest
```

Sau đó chạy search:

```bash
python -m labs.lab_01_basic_retrieve.search
```

## 🧠 Kiến thức chính

- `PointStruct` gồm `id`, `vector`, `payload`.
- `vector` là dense embedding của chunk.
- `payload` lưu metadata như `text`, `title`, `source`, `doc_type`, `page`, `lang`.
- `client.query_points()` dùng để tìm các point gần query vector nhất.
- `client.scroll()` dùng để duyệt dữ liệu trong collection.

## 📌 Lưu ý

- Collection dùng trong lab này là `documents`.
- Chạy `ingest.py` sẽ tạo lại collection, dữ liệu cũ trong `documents` sẽ bị xóa.
- Lần đầu chạy embedding model có thể mất thời gian vì phải tải hoặc load weight.
