import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get(
    "API_URL", "https://i50replq2a.execute-api.us-east-1.amazonaws.com/Prod"
)
