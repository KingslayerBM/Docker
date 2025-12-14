from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Any


def _dsn() -> str:
    host = os.getenv("DB_HOST", "db")
    port = int(os.getenv("DB_PORT", "5432"))
    name = os.getenv("DB_NAME", "shop")
    user = os.getenv("DB_USER", "shop")
    pwd = os.getenv("DB_PASS", "shop")
    return f"postgresql://{user}:{pwd}@{host}:{port}/{name}"


def create_pool() -> Any:
    """Create a psycopg ConnectionPool.

    Import is lazy so unit tests can run without DB dependencies installed.
    """
    from psycopg_pool import ConnectionPool  # type: ignore

    return ConnectionPool(conninfo=_dsn(), min_size=1, max_size=10, open=False)


def iter_migration_files(migrations_dir: Path) -> Iterable[Path]:
    files = sorted(p for p in migrations_dir.glob("*.sql") if p.is_file())
    return files


def run_migrations(pool: Any, migrations_dir: Path) -> None:
    files = list(iter_migration_files(migrations_dir))
    if not files:
        return

    with pool.connection() as conn:
        with conn.cursor() as cur:
            for f in files:
                sql = f.read_text(encoding="utf-8")
                cur.execute(sql)
        conn.commit()
