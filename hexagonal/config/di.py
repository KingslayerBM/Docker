import os
from typing import Tuple
from dotenv import load_dotenv

from config.settings import load_settings
from core.usecases.create_order import CreateOrder
from core.usecases.get_order import GetOrder
from core.ports.order_repository import OrderRepository

from adapters.db.db import load_db_config, wait_for_db, run_migrations
from adapters.db.repository import PostgresOrderRepository
from adapters.file.repository import CsvOrderRepository

def build_usecases() -> Tuple[CreateOrder, GetOrder]:
    load_dotenv(override=False)
    settings = load_settings()

    if settings.repo_adapter == "db":
        db_cfg = load_db_config()
        wait_for_db(db_cfg, timeout_s=45)
        migrations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "adapters", "db", "migrations"))
        run_migrations(db_cfg, migrations_dir)
        repo: OrderRepository = PostgresOrderRepository(db_cfg)
    elif settings.repo_adapter == "file":
        repo = CsvOrderRepository(settings.csv_path)
    else:
        raise RuntimeError(f"Unknown REPO_ADAPTER={settings.repo_adapter} (use 'db' or 'file')")

    return CreateOrder(repo), GetOrder(repo)
