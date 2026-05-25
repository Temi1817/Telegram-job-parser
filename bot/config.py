import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    DATABASE_PATH: str = field(default_factory=lambda: os.getenv("DATABASE_PATH", "jobs.db"))
    UPDATE_INTERVAL_MINUTES: int = field(default_factory=lambda: int(os.getenv("UPDATE_INTERVAL_MINUTES", "30")))
