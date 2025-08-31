from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=('.env.local', '.env')  # Tenta carregar .env.local primeiro, depois .env
    )                                    # Medida tomada para evitar vazamento da senha no gitHub
settings = Settings()