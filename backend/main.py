from fastapi import FastAPI, Depends

from .database import engine, Base, get_db  
from .models.product import Product  
from sqlalchemy.orm import Session

app = FastAPI()

# Créez les tables
Base.metadata.create_all(bind=engine)

# Dépendance (identique à celle dans database.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/")
def create_product(name: str, price: float, db: Session = Depends(get_db)):
    db_product = product.Product(name=name, price=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    return db.query(product.Product).all()