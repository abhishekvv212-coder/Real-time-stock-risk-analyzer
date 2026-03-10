from sqlalchemy import Column, String, Float, BigInteger, DateTime
from sqlalchemy.sql import func
from db.connection import Base

class Stock(Base):
    __tablename__ = "stocks"

    symbol = Column(String, primary_key=True)
    company = Column(String)
    price = Column(Float)
    currency = Column(String)
    market_cap = Column(BigInteger)
    high_52w = Column(Float)
    low_52w = Column(Float)
    pe_ratio = Column(Float)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())