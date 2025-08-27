import os
from dotenv import load_dotenv

load_dotenv()

MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CACHE_DIR = os.getenv('CACHE_DIR', './data/cache')