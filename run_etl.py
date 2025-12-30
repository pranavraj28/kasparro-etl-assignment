from app.core.database.db import SessionLocal
from app.ingestion.coingecko import ingest_coingecko
from app.ingestion.coinpaprika import ingest_coinpaprika

db = SessionLocal()

ingest_coingecko(db)
ingest_coinpaprika(db)

db.close()

print("CoinGecko + CoinPaprika ingestion completed")
