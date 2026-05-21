# Lab 07 - Multitenancy Permission

Lab này mô phỏng bài toán retrieval nhiều tenant trong Qdrant, trong đó dữ liệu của mỗi tenant được cô lập bằng `tenant_id`, còn quyền truy cập được kiểm soát bằng payload filter.

## Mục tiêu

- Tạo collection riêng cho dữ liệu nhiều tenant.
- Tạo payload index cho các trường dùng để filter quyền.
- Đánh dấu `tenant_id` là tenant index bằng `is_tenant=True`.
- Ingest tài liệu kèm metadata phân quyền.
- Search theo tenant để tránh trả nhầm dữ liệu của tenant khác.
- Search theo role như `viewer`, `editor`, `admin`.

## Collection

Collection mặc định:

```text
documents_law_tenant
```

Tên collection được tạo từ:

```python
COLLECTION_NAME = f"{settings.dense_collection_name}_law_tenant"
```

Với cấu hình mặc định `settings.dense_collection_name = "documents"`, collection sẽ là `documents_law_tenant`.

## Payload Schema

Mỗi chunk được lưu vào Qdrant với payload dạng:

```python
{
    "tenant_id": "qdrant_labs",
    "user_id": "tutran",
    "access_roles": ["viewer", "editor", "admin"],
    "visibility": "private",
    "file_name": "...",
    "source": "...",
    "text": "...",
    "title": "...",
    "doc_type": ".pdf",
    "page": "1/10",
    "metadata": {...},
    "lang": "vi",
    "is_deleted": False
}
```

Ý nghĩa các field phân quyền:

| Field | Ý nghĩa |
| --- | --- |
| `tenant_id` | Tenant/workspace/công ty sở hữu dữ liệu |
| `user_id` | Người upload hoặc owner của tài liệu, không phải toàn bộ người được phép xem |
| `access_roles` | Danh sách role được phép truy cập, ví dụ `viewer`, `editor`, `admin` |
| `visibility` | Phạm vi truy cập, ví dụ `private` hoặc `public` |
| `is_deleted` | Dùng cho soft delete |

Trong hệ thống thực tế, nếu cần rõ nghĩa hơn, `user_id` nên được đổi thành `owner_user_id`.

## Index

Lab tạo hai nhóm index:

### Tenant index

```python
("tenant_id", models.KeywordIndexParams(
    type=models.KeywordIndexType.KEYWORD,
    is_tenant=True
))
```

`is_tenant=True` giúp Qdrant tối ưu truy vấn khi workload luôn filter theo tenant.

### Payload index

Các field được index để phục vụ filter:

```text
user_id
access_roles
visibility
file_name
source
doc_type
lang
title
is_deleted
```

## Các file chính

| File | Vai trò |
| --- | --- |
| `create_tenant_index.py` | Tạo collection và payload index |
| `ingest_multi_tenant.py` | Load tài liệu, chunk, embed và upsert vào Qdrant với metadata tenant/permission |
| `search_by_tenant.py` | Search có filter theo `tenant_id` |
| `access_roles_filter.py` | Search có filter theo `tenant_id`, `access_roles`, `visibility` |
| `scroll.py` | Xem nhanh payload đã ingest |

## Thứ tự chạy

Chạy ingest để tạo collection, tạo index và nạp dữ liệu mẫu:

```bash
python -m labs.lab_07_multitenancy_permission.ingest_multi_tenant
```

Kiểm tra dữ liệu đã ingest:

```bash
python -m labs.lab_07_multitenancy_permission.scroll
```

Search giới hạn theo tenant:

```bash
python -m labs.lab_07_multitenancy_permission.search_by_tenant
```

Search giới hạn theo tenant và role:

```bash
python -m labs.lab_07_multitenancy_permission.access_roles_filter
```

## Logic phân quyền

Search theo tenant nên luôn có điều kiện:

```text
tenant_id = current_tenant_id
```

Search theo role nên có thêm điều kiện:

```text
access_roles contains one of current_user_roles
OR visibility = public
```

Ví dụ user có role:

```python
user_roles = ["viewer"]
```

Thì chỉ nên thấy tài liệu trong cùng tenant và có một trong các điều kiện:

- `access_roles` chứa `viewer`
- hoặc `visibility = "public"`

## Lưu ý thiết kế

- Không nên ingest lặp cùng một tài liệu cho từng user nếu nội dung giống nhau.
- Nên ingest một lần cho mỗi document/chunk, sau đó dùng payload filter để kiểm soát ai được xem.
- `tenant_id` là lớp cô lập dữ liệu quan trọng nhất.
- `access_roles` dùng để cấp quyền theo nhóm vai trò.
- Nếu cần cấp quyền riêng cho từng user, có thể bổ sung payload như `allowed_user_ids`.
- Script tạo collection hiện có thể xóa collection cũ trước khi tạo lại, nên dữ liệu cũ trong `documents_law_tenant` có thể bị mất khi chạy lại ingest.
