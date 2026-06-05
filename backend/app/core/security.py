from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


SECRET_KEY = os
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60