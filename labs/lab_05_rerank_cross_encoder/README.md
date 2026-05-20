# Lab 05 - Retrieve Then Rerank với Cross-Encoder

Lab này thực hành pipeline RAG hai bước:

1. Retrieve candidate bằng hybrid search dense + sparse trên Qdrant.
2. Rerank candidate bằng cross-encoder để chọn chunk phù hợp hơn.

Lab 05 dùng lại collection `documents_lab04` từ Lab 04, vì vậy cần ingest Lab 04 trước.

## Mục tiêu

- Lấy top-k candidate bằng hybrid RRF.
- Chấm lại từng cặp `(query, chunk)` bằng cross-encoder.
- So sánh thứ hạng trước và sau rerank.
- Hiểu trade-off: rerank chính xác hơn nhưng chậm hơn retrieve thuần.

## File chính

| File | Vai trò |
| --- | --- |
| `retrieve_candidates.py` | Retrieve candidate bằng dense + sparse + RRF |
| `rerank.py` | Load cross-encoder, tính `rerank_score` và `final_score` |
| `pipeline_retrieve_then_rerank.py` | Ghép retrieve và rerank thành pipeline hoàn chỉnh |

## Cách chạy

Nếu chạy trong WSL với conda env của project:

```bash
conda activate qdrant
```

Tạo dữ liệu Lab 04 trước:

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
```

Chạy retrieve candidate:

```bash
python -m labs.lab_05_rerank_cross_encoder.retrieve_candidates
```

Chạy pipeline retrieve + rerank:

```bash
python -m labs.lab_05_rerank_cross_encoder.pipeline_retrieve_then_rerank
```

## Cách tính điểm

`rerank.py` đang dùng công thức:

```python
final_score = qdrant_score * 0.2 + rerank_score * 0.8
```

| Score | Ý nghĩa |
| --- | --- |
| `qdrant_score` | Điểm retrieve/fusion ban đầu từ Qdrant |
| `rerank_score` | Điểm liên quan do cross-encoder chấm |
| `final_score` | Điểm nội bộ dùng để sort kết quả cuối |

## Benchmark ngắn

Benchmark hiện dùng 4 query thủ công, mỗi query có một expected document.

| Metric | Retrieve | Retrieve + rerank |
| --- | ---: | ---: |
| `hit@1` | `4/4` | `4/4` |
| `hit@5` | `4/4` | `4/4` |

Trong bộ dữ liệu nhỏ này, hybrid retrieve đã đưa đúng document lên top 1 ở cả 4 query. Rerank không làm tăng `hit@1`, nhưng có thể đổi thứ tự chunk bên trong cùng document và giúp chọn chunk đưa vào prompt tốt hơn.

## Nhận xét

- Rerank hữu ích nhất khi top-k có nhiều chunk gần nghĩa hoặc nhiều document cạnh tranh.
- Cross-encoder chậm hơn retrieve vì phải chấm từng cặp `(query, chunk)`.
- `final_score` chỉ nên xem là score nội bộ của pipeline, không nên so trực tiếp với score gốc của Qdrant.
- Khi mở rộng lab, nên thêm ground truth theo `chunk_id` hoặc `page` thay vì chỉ đánh giá theo document.
