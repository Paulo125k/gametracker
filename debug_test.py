from app.integrations.igdb_client import get_access_token, search_game

token = get_access_token()
jogo = search_game("Skyrim", token)

if jogo is None:
    print("Jogo não encontrado.")
else:
    print(jogo)