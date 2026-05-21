# 🔎 Qdrant Learning Lab

Bộ lab thực hành Qdrant cho các bài toán retrieval: ingest dữ liệu, tạo embedding, lưu payload metadata, vector search, filter, hybrid search, rerank, multivector, multi-tenancy và evaluation.

## 🎯 Mục tiêu

- Nắm quy trình tạo collection, upsert point và query trong Qdrant.
- Biết cách load tài liệu, chunk nội dung và tạo embedding.
- Thực hành payload metadata, payload index, scroll, update và delete.
- Xây dựng dense retrieval, hybrid dense + sparse retrieval, rerank và multivector retrieval.
- Mô phỏng multi-tenancy và permission filter bằng payload trong Qdrant.

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
| Lab 05 | Rerank Cross Encoder | ✅ Đã có code |
| Lab 06 | ColBERT Multivector | ✅ Đã có code |
| Lab 07 | Multitenancy Permission | ✅ Đã có code |
| Lab 08 | Agent Memory | ⏳ Placeholder |
| Lab 09 | Eval Retrieval | ⏳ Placeholder |

## ⚙️ Cài đặt

```bash
pip install -r requirements.txt
```

Nếu chạy trong conda env của project:

```bash
conda activate qdrant
```

Các script hiện dùng Qdrant local mode:

```python
QdrantClient(path="./qdrant_storage")
```

Vì vậy không cần chạy Qdrant server riêng cho các lab hiện tại.

## 🚀 Thứ tự chạy khuyến nghị

### 🔹 Lab 01 - Basic Retrieve

```bash
python -m labs.lab_01_basic_retrieve.ingest
python -m labs.lab_01_basic_retrieve.search
```

### 🔹 Lab 02 - Filter Payload Index

```bash
python -m labs.lab_02_filter_payload_index.ingest
python -m labs.lab_02_filter_payload_index.payload_index
python -m labs.lab_02_filter_payload_index.search_with_filter
python -m labs.lab_02_filter_payload_index.scroll_update_delete
```

### 🔹 Lab 04 - Hybrid Dense Sparse

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
python -m labs.lab_04_hybrid_dense_sparse.dense_search
python -m labs.lab_04_hybrid_dense_sparse.sparse_search
python -m labs.lab_04_hybrid_dense_sparse.hybrid_rrf
python -m labs.lab_04_hybrid_dense_sparse.scroll
```

### 🔹 Lab 05 - Retrieve Then Rerank

Lab 05 phụ thuộc collection của Lab 04.

```bash
python -m labs.lab_05_rerank_cross_encoder.retrieve_candidates
python -m labs.lab_05_rerank_cross_encoder.pipeline_retrieve_then_rerank
```

### 🔹 Lab 06 - ColBERT Multivector

Nếu muốn so sánh Dense vs ColBERT, cần ingest cả Lab 04 và Lab 06.

```bash
python -m labs.lab_06_colbert_multivector.ingest_multivector
python -m labs.lab_06_colbert_multivector.colbert_search
python -m labs.lab_06_colbert_multivector.compare_with_dense
```

### 🔹 Lab 07 - Multitenancy Permission

Lab 07 mô phỏng dữ liệu nhiều tenant và filter theo quyền truy cập.

```bash
python -m labs.lab_07_multitenancy_permission.ingest_multi_tenant
python -m labs.lab_07_multitenancy_permission.scroll
python -m labs.lab_07_multitenancy_permission.search_by_tenant
python -m labs.lab_07_multitenancy_permission.access_roles_filter
```

## 🗂️ Collection đang dùng

| Lab | Collection |
| --- | --- |
| Lab 01 | `documents_lab01` |
| Lab 02 | `documents_lab02` |
| Lab 04 | `documents_lab04` |
| Lab 05 | `documents_lab04` |
| Lab 06 | `colbert_documents` |
| Lab 07 | `documents_law_tenant` |

## 🔐 Ghi chú về Lab 07

Lab 07 dùng payload để mô phỏng phân quyền:

| Field | Ý nghĩa |
| --- | --- |
| `tenant_id` | Tenant/workspace/công ty sở hữu dữ liệu |
| `user_id` | Người upload hoặc owner của tài liệu |
| `access_roles` | Role được phép truy cập, ví dụ `viewer`, `editor`, `admin` |
| `visibility` | Phạm vi truy cập, ví dụ `private` hoặc `public` |
| `is_deleted` | Soft delete |

Trong thiết kế thực tế, không nên ingest lặp cùng một tài liệu cho từng user. Nên ingest một lần cho mỗi document/chunk, sau đó dùng `tenant_id`, `access_roles`, `visibility` và các field phân quyền khác để filter khi search.

## 📌 Lưu ý

- Các script ingest thường tạo lại collection, nên dữ liệu cũ trong collection tương ứng có thể bị xóa.
- Lần đầu chạy embedding model có thể mất thời gian do tải hoặc load weight.
- Lab 05 dùng lại dữ liệu Lab 04.
- Lab 06 dùng ColBERT/FastEmbed, có thể cần xóa cache nếu gặp lỗi thiếu file ONNX.
- Lab 07 dùng tenant index `is_tenant=True` cho field `tenant_id`.
- `qdrant_storage/`, cache Python và file môi trường đã được ignore trong `.gitignore`.
