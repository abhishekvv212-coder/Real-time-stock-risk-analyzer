# 📈 Real-Time Stock Portfolio Risk Analyzer

A production-grade REST API for analyzing live stock and crypto risk metrics, built with FastAPI, Redis, PostgreSQL, and deployed on AWS EC2.

## 🚀 Features

- ⚡ **60% faster API responses** via Redis caching layer under concurrent load
- 🔄 **Airflow-scheduled ETL pipeline** that auto-refreshes market data on AWS EC2
- 🗄️ **PostgreSQL + S3 storage** for data persistence and snapshot archiving
- ✅ **Unit tested** with pytest and structured error handling throughout

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| Cache | Redis |
| Database | PostgreSQL |
| ETL Scheduler | Apache Airflow |
| Cloud | AWS EC2 / S3 |
| Testing | pytest |
| Containerization | Docker / Docker Compose |

## 📁 Project Structure
```
├── app/
│   ├── main.py        # FastAPI app & routes
│   ├── routes.py      # API endpoints
│   └── cache.py       # Redis caching layer
├── db/
│   ├── connection.py  # Database connection
│   └── models.py      # SQLAlchemy models
├── etl/
│   └── pipeline.py    # Airflow ETL pipeline
├── tests/
│   └── test_routes.py # Unit tests
├── docker-compose.yml
├── requirements.txt
└── .env
```

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/abhishekvv212-coder/Real-time-stock-risk-analyzer.git
cd Real-time-stock-risk-analyzer
```

### 2. Start services
```bash
docker-compose up -d
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API
```bash
uvicorn app.main:app --reload
```

### 5. Run tests
```bash
pytest
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/stock/{symbol}` | Get live stock risk metrics |
| GET | `/stocks/saved` | Get all saved stocks |

## 👤 Author

**Abhi Nambiar** — [GitHub](https://github.com/abhishekvv212-coder)
