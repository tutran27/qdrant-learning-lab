# 📊 Lab 09 - Evaluation Retrieval

Lab này dùng để đánh giá chất lượng retrieval trên collection `documents_lab09`, gồm dense vector, sparse vector và ColBERT multivector.

## 🎯 Mục tiêu

- Tạo bộ query đánh giá và ground truth trong `eval_set.json`.
- Chạy dense retrieval và hybrid retrieval trên collection `documents_lab09`.
- Tính `Recall@K` và `MRR@K` dựa trên ground truth theo document/page.
- Thử nghiệm rerank bằng Cross-Encoder và ColBERT.
- Đo latency đơn giản cho hybrid retrieval.
- Chuẩn bị mở rộng sang báo cáo kết quả.

## ⚙️ Điều kiện trước khi chạy

Lab 09 dùng collection riêng `documents_lab09`. Cần tạo collection và ingest dữ liệu multi-vector trước:

```bash
python -m labs.lab_09_eval_retrieval.ensure_collection
python -m labs.lab_09_eval_retrieval.ingest_multi_vector
```

## 🚀 Cách chạy

Kiểm tra retrieval:

```bash
python -m labs.lab_09_eval_retrieval.retrieve
```

Tính Recall@K:

```bash
python -m labs.lab_09_eval_retrieval.recall_at_k
```

Tính MRR@K:

```bash
python -m labs.lab_09_eval_retrieval.mrr
```

Chạy pipeline rerank:

```bash
python -m labs.lab_09_eval_retrieval.pipeline_rerank
```

Đo latency:

```bash
python -m labs.lab_09_eval_retrieval.latency_test
```

## 🔁 Lưu ý về rerank

Khi dùng rerank, `retrieve.py` cần lấy nhiều ứng viên hơn số kết quả cuối cùng. Nên phân biệt:

- `top_k`: số candidate lấy từ dense/sparse prefetch.
- `top_n`: số candidate sau fusion trả về cho reranker.
- `rerank top_n`: số kết quả cuối cùng sau Cross-Encoder hoặc ColBERT rerank.

Ví dụ nếu muốn trả về 5 kết quả sau rerank, không nên retrieve đúng 5 candidate. Nên lấy rộng hơn, ví dụ `top_k=40`, `top_n=20`, rồi rerank còn `5`. Nếu `top_n` trong retrieve quá nhỏ, reranker không có đủ candidate tốt để sắp xếp lại.

Với ColBERT rerank, `hybrid_retrieve()` phải bật `with_vectors=True` và collection phải có vector `"colbert"`.

## ⏱️ Latency test

`latency_test.py` hiện đo latency của hybrid dense + sparse retrieval với RRF.

Cấu hình mặc định:

```python
TOP_K = 20
TOP_N = 10
```

Script warm-up một query trước khi đo, sau đó chạy toàn bộ query trong `eval_set.json`. Mỗi query sẽ in latency và số kết quả trả về. Cuối cùng script in `count`, `mean`, `p50`, `p95`, `min`, `max`. Thời gian load model không tính vào latency.

## 🧪 Eval set

`eval_set.json` dùng schema version `2.0`. Ground truth chính nằm trong `relevant_targets`:

```json
{
  "file_name": "GIÁO TRÌNH CHỦ-NGHĨA-XÃ-HỘI-KHOA-HỌC.pdf",
  "pages": [50, 55, 60],
  "topics": ["dân chủ xã hội chủ nghĩa"]
}
```

Khi tính metric, nên match theo cặp `(file_name, page)` thay vì chỉ match `page`, vì nhiều tài liệu có cùng số trang.

## 📁 File chính

| File | Vai trò |
| --- | --- |
| `eval_set.json` | Bộ query đánh giá và ground truth theo document/page/topic. |
| `ensure_collection.py` | Tạo lại collection `documents_lab09` với vector `dense`, sparse vector `sparse` và multivector `colbert`. |
| `ingest_multi_vector.py` | Ingest tài liệu vào collection Lab 09 với dense/sparse/ColBERT vectors. |
| `retrieve.py` | Hàm dense retrieval và hybrid retrieval dùng collection Lab 09. |
| `recall_at_k.py` | Tính Recall@K cho từng query và trung bình toàn bộ eval set. |
| `mrr.py` | Tính MRR@K cho eval set. |
| `cross_encoder_rerank.py` | Rerank candidate bằng Cross-Encoder. |
| `colbert_rerank.py` | Rerank candidate bằng ColBERT late interaction. |
| `pipeline_rerank.py` | Pipeline retrieve rồi rerank bằng Cross-Encoder và ColBERT. |
| `latency_test.py` | Đo latency đơn giản cho hybrid retrieval. |
| `report.md` | Placeholder cho báo cáo kết quả. |

## 📌 Trạng thái

🚧 Đang triển khai.

Đã có:

- `eval_set.json`
- `ensure_collection.py`
- `ingest_multi_vector.py`
- `retrieve.py`
- `recall_at_k.py`
- `mrr.py`
- `cross_encoder_rerank.py`
- `colbert_rerank.py`
- `pipeline_rerank.py`
- `latency_test.py`

Chưa hoàn chỉnh:

- `report.md`
