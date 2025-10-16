project_name/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Điểm vào chính của ứng dụng (FastAPI instance)
│   ├── core/                    # Cấu hình & tiện ích toàn cục
│   │   ├── __init__.py
│   │   ├── config.py            # Config (env vars, settings)
│   │   ├── security.py          # JWT, OAuth2, password hashing
│   │   └── logging_config.py    # Cấu hình logging
│   │
│   ├── api/                     # Định nghĩa router / endpoint
│   │   ├── __init__.py
│   │   ├── v1/                  # Versioning API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── items.py
│   │   │   │   └── ...
│   │   │   └── router.py        # Gom router của v1
│   │   └── dependencies.py      # Common dependency (ví dụ current_user)
│   │
│   ├── models/                  # ORM models (SQLAlchemy / Tortoise)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── schemas/                 # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── db/                      # Database layer
│   │   ├── __init__.py
│   │   ├── base.py              # Base metadata
│   │   ├── session.py           # Tạo SessionLocal, engine
│   │   └── init_db.py           # Khởi tạo DB (seed, migrate)
│   │
│   ├── services/                # Business logic (Xử lý trung gian)
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   │
│   ├── utils/                   # Tiện ích (helper functions)
│   │   ├── __init__.py
│   │   ├── email.py
│   │   └── file.py
│   │
│   └── tests/                   # Unit test / integration test
│       ├── __init__.py
│       ├── test_users.py
│       └── test_items.py
│
├── .env                         # Environment variables
├── requirements.txt              # Dependencies
├── alembic/                     # (Nếu dùng migration)
│   ├── env.py
│   ├── versions/
│   └── ...
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── README.md

| Thư mục       | Vai trò                                                 |
| ------------- | ------------------------------------------------------- |
| **core/**     | Cấu hình, biến môi trường, bảo mật (JWT, hash), logging |
| **api/**      | Nơi khai báo tất cả endpoints và router                 |
| **models/**   | ORM model tương ứng với bảng trong database             |
| **schemas/**  | Định nghĩa các schema dữ liệu (input/output)            |
| **db/**       | Kết nối, session, migration, khởi tạo database          |
| **services/** | Xử lý nghiệp vụ (logic trung gian giữa model và API)    |
| **utils/**    | Hàm tiện ích dùng chung (send email, upload file, v.v.) |
| **tests/**    | Unit test & integration test                            |
calo_estimation_project/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── upload.py       # ESP32 gửi ảnh tới đây
│   │   │   │   ├── predict.py      # API chạy model
│   │   │   │   └── stream.py       # WebSocket cho frontend
│   │   ├── ml/
│   │   │   ├── model.py            # Load model ML
│   │   │   └── preprocess.py
│   │   └── utils/
│   │       └── image_tools.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CameraFeed.jsx      # hiển thị video từ ESP32
│   │   │   ├── CalorieInfo.jsx     # hiển thị kết quả model
│   │   │   └── Layout.jsx
│   │   ├── services/
│   │   │   └── api.js              # axios gọi FastAPI
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── docker-compose.yml
