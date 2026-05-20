# Lab 05 - Retrieve Then Rerank với Cross-Encoder

Lab này thực hành pipeline hai bước cho RAG:

1. Retrieve candidate bằng hybrid search dense + sparse trên Qdrant.
2. Rerank các candidate bằng cross-encoder để đưa chunk phù hợp nhất lên đầu.

Lab 05 kế thừa dữ liệu và collection từ Lab 04. Collection mặc định là `documents_lab04`, được tạo bởi:

```bash
python -m labs.lab_04_hybrid_dense_sparse.ingest_dense_sparse
```

## Mục tiêu

- Đọc dữ liệu đã ingest từ `data/raw/sample_docs`.
- Tạo một vài query kiểm thử có expected document rõ ràng.
- Chạy retrieve bằng hybrid RRF để lấy top-k candidate.
- Chạy retrieve + rerank bằng cross-encoder.
- So sánh kết quả trước và sau rerank bằng `hit@1`, `hit@5`, thứ hạng tài liệu đúng và top chunk.

## File chính

| File | Vai trò |
| --- | --- |
| `retrieve_candidates.py` | Lấy candidate bằng hybrid search: dense vector + sparse vector + RRF |
| `rerank.py` | Load cross-encoder và tính `rerank_score`, `final_score` |
| `pipeline_retrieve_then_rerank.py` | Ghép retrieve và rerank thành một pipeline |
| `README.md` | Thiết kế lab, query benchmark và kết quả đánh giá |

## Dữ liệu raw

Dữ liệu mẫu nằm trong:

```text
data/raw/sample_docs/
```

Các file chính đã dùng để tạo query benchmark:

| File | Chủ đề |
| --- | --- |
| `[Description]-Building-Simple-NotebookLM.pdf` | Simple NotebookLM, RAG, giảm hallucination |
| `qdrant_vector_db_ai_v2.pdf` | Qdrant, vector database, RAG, hybrid search |
| `MemoryAgent.pdf` | Memory cho agent, short-term memory, SQLite, embedding, hybrid retrieval |
| `Complete Roadmap to Become an Agentic AI Engineer.pdf` | Lộ trình học Agentic AI Engineer |

## Cách chạy

Chạy ingest Lab 04 trước nếu chưa có collection:

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

Nếu dùng conda env của project:

```bash
conda activate qdrant
python -m labs.lab_05_rerank_cross_encoder.pipeline_retrieve_then_rerank
```

## Luồng xử lý

### 1. Retrieve candidate

`retrieve_candidates.py` gọi `client.query_points()` với hai `Prefetch`:

- Dense vector: bắt ngữ nghĩa của query.
- Sparse vector: bắt keyword/token.

Sau đó Qdrant dùng:

```python
models.FusionQuery(fusion=models.Fusion.RRF)
```

để gộp hai danh sách candidate thành một danh sách top-k.

### 2. Rerank

`rerank.py` tạo các cặp:

```python
(query, candidate_text)
```

Cross-encoder chấm trực tiếp mức liên quan giữa query và từng chunk. Lab hiện tính điểm cuối:

```python
final_score = qdrant_score * 0.2 + rerank_score * 0.8
```

Ý nghĩa:

- `qdrant_score`: điểm retrieve/fusion ban đầu.
- `rerank_score`: điểm liên quan do cross-encoder chấm.
- `final_score`: điểm dùng để sort kết quả cuối.

## Query benchmark

Benchmark dùng 4 query, mỗi query có một expected document.

| ID | Query | Expected document |
| --- | --- | --- |
| Q1 | `RAG giúp hệ thống NotebookLM giảm hallucination bằng cách nào?` | `[Description]-Building-Simple-NotebookLM.pdf` |
| Q2 | `Qdrant vector database được dùng để làm gì trong hệ thống RAG?` | `qdrant_vector_db_ai_v2.pdf` |
| Q3 | `Memory cho agent gồm short-term memory, SQLite, embedding và hybrid retrieval như thế nào?` | `MemoryAgent.pdf` |
| Q4 | `Lộ trình để trở thành Agentic AI Engineer cần học những kỹ năng và chủ đề nào?` | `Complete Roadmap to Become an Agentic AI Engineer.pdf` |

## Kết quả benchmark

Môi trường test:

| Thành phần | Giá trị |
| --- | --- |
| Conda env | `qdrant` |
| Qdrant path | `./qdrant_storage` |
| Collection | `documents_lab04` |
| Dense model | `bkai-foundation-models/vietnamese-bi-encoder` |
| Sparse model | `Qdrant/bm25` |
| Cross-encoder | `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` |
| Candidate limit | `k=40`, `top_k=5` |
| Rerank limit | `top_n=5`, `threshold=0` |

### Top-level result

| ID | Retrieve expected rank | Rerank expected rank | Retrieve top 1 | Rerank top 1 |
| --- | ---: | ---: | --- | --- |
| Q1 | 1 | 1 | `[Description]-Building-Simple-NotebookLM.pdf` | `[Description]-Building-Simple-NotebookLM.pdf` |
| Q2 | 1 | 1 | `qdrant_vector_db_ai_v2.pdf` | `qdrant_vector_db_ai_v2.pdf` |
| Q3 | 1 | 1 | `MemoryAgent.pdf` | `MemoryAgent.pdf` |
| Q4 | 1 | 1 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `Complete Roadmap to Become an Agentic AI Engineer.pdf` |

### Metrics

| Metric | Retrieve | Retrieve + rerank |
| --- | ---: | ---: |
| `hit@1` | `4/4` | `4/4` |
| `hit@5` | `4/4` | `4/4` |

Với bộ query này, hybrid retrieve đã đưa đúng tài liệu lên top 1 ở cả 4 query. Rerank không làm tăng `hit@1`, nhưng có thay đổi thứ tự chunk bên trong cùng tài liệu, đặc biệt ở Q4.

