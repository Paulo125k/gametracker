from sqlalchemy.orm import Session

from app.models.game import Game


def save_game(db: Session, jogo: dict) -> Game:
    """Salva um jogo no banco, evitando duplicar pelo igdb_id.

    Se o jogo já existir (mesmo igdb_id), atualiza os dados.
    Caso contrário, cria um novo registro.
    """
    igdb_id = jogo["id"]

    existente = db.query(Game).filter(Game.igdb_id == igdb_id).first()

    genres = ", ".join(g["name"] for g in jogo.get("genres", []))
    cover_image_id = jogo.get("cover", {}).get("image_id")

    if existente:
        existente.name = jogo.get("name")
        existente.release_date = jogo.get("first_release_date")
        existente.rating = jogo.get("rating")
        existente.genres = genres
        existente.cover_image_id = cover_image_id
        existente.summary = jogo.get("summary")
        db.commit()
        return existente

    novo_jogo = Game(
        igdb_id=igdb_id,
        name=jogo.get("name"),
        release_date=jogo.get("first_release_date"),
        rating=jogo.get("rating"),
        genres=genres,
        cover_image_id=cover_image_id,
        summary=jogo.get("summary"),
    )
    db.add(novo_jogo)
    db.commit()
    db.refresh(novo_jogo)
    return novo_jogo