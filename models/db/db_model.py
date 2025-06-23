# db_mode
from sqlalchemy import Column, Integer, Numeric, String

from scripts.db_config import Base


class Borrow(Base):
    __tablename__ = "borrow"
    id: Column[int] = Column(Integer, primary_key=True)
    user_address: Column[str] = Column(String, index=True)
    reserve: Column[str] = Column(String)
    amount: Column[int] = Column(Numeric)
    block: Column[int] = Column(Integer)
    timestamp: Column[int] = Column(Integer)
