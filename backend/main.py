from fastapi import FastAPI
from backend.database import engine, Base
from .models.product import Product
from routers import products

Base.metadata.create_all(bind=engine)  # Crée les tables

app = FastAPI()
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "API de produits sportifs"}
