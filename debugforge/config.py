import os
from dotenv import load_dotenv

load_dotenv()

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

NEBIUS_BASE_URL = os.getenv(
    "NEBIUS_BASE_URL",
    "https://api.tokenfactory.nebius.com/v1/"
)

NEBIUS_MODEL = os.getenv("NEBIUS_MODEL")


if not NEBIUS_API_KEY:
    raise ValueError("NEBIUS_API_KEY is missing")

if not NEBIUS_MODEL:
    raise ValueError("NEBIUS_MODEL is missing")