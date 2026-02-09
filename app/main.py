from fastapi import FastAPI

from app.routers import sources, users

app = FastAPI()

app.include_router(users.router)
app.include_router(sources.router)
