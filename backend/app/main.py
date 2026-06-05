from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.core.logger import get_logger
from app.api import auth as auth_v1
from app.helpers.exceptionHandler import setup_exception_handlers
from app.middleware.token_middleware import add_token_middleware

load_dotenv() 

logger = get_logger(__name__)
app = FastAPI()


# Set up custom exception handlers
setup_exception_handlers(app)

# Add token middleware (requires `token` header on every request)
add_token_middleware(app)

# Register API routers
app.include_router(auth_v1.router, prefix="/api/v1")

