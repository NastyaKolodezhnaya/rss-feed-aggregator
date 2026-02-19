import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.routers import sources, users

load_dotenv()

app = FastAPI()

app.include_router(users.router)
app.include_router(sources.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET_KEY'),
    max_age=3600,  # an hour
    https_only=os.getenv('HTTPS_ONLY', 'false').lower() == 'true',
)
