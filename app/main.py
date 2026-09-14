from app.integrations.igdb_client import get_access_token, search_game

if __name__ == "__main__":
    token = get_access_token()
    jogo = search_game("The Witcher 3", token)

    if jogo is None:
        print("Jogo não encontrado.")
    else:
        print(jogo)