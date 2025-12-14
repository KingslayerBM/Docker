import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    port: int
    repo_adapter: str
    csv_path: str

def load_settings() -> Settings:
    return Settings(
        port=int(os.getenv("PORT", "8081")),
        repo_adapter=os.getenv("REPO_ADAPTER", "db").strip().lower(),
        csv_path=os.getenv("CSV_PATH", "/data/orders.csv"),
    )
