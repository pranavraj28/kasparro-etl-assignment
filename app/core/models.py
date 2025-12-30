from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database.db import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)  # BTC
    name = Column(String, nullable=False)                 # Bitcoin


class CoinSource(Base):
    __tablename__ = "coin_sources"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coins.id"), nullable=False)
    source = Column(String, nullable=False)               # coingecko
    source_id = Column(String, nullable=False)            # gecko id

    coin = relationship("Coin")

    __table_args__ = (
        UniqueConstraint("source", "source_id"),
    )


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coins.id"), nullable=False)
    source = Column(String, nullable=False)
    price_usd = Column(Float)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    coin = relationship("Coin")
