from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Data Preparation API"
    VERSION: str = "1.0.0"
    
    # Database settings
    PSQL_HOST: str = os.getenv("PSQL_HOST", "localhost")
    PSQL_DATABASE: str = os.getenv("PSQL_DATABASE", "")
    PSQL_PORT: str = os.getenv("PSQL_PORT", "5432")
    PSQL_USER: str = os.getenv("PSQL_USER", "")
    PSQL_PASSWORD: str = os.getenv("PSQL_PASSWORD", "")
    
    # File settings
    URL: str = os.getenv("URL", "")
    URL2: str = os.getenv("URL2", "")  # Feature store URL
    URL3: str = os.getenv("URL3", "")  # Training dataset URL
    LOCAL_DIR: str = os.getenv("LOCAL_DIR", "/tmp/dataprep")

    # Redis settings (for feature store)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # Hive settings (for feature store)
    HIVE_HOST: str = os.getenv("HIVE_HOST", "localhost")
    HIVE_PORT: int = int(os.getenv("HIVE_PORT", "10000"))
    HIVE_PRINCIPAL: str = os.getenv("HIVE_PRINCIPAL", "")
    HIVE_DATABASE: str = os.getenv("HIVE_DATABASE", "default")
    
    # HDFS settings (for training datasets)
    HADOOP_HOME: str = os.getenv("HADOOP_HOME", "/usr/hadoop")
    HDFS_NAMENODE: str = os.getenv("HDFS_NAMENODE", "localhost")
    TICKET_CACHE_PATH: str = os.getenv("TICKET_CACHE_PATH", "/tmp/krb5cc_1062")
    
    # Logging settings
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "logs/dataset.log")
    MAX_LOG_SIZE: int = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT: int = 5
    
    # API settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_FILE_TYPES: list = ['csv', 'tsv', 'xls', 'xlsx', 'sav']
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.PSQL_USER}:{self.PSQL_PASSWORD}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_DATABASE}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()