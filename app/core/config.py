import os
from dotenv import load_dotenv

load_dotenv()

IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
IGDB_CLIENT_SECRET = os.getenv("IGDB_CLIENT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

if not IGDB_CLIENT_ID or not IGDB_CLIENT_SECRET:
    raise RuntimeError(
        "IGDB_CLIENT_ID e IGDB_CLIENT_SECRET precisam estar definidos no .env"
    )

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL precisa estar definida no .env")