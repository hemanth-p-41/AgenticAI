from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent.joinpath('.env'))

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./dev.db')
# Support both SECRET_KEY and JWT_SECRET env names for flexibility
SECRET_KEY = os.getenv('SECRET_KEY', os.getenv('JWT_SECRET', 'change-me'))
ALGORITHM = os.getenv('ALGORITHM', os.getenv('JWT_ALGORITHM', 'HS256'))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
