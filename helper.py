import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET_KEY")
base_url = os.getenv("BASE_URL")
is_prod = os.getenv("PROD")
my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")