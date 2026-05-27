# 🧠 Lab 08 - Agent Memory

Lab này mô phỏng memory layer cho AI agent bằng Qdrant local mode.

## 🎯 Mục tiêu

- Lưu long-term memory của từng user dưới dạng dense vector.
- Search memory liên quan theo `user_id` và `is_deleted`.
- Đưa memory vào prompt như ngữ cảnh nội bộ để assistant trả lời tự nhiên.
- Extract thông tin đáng nhớ từ message mới của user và lưu lại vào Qdrant.

## 📁 Cấu trúc

```text
lab_08_agent_memory/
|-- main.py              # Pipeline chat: retrieve -> answer -> extract -> store
|-- memory_service.py    # Qdrant collection, index, add/search/delete memory
|-- llm_service.py       # Wrapper gọi Groq chat completion
|-- memory_extractor.py  # Parse JSON memory từ output LLM
|-- prompt.py            # Prompt trả lời và prompt extract memory
|-- config.py            # Collection name, Qdrant path, payload index
|-- requirements.txt
`-- .env
```

## 🗂️ Collection

Collection mặc định:

```text
agents_memory
```

Payload mỗi memory:

```python
{
    "user_id": "user_3",
    "text": "User đang học/tìm hiểu về AI.",
    "memory_type": "learning_context",
    "is_deleted": False,
    "created_at": "2026-05-22T..."
}
```

Các payload index:

```text
user_id
memory_type
is_deleted
```

Lưu ý: khi dùng `QdrantClient(path=...)`, payload index không tối ưu tốc độ như Qdrant server, nhưng vẫn phù hợp cho lab local.

## 🔁 Pipeline

```text
User query
  -> search_memory(query)
  -> build_chat_prompt(query, memories)
  -> llm_service.generate(...)
  -> EXTRACT_SYSTEM_PROMPT
  -> extract_response(...)
  -> add_memory(...)
```

Memory được dùng như ngữ cảnh nội bộ. Assistant không nên nói các câu như "tôi nhớ", "trước đây bạn nói", hoặc nhắc Qdrant/vector database.

## 🚀 Chạy lab

Từ repo root:

```bash
python -m labs.lab_08_agent_memory.memory_service
python -m labs.lab_08_agent_memory.main
```

`memory_service` tạo collection và payload index. `main` chạy vòng chat tương tác.

## ⚙️ Cấu hình

Lab dùng config chung từ `common.config`, gồm:

```text
QDRANT_PATH
EMBEDDING_MODEL
VECTOR_SIZE
GROQ_API_KEY
GROQ_MODEL
HF_TOKEN
```

Nếu model embedding nặng gây lỗi thiếu paging file trên Windows, dùng model nhẹ hơn:

```env
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
VECTOR_SIZE=384
```

Khi đổi `VECTOR_SIZE`, cần tạo lại collection vì size vector phải khớp với collection.

## 📌 Ghi chú thiết kế

- Lab hiện dùng dense search để giữ pipeline đơn giản.
- `search_memory` có threshold để tránh đưa memory không liên quan vào prompt.
- Extract memory trả JSON; nếu LLM trả sai format, extractor fallback về `memories: []`.
- Chưa xử lý deduplicate memory, query rewrite, hoặc hybrid/RRF. Đây là các hướng mở rộng hợp lý sau khi dense pipeline ổn định.
