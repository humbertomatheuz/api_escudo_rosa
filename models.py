from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db" # Nome do seu arquivo de banco de dados SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Contato(Base):
    __tablename__ = "contatos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    local = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False) # Armazenar timestamp como número

class Denuncia(Base):
    __tablename__ = "denuncias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True)
    identificar = Column(Boolean, nullable=False) # Armazenar como Boolean
    motivo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    agressor = Column(String, nullable=True)
    createdAt = Column(String, nullable=False) # Manter como string, conforme seu tipo

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    local = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False)

class Informacao(Base):
    __tablename__ = "informacoes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    local = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    avatarColor = Column(String, nullable=True)

# Função para criar todas as tabelas no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tabelas do banco de dados criadas com sucesso!")