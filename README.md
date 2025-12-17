# Data Preparation API Service

A comprehensive FastAPI-based service for automated data preparation and profiling across multiple data sources including datasets, feature stores, and training datasets.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Processing Workflow](#processing-workflow)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This API service provides automated data profiling and preparation capabilities for three types of data sources:

1. **Dataset Processing** - Traditional file-based datasets (CSV, TSV, XLS, XLSX, SAV)
2. **Feature Store Processing** - Feature groups stored in Hive (offline) or Redis (online)
3. **Training Dataset Processing** - ML training datasets stored in HDFS (CSV, TFRecord)

All processing happens asynchronously with comprehensive status tracking and error handling.

## ✨ Features

### Core Capabilities

- ✅ Asynchronous background processing
- ✅ RESTful API with OpenAPI documentation
- ✅ Multi-source data processing (Files, Hive, Redis, HDFS)
- ✅ Automated data profiling using ydata-profiling
- ✅ Status tracking (pending, processing, success, failed)
- ✅ Batch processing support
- ✅ Comprehensive logging
- ✅ Error handling and recovery

### Supported Data Sources

- **Files**: CSV, TSV, Excel (XLS/XLSX), SPSS (SAV)
- **Databases**: PostgreSQL
- **Big Data**: Apache Hive, HDFS
- **Cache**: Redis

## 📁 Project Structure

```
dataprep-api/
├── README.md              # Project documentation (outside app)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
└── app/                   # Main application directory
    ├── __init__.py
    ├── main.py           # FastAPI application entry point
    ├── api/
    │   ├── __init__.py
    │   ├── routes.py     # API routes/endpoints
    │   └── models.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py     # Configuration management
    │   └── utils.py      # Utility functions
    └── service/
        ├── __init__.py
        ├── db_service.py           # Database operations
        ├── dataset_service.py      # Dataset processing logic
        ├── feature_store_service.py    # Feature store operations (placeholder)
        └── training_dataset_service.py # Training dataset operations (placeholder)
```

### File Descriptions

| File                                  | Purpose                                         |
| ------------------------------------- | ----------------------------------------------- |
| `main.py`                             | FastAPI application initialization and startup  |
| `api/routes.py`                       | All API endpoint definitions                    |
| `api/models.py`                       | Pydantic models for request/response validation |
| `core/config.py`                      | Configuration from environment variables        |
| `core/utils.py`                       | Logging setup and utility functions             |
| `service/db_service.py`               | PostgreSQL database operations                  |
| `service/dataset_service.py`          | File-based dataset processing                   |
| `service/feature_store_service.py`    | Feature store data processing                   |
| `service/training_dataset_service.py` | HDFS training dataset processing                |

## 🚀 Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Access to required data sources (based on your use case):
  - File storage server (for datasets)
  - Apache Hive (for offline feature store)
  - Redis (for online feature store)
  - HDFS cluster (for training datasets)
  - Kerberos authentication (for Hive/HDFS)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd dataprep-api
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create log directory**

   ```bash
   cd data-prep-api
   mkdir logs
   # Or update LOG_FILE_PATH in .env
   ```

6. **Initialize database tables**

   Run these SQL scripts in your PostgreSQL database:

   ```sql
   -- For datasets (if not exists)
   ALTER TABLE dataset ADD COLUMN IF NOT EXISTS dataset_preprocessed INTEGER DEFAULT 1;

   -- For feature groups
   CREATE TABLE IF NOT EXISTS feature_group (
       table_name VARCHAR(255) PRIMARY KEY,
       online BOOLEAN NOT NULL DEFAULT FALSE,
       dataprep_status INTEGER DEFAULT 1,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- For training datasets
   CREATE TABLE IF NOT EXISTS training_dataset (
       id SERIAL PRIMARY KEY,
       path VARCHAR(500) NOT NULL,
       dataset_format VARCHAR(50) NOT NULL,
       dataprep_status INTEGER DEFAULT 1,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# ============================================
# Application Settings
# ============================================
APP_NAME=Data Preparation API
VERSION=1.0.0

# ============================================
# Database Configuration
# ============================================
PSQL_HOST=localhost
PSQL_DATABASE=your_database
PSQL_PORT=5432
PSQL_USER=your_user
PSQL_PASSWORD=your_password

# ============================================
# File Storage (for Dataset Processing)
# ============================================
URL=https://your-api-url.com/api/files/
LOCAL_DIR=/tmp/dataprep

# ============================================
# Feature Store Configuration
# ============================================
URL2=http://your-api-url.com/api/v1/lib/feature-groups/

# Redis (for online feature store)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Hive (for offline feature store)
HIVE_HOST=localhost
HIVE_PORT=10000
HIVE_PRINCIPAL=hive/_HOST@REALM.COM
HIVE_DATABASE=default

# ============================================
# Training Dataset Configuration
# ============================================
URL3=http://your-api-url.com/api/v1/lib/training-datasets/

# HDFS Configuration
HADOOP_HOME=/usr/hadoop
HDFS_NAMENODE=namenode.example.com
TICKET_CACHE_PATH=/tmp/krb5cc_1062

# ============================================
# Logging Configuration
# ============================================
LOG_FILE_PATH=data-prep-api/logs/data-prep-api.log
MAX_LOG_SIZE=10485760  # 10 MB
BACKUP_COUNT=5

# ============================================
# API Configuration
# ============================================
MAX_FILE_SIZE=104857600  # 100 MB
```

### Status Codes

All processing operations use the following status codes:

| Code   | Status     | Description                       |
| ------ | ---------- | --------------------------------- |
| `0`    | Success    | Processing completed successfully |
| `1`    | Pending    | Waiting to be processed           |
| `2`    | Processing | Currently being processed         |
| `3`    | Failed     | Processing failed with errors     |
| `NULL` | Error      | Database error or not found       |

## 📡 API Endpoints

### Dataset Processing

| Method | Endpoint                     | Description                     |
| ------ | ---------------------------- | ------------------------------- |
| POST   | `/dataprep/process`          | Process single dataset file     |
| POST   | `/dataprep/batch`            | Batch process multiple datasets |
| GET    | `/dataprep/status/{file_id}` | Get processing status           |
| GET    | `/dataprep/list`             | List datasets with filtering    |

### Feature Store Processing

| Method | Endpoint                                      | Description                              |
| ------ | --------------------------------------------- | ---------------------------------------- |
| POST   | `/dataprep/feature-store/process`             | Process single feature group             |
| POST   | `/dataprep/feature-store/batch`               | Batch process all pending feature groups |
| GET    | `/dataprep/feature-store/status/{table_name}` | Get feature group status                 |
| GET    | `/dataprep/feature-store/list`                | List feature groups                      |

### Training Dataset Processing

| Method | Endpoint                                    | Description                     |
| ------ | ------------------------------------------- | ------------------------------- |
| POST   | `/dataprep/training-dataset/process`        | Process single training dataset |
| POST   | `/dataprep/training-dataset/batch`          | Batch process training datasets |
| GET    | `/dataprep/training-dataset/status/{td_id}` | Get training dataset status     |
| GET    | `/dataprep/training-dataset/list`           | List training datasets          |

## 💡 Usage Examples

### 1. Process a Single CSV Dataset

```bash
curl -X POST "http://localhost:3306/dataprep/process" \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "dataset",
    "file_id": "12345",
    "file_type": "csv"
  }'
```

**Response:**

```json
{
  "status": "accepted",
  "message": "Dataset processing started",
  "file_id": "12345"
}
```

### 2. Process a Feature Group from Hive

```bash
curl -X POST "http://localhost:3306/dataprep/feature-store/process" \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "customer_features_v1",
    "online": false
  }'
```

### 3. Process a Training Dataset from HDFS

```bash
curl -X POST "http://localhost:3306/dataprep/training-dataset/process" \
  -H "Content-Type: application/json" \
  -d '{
    "td_id": "67890",
    "hdfs_path": "hdfs://namenode:8020/datasets/train/data.csv",
    "dataset_format": "csv"
  }'
```

### 4. Batch Process All Pending Items

```bash
# Process all pending datasets
curl -X POST "http://localhost:3306/dataprep/batch" \
  -H "Content-Type: application/json" \
  -d '{"table_name": "dataset", "filters": {"status": 1}}'

# Process all pending feature groups
curl -X POST "http://localhost:3306/dataprep/feature-store/batch"

# Process all pending CSV training datasets
curl -X POST "http://localhost:3306/dataprep/training-dataset/batch" \
  -H "Content-Type: application/json" \
  -d '{"dataset_format": "csv"}'
```

### 5. Check Processing Status

```bash
# Dataset status
curl "http://localhost:3306/dataprep/status/12345?table_name=dataset"

# Feature group status
curl "http://localhost:3306/dataprep/feature-store/status/customer_features_v1"

# Training dataset status
curl "http://localhost:3306/dataprep/training-dataset/status/67890"
```

### 6. List Items with Filtering

```bash
# List pending datasets
curl "http://localhost:3306/dataprep/list?status=1&limit=50"

# List all feature groups
curl "http://localhost:3306/dataprep/feature-store/list?limit=100"

# List CSV training datasets
curl "http://localhost:3306/dataprep/training-dataset/list?dataset_format=csv"
```

### Python Client Example

```python
import requests

class DataPrepClient:
    def __init__(self, base_url="http://localhost:3306"):
        self.base_url = base_url

    def process_dataset(self, table_name, file_id, file_type):
        url = f"{self.base_url}/dataprep/process"
        payload = {
            "table_name": table_name,
            "file_id": file_id,
            "file_type": file_type
        }
        response = requests.post(url, json=payload)
        return response.json()

    def process_feature_group(self, table_name, online=False):
        url = f"{self.base_url}/dataprep/feature-store/process"
        payload = {
            "table_name": table_name,
            "online": online
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_status(self, file_id, table_name="dataset"):
        url = f"{self.base_url}/dataprep/status/{file_id}"
        params = {"table_name": table_name}
        response = requests.get(url, params=params)
        return response.json()

# Usage
client = DataPrepClient()

# Process a dataset
result = client.process_dataset("dataset", "12345", "csv")
print(result)

# Process a feature group
result = client.process_feature_group("sales_features", online=False)
print(result)

# Check status
status = client.get_status("12345")
print(f"Status: {status['status']}")
```

## 🔄 Processing Workflow

### Dataset Processing Flow

```
1. API receives request → Validates file type
2. Updates status to "pending" (1) in database
3. Background task starts
4. Downloads file from URL
5. Generates ydata-profiling report
6. Uploads JSON report back to server
7. Updates status to "success" (0) or "failed" (3)
8. Cleans up temporary files
```

### Feature Store Processing Flow

```
1. API receives request → Validates table name
2. Updates status to "processing" (2)
3. Fetches data from Redis (online) or Hive (offline)
4. Generates ydata-profiling report
5. Uploads JSON report to URL2
6. Updates status to "success" (0) or "failed" (3)
7. Cleans up temporary files
```

### Training Dataset Processing Flow

```
1. API receives request → Validates HDFS path
2. Updates status to "processing" (2)
3. Downloads file from HDFS using Kerberos
4. Reads data (CSV or TFRecord)
5. Generates ydata-profiling report
6. Uploads JSON report to URL3
7. Updates status to "success" (0) or "failed" (3)
8. Cleans up temporary files
```

## 🏃 Deployment

### Running the Application

#### Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 3306

# Access API documentation
# Swagger UI: http://localhost:3306/docs
# ReDoc: http://localhost:3306/redoc
```

#### Production Mode

```bash
# Multiple workers for better performance
uvicorn main:app --host 0.0.0.0 --port 3306 --workers 4

# With Gunicorn (recommended)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:3306
```

### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create log directory
RUN mkdir -p /home/apps/logs

# Expose port
EXPOSE 3306

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3306", "--workers", "4"]
```

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  dataprep-api:
    build: .
    ports:
      - "3306:3306"
    env_file:
      - .env
    volumes:
      - ./logs:/home/apps/logs
      - ./tmp:/tmp/dataprep
    restart: unless-stopped
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${PSQL_DATABASE}
      POSTGRES_USER: ${PSQL_USER}
      POSTGRES_PASSWORD: ${PSQL_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Build and run:**

```bash
docker-compose up -d
```

### Systemd Service (Linux)

Create `/etc/systemd/system/dataprep-api.service`:

```ini
[Unit]
Description=Data Preparation API Service
After=network.target

[Service]
Type=simple
User=apps
WorkingDirectory=/home/apps/dataprep-api
Environment="PATH=/home/apps/dataprep-api/venv/bin"
ExecStart=/home/apps/dataprep-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 3306 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable dataprep-api
sudo systemctl start dataprep-api
sudo systemctl status dataprep-api
```

### Scheduled Batch Processing

Use cron for periodic batch processing:

```bash
# Edit crontab
crontab -e

# Add these lines for hourly batch processing
0 * * * * curl -X POST http://localhost:3306/dataprep/batch -H "Content-Type: application/json" -d '{"table_name": "dataset", "filters": {"status": 1}}'
5 * * * * curl -X POST http://localhost:3306/dataprep/feature-store/batch
10 * * * * curl -X POST http://localhost:3306/dataprep/training-dataset/batch -H "Content-Type: application/json" -d '{"dataset_format": "csv"}'
```

## 📊 Monitoring

### Health Check Endpoint

Add to `main.py`:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat()
    }
```

### Logging

Logs are written to `LOG_FILE_PATH` with rotation:

```bash
# View logs
tail -f /home/apps/logs/dataset.log

# Search for errors
grep ERROR /home/apps/logs/dataset.log

# Search for specific file_id
grep "12345" /home/apps/logs/dataset.log
```

**Log Format:**

```
[2024-01-15 10:30:00] [INFO] [service.dataset_service] Starting processing for file_id: 12345
[2024-01-15 10:30:15] [INFO] [service.dataset_service] Successfully downloaded file_id: 12345
[2024-01-15 10:30:45] [INFO] [service.dataset_service] Report saved: /tmp/dataprep/12345_Sheet1.json
[2024-01-15 10:31:00] [INFO] [service.dataset_service] Successfully processed file_id: 12345
```

### Metrics

Consider adding Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, make_asgi_app

# Metrics
processing_counter = Counter('dataprep_processed_total', 'Total processed items', ['type'])
processing_duration = Histogram('dataprep_duration_seconds', 'Processing duration', ['type'])

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection details in `.env`
- Test connection: `psql -h $PSQL_HOST -U $PSQL_USER -d $PSQL_DATABASE`
- Check firewall rules

#### 2. Hive Connection Failed

**Error:** `pyhive.exc.OperationalError: Could not connect to hive`

**Solutions:**

- Verify Kerberos ticket: `klist`
- Renew ticket if expired: `kinit -kt /path/to/keytab user@REALM`
- Check HIVE_HOST and HIVE_PORT
- Verify Hive service is running

#### 3. HDFS Download Failed

**Error:** `pyarrow.lib.ArrowIOError: HDFS connection failed`

**Solutions:**

- Check Kerberos ticket: `klist`
- Verify HADOOP_HOME path
- Check HDFS namenode: `hdfs dfsadmin -report`
- Verify HDFS path exists: `hdfs dfs -ls /path/to/data`

#### 4. Redis Connection Failed

**Error:** `redis.exceptions.ConnectionError`

**Solutions:**

- Verify Redis is running: `redis-cli ping`
- Check REDIS_HOST and REDIS_PORT
- Test connection: `redis-cli -h $REDIS_HOST -p $REDIS_PORT`

#### 5. File Upload Failed

**Error:** `requests.exceptions.ConnectionError`

**Solutions:**

- Verify URL, URL2, URL3 endpoints
- Check network connectivity
- Verify SSL certificates (or set `verify=False` in dev)
- Check API authentication/authorization

#### 6. Memory Issues with Large Files

**Error:** `MemoryError` during profiling

**Solutions:**

- Increase system memory
- Use `minimal=True` for ProfileReport (already default)
- Process smaller batches
- Consider sampling large datasets before profiling

### Debug Mode

Enable debug logging in `core/utils.py`:

```python
logger.setLevel(logging.DEBUG)
```

### Testing Endpoints

Test with curl:

```bash
# Test health
curl http://localhost:3306/health

# Test API docs
curl http://localhost:3306/docs

# Test with verbose output
curl -v -X POST http://localhost:3306/dataprep/process \
  -H "Content-Type: application/json" \
  -d '{"table_name": "dataset", "file_id": "test", "file_type": "csv"}'
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [PyHive Documentation](https://github.com/dropbox/PyHive)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

## 📄 License

[Your License Here]

## 📞 Support

For issues or questions:

- Check logs: `/data-prep-api/logs/data-prep-api.log`
- Review API documentation: `http://localhost:3306/docs`
- Contact: [your-email@example.com]
