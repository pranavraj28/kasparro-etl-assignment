from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.db import SessionLocal
from app.core.models import Coin, CoinSource, Price

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/data")
def get_data(db: Session = Depends(get_db)):
    response = []

    coins = db.query(Coin).all()

    for coin in coins:
        sources = (
            db.query(CoinSource.source)
            .filter(CoinSource.coin_id == coin.id)
            .all()
        )
        source_list = [s[0] for s in sources]

        latest_price = (
            db.query(Price)
            .filter(Price.coin_id == coin.id)
            .order_by(Price.fetched_at.desc())
            .first()
        )

        response.append({
            "symbol": coin.symbol,
            "name": coin.name,
            "sources": source_list,
            "latest_price_usd": latest_price.price_usd if latest_price else None
        })

    return response
