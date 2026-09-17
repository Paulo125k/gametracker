import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher

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


def normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas, para comparação de texto."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def similaridade(a: str, b: str) -> float:
    """Retorna um score de 0 a 1 de quão parecidos dois textos são."""
    return SequenceMatcher(None, normalizar(a), normalizar(b)).ratio()


def search_game(name: str, access_token: str) -> dict | None:
    """Busca jogos na IGDB pelo nome e retorna o resultado mais adequado.

    Entre os candidatos que são main_game e não parecem edições especiais,
    escolhe o que tem o nome mais parecido com o termo buscado (em vez de
    simplesmente confiar na ordem de relevância da IGDB).
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

    candidatos = [
        jogo for jogo in resultados
        if jogo.get("category", 0) == 0 and not eh_edicao_especial(jogo.get("name", ""))
    ]

    if not candidatos:
        return resultados[0]

    melhor = max(candidatos, key=lambda jogo: similaridade(name, jogo.get("name", "")))
    return melhor

def discover_games(
    access_token: str,
    year: int | None = None,
    min_rating: float | None = None,
    limit: int = 20,
) -> list[dict]:
    """Busca jogos por critérios, sem precisar informar um nome.

    year: filtra jogos lançados nesse ano.
    min_rating: filtra jogos com nota mínima (0 a 100).
    limit: quantidade máxima de resultados.
    """
    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }

    condicoes = []

    if year:
        inicio = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
        fim = int(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp())
        condicoes.append(f"first_release_date >= {inicio}")
        condicoes.append(f"first_release_date <= {fim}")

    if min_rating:
        condicoes.append(f"rating >= {min_rating}")

    # Pedimos mais resultados do que o limite final, porque parte
    # será descartada no filtro de categoria feito em Python.
    limit_bruto = limit * 3

    if condicoes:
        where_clause = " & ".join(condicoes)
        query = f"""
            fields name, category, first_release_date, rating, genres.name, cover.image_id, summary;
            where {where_clause};
            sort rating desc;
            limit {limit_bruto};
        """
    else:
        query = f"""
            fields name, category, first_release_date, rating, genres.name, cover.image_id, summary;
            sort rating desc;
            limit {limit_bruto};
        """

    response = requests.post(GAMES_URL, headers=headers, data=query)
    response.raise_for_status()
    resultados = response.json()

    apenas_principais = [
        jogo for jogo in resultados
        if jogo.get("category", 0) == 0 and not eh_edicao_especial(jogo.get("name", ""))
    ]

    return apenas_principais[:limit]