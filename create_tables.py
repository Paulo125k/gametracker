from app.core.database import Base, engine
from app.models.game import Game

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")