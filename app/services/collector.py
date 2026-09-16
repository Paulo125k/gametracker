from app.integrations.igdb_client import search_game


def collect_games(names: list[str], access_token: str) -> dict:
    """Busca uma lista de jogos na IGDB.

    Retorna um dicionário com duas listas: os jogos encontrados
    e os nomes que não retornaram nenhum resultado.
    """
    encontrados = []
    nao_encontrados = []

    for name in names:
        jogo = search_game(name, access_token)

        if jogo is None:
            nao_encontrados.append(name)
        else:
            encontrados.append(jogo)

    return {
        "encontrados": encontrados,
        "nao_encontrados": nao_encontrados,
    }