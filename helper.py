import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET_KEY")
base_url = os.getenv("BASE_URL")