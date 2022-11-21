from sqlmodel import create_engine, SQLModel, Session
from src.constants.const import System

engine = create_engine(f"sqlite:///{System.SQLITE_FILE_PATH}", echo=True)
