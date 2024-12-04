from sqlalchemy import Column, Integer, String,Text
from sqlalchemy.orm import DeclarativeBase

from storage.postgresql.main import BaseCustom


class Image(BaseCustom):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    saved_address = Column(String(255), nullable=False)
    src = Column(Text, nullable=False)
    query = Column(Text, nullable=True)
