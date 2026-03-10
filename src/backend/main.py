from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload

app = FastAPI(title="Contract Comparator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contract Comparator API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
