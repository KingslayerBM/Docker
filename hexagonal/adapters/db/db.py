import os
import time
from dataclasses import dataclass
import psycopg

@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return f"host={self.host} port={self.port} dbname={self.name} user={self.user} password={self.password}"

def load_db_config() -> DbConfig:
    return DbConfig(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        name=os.getenv("DB_NAME", "shop"),
        user=os.getenv("DB_USER", "shop"),
        password=os.getenv("DB_PASS", "shop"),
    )

def wait_for_db(cfg: DbConfig, timeout_s: int = 45) -> None:
    deadline = time.time() + timeout_s
    last_err = None
    while time.time() < deadline:
        try:
            with psycopg.connect(cfg.dsn) as conn:
                conn.execute("SELECT 1;").fetchone()
            return
        except Exception as e:
            last_err = e
            time.sleep(1)
    raise RuntimeError(f"DB not ready after {timeout_s}s: {last_err}")

def run_migrations(cfg: DbConfig, migrations_dir: str) -> None:
    files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])
    if not files:
        return
    with psycopg.connect(cfg.dsn) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS _migrations (name TEXT PRIMARY KEY);")
        for fname in files:
            if conn.execute("SELECT 1 FROM _migrations WHERE name=%s;", (fname,)).fetchone():
                continue
            with open(os.path.join(migrations_dir, fname), "r", encoding="utf-8") as f:
                conn.execute(f.read())
            conn.execute("INSERT INTO _migrations(name) VALUES (%s);", (fname,))
        conn.commit()
