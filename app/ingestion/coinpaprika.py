import httpx
from sqlalchemy.orm import Session
from app.ingestion.normalize import normalize_and_store


COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/tickers"


def ingest_coinpaprika(db: Session):
    """
    Fetch data from CoinPaprika and store it using the SAME normalization logic.
    """

    response = httpx.get(COINPAPRIKA_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    # limit to top 10 to match CoinGecko
    for item in data[:10]:
        normalize_and_store(
            db=db,
            symbol=item["symbol"],
            name=item["name"],
            source="coinpaprika",
            source_id=item["id"],
            price_usd=item["quotes"]["USD"]["price"]
        )

    db.commit()
