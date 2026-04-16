from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class defines the settings for the app
    """
    POSTGRES_URL: str
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    
    # Admin User Configuration
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
