# Lab 04 - Hybrid Dense Sparse Search

Lab này thực hành hybrid retrieval với Qdrant bằng cách lưu cùng lúc dense vector và sparse vector, sau đó tìm kiếm riêng từng loại hoặc fusion bằng RRF.

## 🎯 Mục tiêu

- Tạo collection có named dense vector và sparse vector.
- Ingest tài liệu với cả dense embedding và sparse embedding.
- Tìm kiếm bằng dense vector.
- Tìm kiếm bằng sparse vector.
- Gộp kết quả bằng RRF trong hybrid search.
- Filter kết quả hybrid bằng metadata.

## 🧩 File chính

| File | Vai trò |
| --- | --- |
| `constants.py` | Khai báo tên collection, tên vector và limit mặc định |
| `create_hybrid_collection.py` | Tạo collection `documents_lab04` với vector `dense` và sparse vector `sparse` |
| `ingest_dense_sparse.py` | Load tài liệu, tạo dense/sparse vector và upsert |
| `dense_search.py` | Query bằng dense vector |
| `sparse_search.py` | Query bằng sparse vector |
| `hybrid_rrf.py` | Hybrid search bằng `Prefetch` + `Fusion.RRF` |
| `scroll.py` | Scroll dữ liệu kèm filter metadata |
| `compare_results.py` | Placeholder để so sánh kết quả dense/sparse/hybrid |

## 🚀 Cách chạy

Tạo collection và ingest dữ liệu:

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
```

Chạy dense search:

```bash
python -m labs.lab_04_hybrid_dense_sparse.dense_search
```

Chạy sparse search:

```bash
python -m labs.lab_04_hybrid_dense_sparse.sparse_search
```

Chạy hybrid RRF:

```bash
python -m labs.lab_04_hybrid_dense_sparse.hybrid_rrf
```

Scroll dữ liệu theo filter:

```bash
python -m labs.lab_04_hybrid_dense_sparse.scroll
```

So sánh dense, sparse và hybrid:

```bash
python -m labs.lab_04_hybrid_dense_sparse.compare_results
```

## 🧠 Dense, Sparse và Hybrid

### Dense search

Dense vector dùng embedding model để bắt ý nghĩa ngữ nghĩa của câu hỏi và nội dung.

Phù hợp khi query không trùng từ khóa chính xác với tài liệu nhưng cùng ý nghĩa.

### Sparse search

Sparse vector dùng mô hình kiểu BM25 để bắt keyword/token.

Phù hợp với query có thuật ngữ rõ ràng như `NotebookLM`, `Qdrant`, `HNSW`, `RAG`.

### Hybrid RRF

Hybrid search trong lab này dùng:

```python
models.FusionQuery(fusion=models.Fusion.RRF)
```

RRF là Reciprocal Rank Fusion. Cơ chế này gộp kết quả từ dense và sparse dựa trên thứ hạng, thay vì phụ thuộc trực tiếp vào score gốc của từng phương pháp.

## 📊 So sánh kết quả

File `compare_results.py` dùng cùng một query để chạy 3 kiểu search:

- `Dense Search`: tìm theo ngữ nghĩa.
- `Sparse Search`: tìm theo keyword/token.
- `Hybrid RRF`: gộp kết quả dense và sparse bằng RRF.

### Tiêu chí đánh giá

| Tiêu chí | Ý nghĩa |
| --- | --- |
| `rank` | Thứ hạng của kết quả trong từng phương pháp |
| `score` | Điểm do Qdrant trả về, chỉ nên so sánh trong cùng một phương pháp |
| `file_name` | Kết quả đến từ tài liệu nào |
| `page` | Kết quả nằm ở trang nào |
| `text preview` | Đọc nhanh để kiểm tra có đúng intent query không |
| `overlap top-k` | Số kết quả trùng nhau giữa các phương pháp |

### Kết quả test mẫu nhiều query

Chạy lệnh:

```bash
python -m labs.lab_04_hybrid_dense_sparse.compare_results
```

Top 1 theo từng query:

| Query | Dense top 1 | Sparse top 1 | Hybrid top 1 | Nhận xét |
| --- | --- | --- | --- | --- |
| `NotebookLM có thể làm gì?` | `[Description]-Building-Simple-NotebookLM.pdf`, page `1/38`, score `0.4268` | `qdrant_vector_db_ai_v2.pdf`, page `10/30`, score `9.2105` | `[Description]-Building-Simple-NotebookLM.pdf`, page `1/38`, score `0.5833` | Dense và hybrid bắt đúng intent NotebookLM; sparse lệch sang tài liệu Qdrant do token chưa đủ đặc hiệu |
| `vector database dùng để làm gì?` | `qdrant_vector_db_ai_v2.pdf`, page `5/30`, score `0.4785` | `qdrant_vector_db_ai_v2.pdf`, page `27/30`, score `15.2585` | `qdrant_vector_db_ai_v2.pdf`, page `27/30`, score `0.8333` | Cả 3 phương pháp đều về đúng tài liệu Qdrant; hybrid ưu tiên đoạn được sparse xếp cao |
| `agent memory nên lưu thông tin gì?` | `MemoryAgent.pdf`, page `3/32`, score `0.5719` | `qdrant_vector_db_ai_v2.pdf`, page `24/30`, score `18.1609` | `MemoryAgent.pdf`, page `3/32`, score `0.6250` | Dense và hybrid bắt đúng tài liệu MemoryAgent; sparse bị kéo sang tài liệu có token liên quan filter/backend |

Overlap top-k:

| Query | Dense ∩ Sparse | Dense ∩ Hybrid | Sparse ∩ Hybrid |
| --- | ---: | ---: | ---: |
| `NotebookLM có thể làm gì?` | `0` | `3` | `2` |
| `vector database dùng để làm gì?` | `2` | `4` | `3` |
| `agent memory nên lưu thông tin gì?` | `0` | `2` | `3` |

Diễn giải nhanh:

- Query có keyword rất rõ như `vector database` thì dense, sparse và hybrid đều ổn.
- Query thiên về intent như `NotebookLM có thể làm gì?` hoặc `agent memory nên lưu thông tin gì?` thì dense/hybrid ổn định hơn sparse-only.
- Hybrid thường giữ top 1 hợp lý từ dense nhưng vẫn kéo thêm một phần kết quả từ sparse, đúng vai trò cân bằng semantic search và keyword search.

## 🔎 Filter trong hybrid search

Filter nên được đưa vào từng `Prefetch` để giới hạn candidate ngay từ dense và sparse search:

```python
models.Prefetch(
    query=dense_vectors[0].tolist(),
    limit=DEFAULT_PREFETCH_LIMIT,
    filter=flt,
    using=DENSE_VECTOR_NAME
)
```

Với metadata như `file_name`, nên dùng `MatchValue` để match chính xác:

```python
models.FieldCondition(
    key="file_name",
    match=models.MatchValue(
        value="[Description]-Building-Simple-NotebookLM.pdf"
    )
)
```

## 📌 Lưu ý

- Collection dùng trong lab này là `documents_lab04`.
- Chạy `ingest_dense_sparse.py` sẽ tạo lại collection và ingest lại dữ liệu.
- `file_name` và `is_deleted` chỉ có sau khi ingest bằng bản lab 04 hiện tại.
- `MatchText` không phải contains string đơn giản; nó phụ thuộc vào text index và tokenizer.
- Dense model và sparse model đã được tách thành `load_*_model()` và `embed_*()` trong `common/embedding.py` để hạn chế load weight lặp lại.
