import requests
from app.core.config import IGDB_CLIENT_ID, IGDB_CLIENT_SECRET

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
GAMES_URL = "https://api.igdb.com/v4/games"

PALAVRAS_IGNORADAS = ["remaster", "edition", "goty", "bundle", "+ ", "soundtrack", "dlc"]


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


def eh_edicao_especial(nome: str) -> bool:
    """Verifica se o nome do jogo indica uma edição especial/bundle."""
    nome_lower = nome.lower()
    return any(palavra in nome_lower for palavra in PALAVRAS_IGNORADAS)


def search_game(name: str, access_token: str) -> dict | None:
    """Busca jogos na IGDB pelo nome e retorna o resultado mais adequado.

    Prioriza jogos com category == 0 (main_game) e que não pareçam
    ser edições especiais/bundles pelo nome. Se nenhum resultado
    passar nos dois critérios, retorna o primeiro da lista como fallback.
    """
    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    query = f"""
        search "{name}";
        fields name, category, first_release_date, rating, genres.name, cover.image_id, summary;
        limit 10;
    """
    response = requests.post(GAMES_URL, headers=headers, data=query)
    response.raise_for_status()
    resultados = response.json()

    if not resultados:
        return None

    main_games = [
        jogo for jogo in resultados
        if jogo.get("category", 0) == 0 and not eh_edicao_especial(jogo.get("name", ""))
    ]

    if main_games:
        return main_games[0]

    return resultados[0]