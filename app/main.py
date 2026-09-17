from app.core.database import SessionLocal
from app.integrations.igdb_client import get_access_token
from app.services.collector import collect_games
from app.repositories.game_repository import save_game
from app.exporters.excel_exporter import export_games_to_excel

JOGOS_PARA_BUSCAR = [
    "The Witcher 3",
    "Red Dead Redemption 2",
    "Cyberpunk 2077",
    "God of War Ragnarök",
    "Horizon Forbidden West",
]

if __name__ == "__main__":
    token = get_access_token()
    resultado = collect_games(JOGOS_PARA_BUSCAR, token)

    print(f"\n{len(resultado['encontrados'])} jogos encontrados:")
    for jogo in resultado["encontrados"]:
        print(f"  - {jogo['name']}")

    if resultado["nao_encontrados"]:
        print(f"\n{len(resultado['nao_encontrados'])} não encontrados:")
        for nome in resultado["nao_encontrados"]:
            print(f"  - {nome}")

    db = SessionLocal()
    try:
        print("\nSalvando no banco de dados...")
        for jogo in resultado["encontrados"]:
            salvo = save_game(db, jogo)
            print(f"  - {salvo.name} (id no banco: {salvo.id})")

        print("\nExportando para Excel...")
        export_games_to_excel(db, "output/jogos.xlsx")
        print("Planilha gerada em output/jogos.xlsx")
    finally:
        db.close()