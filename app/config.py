import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEXT_PUBLIC_STACK_PROJECT_ID: str = os.getenv("NEXT_PUBLIC_STACK_PROJECT_ID", "")
    NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY: str = os.getenv("NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY", "")
    STACK_SECRET_SERVER_KEY: str = os.getenv("STACK_SECRET_SERVER_KEY", "")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise RuntimeError("Defina DATABASE_URL no .env ou nas ENV Vars")

    AUTH_API_URL: str = os.getenv("API_SENHAS_URL", "https://api-senhas.vercel.app")

settings = Settings()
