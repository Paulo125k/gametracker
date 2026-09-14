import requests
from app.core.config import IGDB_CLIENT_ID, IGDB_CLIENT_SECRET

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
GAMES_URL = "https://api.igdb.com/v4/games"


def get_access_token() -> str:
    """Solicita um access token à Twitch usando o fluxo client credentials."""
    response = requests.post(
        TOKEN_URL,
        params={
            "client_id": IGDB_CLIENT_ID,
            "client_secret": IGDB_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


def search_game(name: str, access_token: str) -> list[dict]:
    """Busca jogos na IGDB pelo nome e retorna os campos básicos."""
    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    query = f"""
        search "{name}";
        fields name, first_release_date, rating, genres.name, cover.image_id, summary;
        limit 5;
    """
    response = requests.post(GAMES_URL, headers=headers, data=query)
    response.raise_for_status()
    return response.json()