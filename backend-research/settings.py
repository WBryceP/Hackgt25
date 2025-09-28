# settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RAPIDAPI_KEY: str
    RAPIDAPI_HOST: str = "yt-video-audio-downloader-api.p.rapidapi.com"

settings = Settings()
