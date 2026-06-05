from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.core.logger import get_logger
from app.api import auth as auth_v1


load_dotenv() 

logger = get_logger(__name__)
app = FastAPI()

# Register API routers
app.include_router(auth_v1.router, prefix="/api/v1")

