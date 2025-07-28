from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # OPENAI API key
    OPENAI_API_KEY: str
    OPENAI_LLM_MODEL: str = "gpt-4o"
    OPENAI_LLM_MODEL_SUMMARY: str = "gpt-4o"


    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5


    # --- Comet ML & Opik Configuration ---
    COMET_API_KEY: str | None = Field(
        default=None, description="API key for Comet ML and Opik services."
    )
    COMET_PROJECT: str = Field(
        default="mpdagents_course",
        description="Project name for Comet ML and Opik tracking.",
    )

    # # --- MongoDB Configuration ---
    # MONGO_URI: str = Field(
    #     default="mongodb://mpdagents:mpdagents@localhost:27017/?directConnection=true",
    #     description="Connection URI for the local MongoDB Atlas instance.",
    # )
    # MONGO_DB_NAME: str = "mpdagents"
    # MONGO_STATE_CHECKPOINT_COLLECTION: str = "mpdagents_state_checkpoints"
    # MONGO_STATE_WRITES_COLLECTION: str = "mpdagents_state_writes"
    # MONGO_LONG_TERM_MEMORY_COLLECTION: str = "mpdagents_long_term_memory"

    MONGO_URI: str 
    MONGO_DB_NAME: str 
    MONGO_STATE_CHECKPOINT_COLLECTION: str 
    MONGO_STATE_WRITES_COLLECTION: str
    
settings = Settings()
