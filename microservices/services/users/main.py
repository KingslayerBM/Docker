from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Users Service", version="1.0.0")

USERS = {
    1: {"id": 1, "email": "alice@example.com"},
    2: {"id": 2, "email": "bob@example.com"},
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=user)
