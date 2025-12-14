from fastapi import FastAPI
from adapters.http.routes import build_router
from config.di import build_usecases

def create_app() -> FastAPI:
    app = FastAPI(title="Hexagonal Orders API", version="1.0.0")
    create_uc, get_uc = build_usecases()
    app.include_router(build_router(create_uc, get_uc))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()
