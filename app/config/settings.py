from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from datetime import timedelta
from typing import Optional
import certifi
from pymongo import AsyncMongoClient

load_dotenv()

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "hobby_discoverer"
    
    # API Keys
    # TICKETMASTER_API_KEY: str = os.getenv("TICKETMASTER_API_KEY")
    
    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")  # You should generate this
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"

settings = Settings()

class MongoManager:
    client: Optional[AsyncMongoClient] = None
    db = None

    @classmethod
    def connect(cls):
        cls.client = AsyncMongoClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where()
        )
        cls.db = cls.client[settings.DATABASE_NAME]

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()

    @classmethod
    def get_collection(cls, name: str):
        if cls.db is None:
            raise RuntimeError("MongoDB connection not established. Call connect() first.")
        return cls.db[name]