### Chi tiết top 3

#### Q1 - NotebookLM và hallucination

Retrieve top 3:

| Rank | File | Page | Score |
| ---: | --- | --- | ---: |
| 1 | `[Description]-Building-Simple-NotebookLM.pdf` | `25/38` | `0.5000` |
| 2 | `MemoryAgent.pdf` | `3/32` | `0.5000` |
| 3 | `MemoryAgent.pdf` | `13/32` | `0.3333` |

Rerank top 3:

| Rank | File | Page | Final score |
| ---: | --- | --- | ---: |
| 1 | `[Description]-Building-Simple-NotebookLM.pdf` | `25/38` | `0.1009` |
| 2 | `MemoryAgent.pdf` | `3/32` | `0.1000` |
| 3 | `qdrant_vector_db_ai_v2.pdf` | `21/30` | `0.0668` |

Nhận xét: Q1 khá sát giữa NotebookLM và MemoryAgent ở retrieve score. Rerank vẫn giữ đúng tài liệu NotebookLM ở top 1.

#### Q2 - Qdrant trong RAG

Retrieve top 3:

| Rank | File | Page | Score |
| ---: | --- | --- | ---: |
| 1 | `qdrant_vector_db_ai_v2.pdf` | `9/30` | `0.6250` |
| 2 | `qdrant_vector_db_ai_v2.pdf` | `9/30` | `0.5286` |
| 3 | `qdrant_vector_db_ai_v2.pdf` | `0/30` | `0.4762` |

Rerank top 3:

| Rank | File | Page | Final score |
| ---: | --- | --- | ---: |
| 1 | `qdrant_vector_db_ai_v2.pdf` | `9/30` | `0.9034` |
| 2 | `qdrant_vector_db_ai_v2.pdf` | `0/30` | `0.8946` |
| 3 | `qdrant_vector_db_ai_v2.pdf` | `4/30` | `0.8590` |

Nhận xét: Query có keyword rõ ràng `Qdrant`, `vector database`, `RAG`, nên retrieve và rerank đều rất ổn.

#### Q3 - Memory cho agent

Retrieve top 3:

| Rank | File | Page | Score |
| ---: | --- | --- | ---: |
| 1 | `MemoryAgent.pdf` | `2/32` | `0.7500` |
| 2 | `MemoryAgent.pdf` | `3/32` | `0.5667` |
| 3 | `MemoryAgent.pdf` | `29/32` | `0.4167` |

Rerank top 3:

| Rank | File | Page | Final score |
| ---: | --- | --- | ---: |
| 1 | `MemoryAgent.pdf` | `2/32` | `0.9470` |
| 2 | `MemoryAgent.pdf` | `0/32` | `0.8630` |
| 3 | `MemoryAgent.pdf` | `3/32` | `0.8500` |

Nhận xét: Query rất đặc thù với `Memory`, `SQLite`, `embedding`, `hybrid retrieval`, nên kết quả tập trung đúng vào tài liệu MemoryAgent.

#### Q4 - Roadmap Agentic AI Engineer

Retrieve top 3:

| Rank | File | Page | Score |
| ---: | --- | --- | ---: |
| 1 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `3/23` | `0.5526` |
| 2 | `MemoryAgent.pdf` | `3/32` | `0.5000` |
| 3 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `10/23` | `0.4103` |

Rerank top 3:

| Rank | File | Page | Final score |
| ---: | --- | --- | ---: |
| 1 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `10/23` | `0.3909` |
| 2 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `3/23` | `0.2119` |
| 3 | `Complete Roadmap to Become an Agentic AI Engineer.pdf` | `2/23` | `0.1316` |

Nhận xét: Đây là ví dụ rõ nhất cho giá trị của rerank. Retrieve top 3 còn xen `MemoryAgent.pdf`, nhưng rerank đẩy các chunk thuộc roadmap lên top 3.

## Cách đánh giá

Trong lab này dùng đánh giá thủ công theo expected document:

| Metric | Ý nghĩa |
| --- | --- |
| `expected_rank` | Thứ hạng đầu tiên mà expected document xuất hiện trong top-k |
| `hit@1` | Expected document nằm ở rank 1 |
| `hit@5` | Expected document xuất hiện trong top 5 |
| `top 3` | Dùng để đọc nhanh các chunk có hợp intent không |

Với dataset nhỏ, metric theo document là đủ để quan sát pipeline. Khi mở rộng lab, nên bổ sung ground truth theo chunk id hoặc page để đánh giá chính xác hơn.

## Nhận xét chính

- Hybrid retrieve đã hoạt động tốt trên bộ dữ liệu nhỏ này, đặc biệt khi query chứa keyword rõ.
- Rerank hữu ích nhất khi candidate top-k có nhiều tài liệu gần nghĩa hoặc nhiều chunk cạnh tranh nhau.
- Rerank không nhất thiết cải thiện `hit@1` nếu retrieve đã đúng, nhưng có thể cải thiện chất lượng chunk đưa vào prompt.
- `final_score` nên được xem là score nội bộ của pipeline, không nên so trực tiếp với score gốc của Qdrant.

## Lưu ý

- Lab 05 phụ thuộc collection `documents_lab04` từ Lab 04.
- Nếu chưa ingest Lab 04, `retrieve_candidates.py` và pipeline sẽ không có dữ liệu để search.
- Lần đầu load model có thể mất thời gian vì phải tải/cache weight từ Hugging Face.
- Nếu gặp warning unauthenticated HF Hub, có thể set `HF_TOKEN` trong `.env` để tăng rate limit.
- Cross-encoder chậm hơn retrieve vì nó chấm từng cặp `(query, chunk)` trực tiếp.
