from fastapi import FastAPI

from app.database import create_indexes
from app.routes import auth_routes, stats_routes, user_routes


app = FastAPI(
    title="Authentication System API",
    description="A simple backend-only authentication system using FastAPI and MongoDB.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event():
    create_indexes()


@app.get("/")
def root():
    return {"message": "Authentication System API is running"}


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(stats_routes.router)
