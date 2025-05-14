import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_TITLE = os.getenv("API_TITLE", "My data getter XD")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Data getter API Description")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("ENV", "development")

    API_VERSION_V1 = "v1"

    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "")

    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
