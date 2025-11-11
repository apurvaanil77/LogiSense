import os


class Settings:
    POSTGRES_DSN = os.getenv(
        "POSTGRES_DSN",
        "postgresql://root:root@localhost:5432/logisense",
    )
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    API_KEY = os.getenv("LOGISENSE_API_KEY", "change-me")
    ENV = os.getenv("ENV", "dev")


settings = Settings()
