# 🧬 Lab 06 - ColBERT Multivector Retrieval

Lab này thực hành late-interaction retrieval với ColBERT và Qdrant multivector. Khác với dense embedding chỉ lưu một vector cho mỗi chunk, ColBERT lưu nhiều vector token-level cho một chunk và dùng `MAX_SIM` để so khớp query với document.

## 🎯 Mục tiêu

- Tạo collection Qdrant có multivector config.
- Ingest document bằng ColBERT embedding.
- Search bằng vector tên `colbert`.
- So sánh kết quả ColBERT với dense search từ Lab 04.

## 🧩 File chính

| File | Vai trò |
| --- | --- |
| `create_colbert_collection.py` | Tạo collection multivector |
| `ingest_multivector.py` | Chunk tài liệu, tạo ColBERT vectors và upsert vào Qdrant |
| `colbert_search.py` | Search bằng ColBERT multivector |
| `compare_with_dense.py` | Chạy cùng query qua dense search và ColBERT để so sánh |

## 🚀 Cách chạy

Nếu chạy trong WSL:

```bash
conda activate qdrant
```

Chuẩn bị collection dense của Lab 04 để dùng cho file compare:

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
```

Ingest ColBERT multivector:

```bash
python -m labs.lab_06_colbert_multivector.ingest_multivector
```

Search riêng bằng ColBERT:

```bash
python -m labs.lab_06_colbert_multivector.colbert_search
```

So sánh Dense vs ColBERT:

```bash
python -m labs.lab_06_colbert_multivector.compare_with_dense
```

## ⚖️ Dense vs ColBERT

| Tiêu chí | Dense retrieval | ColBERT multivector |
| --- | --- | --- |
| Biểu diễn chunk | Một vector cho cả chunk | Nhiều vector token-level cho mỗi chunk |
| Cách match | So khớp vector query với vector chunk | Late interaction, lấy tương đồng tốt nhất giữa token query và token document |
| Tốc độ | Nhanh hơn | Chậm hơn và tốn lưu trữ hơn |
| Độ chi tiết | Tốt cho semantic search tổng quát | Tốt hơn khi cần match chi tiết theo cụm từ/token |
| Storage | Nhẹ hơn | Nặng hơn vì mỗi chunk có nhiều vector |
| Use case phù hợp | Search mặc định, baseline, dữ liệu lớn | Rerank/search chất lượng cao, query cần bám sát nội dung |

## 🗂️ Collection

| Loại | Collection | Vector name |
| --- | --- | --- |
| Dense Lab 04 | `documents_lab04` | `dense` |
| ColBERT Lab 06 | `colbert_documents` | `colbert` |

## 📌 Lưu ý

- ColBERT phụ thuộc `LateInteractionTextEmbedding` của FastEmbed, lần đầu chạy có thể mất thời gian tải model.
- Nếu gặp lỗi thiếu `model.onnx`, thường là cache FastEmbed bị hỏng hoặc model không đúng format ONNX mà FastEmbed hỗ trợ.
- Với multivector, `size` trong collection là chiều của mỗi token vector, không phải tổng số chiều của toàn bộ document.
- `compare_with_dense.py` chỉ dùng để quan sát khác biệt kết quả, không phải benchmark chính thức.
