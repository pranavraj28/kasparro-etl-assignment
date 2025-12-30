# Kasparro Backend & ETL Assignment

This project implements a production-ready ETL system that ingests cryptocurrency data from multiple sources, **normalizes identity across sources**, and exposes a clean backend API.

The core focus of this assignment is **identity unification** — ensuring that the same coin (e.g., BTC) exists **once** regardless of how many sources provide data for it.

---

## 🔑 Key Design Principle: Canonical Coin Identity

Instead of storing assets as `(symbol, source)` pairs, this system introduces a **canonical coin entity**.

### Canonical Model
- Each cryptocurrency (BTC, ETH, etc.) exists **once** in the `coins` table.
- Source-specific identifiers are mapped via a separate `coin_sources` table.
- All prices link to the canonical coin.

This ensures:
- No duplicate BTC entries
- Unified querying across sources
- Correct ETL normalization (core assignment requirement)

---

## 🗂️ Architecture Overview

app/
├── core/
│ ├── database/ # SQLAlchemy engine & session
│ └── models.py # Canonical data models
├── ingestion/
│ ├── normalize.py # Core normalization logic
│ ├── coingecko.py # CoinGecko ingestion
│ └── coinpaprika.py # CoinPaprika ingestion
├── api/
│ └── routes/
│ └── data.py # /data API


---

## 🔄 ETL Flow

1. Fetch data from source (CoinGecko / CoinPaprika)
2. Normalize symbol (e.g., `btc → BTC`)
3. Get or create **canonical coin**
4. Map source-specific ID to canonical coin
5. Store price linked to canonical coin

This guarantees identity unification across all sources.

---

## 🌐 API Endpoints

### `GET /data`

Returns unified coin data across all sources.

Example response:

```json
[
  {
    "symbol": "BTC",
    "name": "Bitcoin",
    "sources": ["coingecko", "coinpaprika"],
    "latest_price_usd": 87593.11
  }
]
