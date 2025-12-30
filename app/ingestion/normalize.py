from sqlalchemy.orm import Session
from app.core.models import Coin, CoinSource, Price


def normalize_and_store(
    db: Session,
    *,
    symbol: str,
    name: str,
    source: str,
    source_id: str,
    price_usd: float
):
    """
    Core normalization function.

    Rules:
    - One coin per symbol (BTC exists once)
    - Multiple sources map to the same coin
    - Prices always link to canonical coin
    """

    # 1. Normalize symbol
    symbol = symbol.upper().strip()

    # 2. Get or create canonical coin
    coin = db.query(Coin).filter_by(symbol=symbol).first()
    if not coin:
        coin = Coin(symbol=symbol, name=name)
        db.add(coin)
        db.flush()  # assigns coin.id without commit

    # 3. Ensure source mapping exists
    mapping = db.query(CoinSource).filter_by(
        source=source,
        source_id=source_id
    ).first()

    if not mapping:
        mapping = CoinSource(
            coin_id=coin.id,
            source=source,
            source_id=source_id
        )
        db.add(mapping)

    # 4. Store price linked to canonical coin
    price = Price(
        coin_id=coin.id,
        source=source,
        price_usd=price_usd
    )
    db.add(price)
