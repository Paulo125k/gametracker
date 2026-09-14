from app.integrations.igdb_client import get_access_token, search_game

if __name__ == "__main__":
    token = get_access_token()
    resultados = search_game("The Witcher 3", token)

    for jogo in resultados:
        print(jogo.get("name"), "-", jogo.get("rating"))