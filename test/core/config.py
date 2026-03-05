import os
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
load_dotenv()


class Settings(BaseSettings):
    # TWILIO_AUTH_TOKEN:str = os.getenv("TWILIO_AUTH_TOKEN")
    DEEPGRAM_API_KEY:str = os.getenv("DEEPGRAM_API_KEY")
    # OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY:str=os.getenv("GROQ_API_KEY")
    DEEPGRAM_URL:str=os.getenv("DEEPGRAM_URL")
    TTS_MODEL:str=os.getenv("TTS_MODEL")
    CHAT_MODEL:str=os.getenv("CHAT_MODEL")

    model_config = ConfigDict(env_file=".env", extra="allow")

settings = Settings()
