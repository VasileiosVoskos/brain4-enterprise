import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
LEGAL_DIR = DATA_DIR / "legal"
OCR_DIR = DATA_DIR / "ocr"
TEMP_DIR = DATA_DIR / "temp"

# Create directories if they don't exist
for directory in [DATA_DIR, UPLOADS_DIR, LEGAL_DIR, OCR_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File type configurations
ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif"
]

ALLOWED_DOCUMENT_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

# Database configuration
DATABASE_URL = "sqlite:///data/brain4.db"

# Email configuration
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "sender_email": os.getenv("SENDER_EMAIL", ""),
    "sender_password": os.getenv("SENDER_PASSWORD", "")
}

# OpenAI configuration
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    "model": "gpt-4-turbo-preview",
    "temperature": 0.7,
    "max_tokens": 2000
}

# Application settings
APP_SETTINGS = {
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "max_upload_size": 10 * 1024 * 1024,  # 10MB
    "session_timeout": 3600,  # 1 hour
    "max_retries": 3
}
