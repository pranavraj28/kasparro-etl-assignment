from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Kasparro ETL")
app.include_router(router)
