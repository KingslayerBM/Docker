from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from fastapi import FastAPI

from app.application.contracts import ProductRepository
from app.infrastructure.cache import create_redis_client
from app.infrastructure.db import create_pool, run_migrations
from app.infrastructure.product_repository import CachedProductRepository, PostgresProductRepository
from app.presentation.controllers import router


def create_app() -> FastAPI:
    app = FastAPI(title="Layered Monolith Shop", version="1.0.0")

    testing = os.getenv("TESTING") == "1"

    if not testing:
        pool = create_pool()
        redis_client = create_redis_client()

        def repo_factory() -> ProductRepository:
            repo: ProductRepository = PostgresProductRepository(pool)
            if redis_client is not None:
                repo = CachedProductRepository(repo, redis_client)
            return repo

        app.state.pool = pool
        app.state.redis = redis_client
        app.state.repo_factory = repo_factory
    else:
        # tests can override repo_factory without requiring DB/Redis libs
        app.state.pool = None
        app.state.redis = None
        app.state.repo_factory = lambda: None  # will be overridden in tests

    @app.on_event("startup")
    def _startup() -> None:
        if testing:
            return
        app.state.pool.open()
        migrations_dir = Path(__file__).parent / "infrastructure" / "migrations"
        run_migrations(app.state.pool, migrations_dir)

        if app.state.redis is not None:
            try:
                app.state.redis.ping()
            except Exception:
                app.state.redis = None

    @app.on_event("shutdown")
    def _shutdown() -> None:
        if testing:
            return
        app.state.pool.close()
        if app.state.redis is not None:
            try:
                app.state.redis.close()
            except Exception:
                pass

    app.include_router(router)
    return app


app = create_app()
