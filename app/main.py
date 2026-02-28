import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.exceptions import RedirectToLogin
from app.routers import entries, sources, users

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    force=True,
)

app = FastAPI()

app.include_router(users.router)
app.include_router(sources.router)
app.include_router(entries.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET_KEY'),
    max_age=3600,  # an hour
    https_only=os.getenv('HTTPS_ONLY', 'false').lower() == 'true',
)


@app.exception_handler(RedirectToLogin)
def redirect_to_login(_request: Request, _exc: RedirectToLogin):
    return RedirectResponse('/users/login', status_code=303)


@app.get('/')
def root(request: Request):
    user_id = request.session.get('user_id')
    if user_id:
        return RedirectResponse('/entries/list', status_code=303)
    return RedirectResponse('/users/login', status_code=303)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
