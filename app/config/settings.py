from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI PDF Extraction API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_UPLOAD_TOPIC: str
    KAFKA_GROUP: str
    
    TESSERACT_CMD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
