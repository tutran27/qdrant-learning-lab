# Qdrant Learning Lab

Bộ lab thực hành Qdrant cho các bài toán truy xuất tài liệu: ingest dữ liệu, tạo embedding, lưu payload metadata, tìm kiếm vector, filter, hybrid search và các hướng mở rộng như rerank, multivector, multi-tenancy, memory, evaluation.

## 🎯 Mục tiêu

- Nắm được quy trình tạo collection, upsert point và query trong Qdrant.
- Biết cách load tài liệu, chunk nội dung và tạo dense embedding.
- Thực hành payload metadata, payload index, scroll, update và delete.
- Xây dựng hybrid retrieval bằng dense vector, sparse vector và RRF.
- Chuẩn bị cấu trúc cho các lab nâng cao về tối ưu, rerank, memory và đánh giá retrieval.

## 📁 Cấu trúc thư mục

```text
common/                              # Code dùng chung: config, embedding, chunking, loader
data/raw/sample_docs/                 # Tài liệu mẫu để ingest
labs/lab_01_basic_retrieve/           # Dense vector retrieval cơ bản
labs/lab_02_filter_payload_index/     # Payload filter, payload index, update/delete
labs/lab_03_hnsw_quantization/        # HNSW, quantization, benchmark latency
labs/lab_04_hybrid_dense_sparse/      # Hybrid dense + sparse search
labs/lab_05_rerank_cross_encoder/     # Retrieve candidates + cross-encoder rerank
labs/lab_06_colbert_multivector/      # ColBERT / multivector retrieval
labs/lab_07_multitenancy_permission/  # Multi-tenancy và permission filter
labs/lab_08_agent_memory/             # Agent memory với Qdrant
labs/lab_09_eval_retrieval/           # Evaluation: Recall@K, MRR, latency
scripts/                              # Script tiện ích
qdrant_storage/                       # Dữ liệu Qdrant local, không commit
```

## ✅ Trạng thái lab

| Lab | Chủ đề | Trạng thái |
| --- | --- | --- |
| Lab 01 | Basic Retrieve | ✅ Đã có code |
| Lab 02 | Filter Payload Index | ✅ Đã có code |
| Lab 03 | HNSW Quantization | ⏳ Placeholder |
| Lab 04 | Hybrid Dense Sparse | ✅ Đã có code |
| Lab 05 | Rerank Cross Encoder | ⏳ Placeholder |
| Lab 06 | ColBERT Multivector | ⏳ Placeholder |
| Lab 07 | Multitenancy Permission | ⏳ Placeholder |
| Lab 08 | Agent Memory | ⏳ Placeholder |
| Lab 09 | Eval Retrieval | ⏳ Placeholder |

## ⚙️ Cài đặt

Cài dependency:

```bash
pip install -r requirements.txt
```

Các script hiện tại dùng Qdrant local mode:

```python
QdrantClient(path="./qdrant_storage")
```

Vì vậy không cần chạy Qdrant server riêng nếu chỉ dùng các lab hiện tại.

## 🚀 Thứ tự chạy khuyến nghị

### Lab 01 - Basic Retrieve

```bash
python -m labs.lab_01_basic_retrieve.ingest
python -m labs.lab_01_basic_retrieve.search
```

### Lab 02 - Filter Payload Index

```bash
python -m labs.lab_02_filter_payload_index.ingest
python -m labs.lab_02_filter_payload_index.payload_index
python -m labs.lab_02_filter_payload_index.search_with_filter
python -m labs.lab_02_filter_payload_index.scroll_update_delete
```

### Lab 04 - Hybrid Dense Sparse

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
python -m labs.lab_04_hybrid_dense_sparse.dense_search
python -m labs.lab_04_hybrid_dense_sparse.sparse_search
python -m labs.lab_04_hybrid_dense_sparse.hybrid_rrf
python -m labs.lab_04_hybrid_dense_sparse.scroll
```

## 🗂️ Collection đang dùng

| Lab | Collection |
| --- | --- |
| Lab 01 | `documents` |
| Lab 02 | `documents_lab02` |
| Lab 04 | `documents_lab04` |

## 📌 Lưu ý

- Các script ingest thường tạo lại collection, nên dữ liệu cũ trong collection tương ứng sẽ bị xóa.
- Lần đầu chạy embedding model có thể mất thời gian do tải hoặc load weight.
- Với metadata như `source`, `file_name`, `page`, nên ưu tiên `MatchValue` nếu cần match chính xác.
- `MatchText` phù hợp hơn cho field text dài hoặc field đã tạo text index rõ ràng.
- `qdrant_storage/`, cache Python và file môi trường đã được ignore trong `.gitignore`.
