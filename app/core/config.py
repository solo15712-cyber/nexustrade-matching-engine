from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "NexusTrade High-Load Order Engine"
    VERSION: str = "2.5.0"
    API_V1_STR: str = "/api/v1"
    MAX_ORDERS_IN_MEMORY: int = 100_000
    REDIS_URL: str = "redis://localhost:6379/0"

settings = Settings()
