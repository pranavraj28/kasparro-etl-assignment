import httpx
from sqlalchemy.orm import Session
from app.ingestion.normalize import normalize_and_store


COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def ingest_coingecko(db: Session):
    """
    Fetch data from CoinGecko and store it using normalization logic.
    """

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    response = httpx.get(COINGECKO_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    for item in data:
        normalize_and_store(
            db=db,
            symbol=item["symbol"],
            name=item["name"],
            source="coingecko",
            source_id=item["id"],
            price_usd=item["current_price"]
        )

    db.commit()
