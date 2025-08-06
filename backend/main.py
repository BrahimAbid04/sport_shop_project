from fastapi import FastAPI, Depends
from backend import models
from .database import engine, Base, get_db  
from .models.product import Product  
from sqlalchemy.orm import Session
from fastapi import HTTPException  
from backend.schemas.product import ProductResponse, ProductCreate
from typing import List  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.post("/products/", response_model=ProductCreate)
async def create_product(
    product_data: ProductCreate,  
    db: Session = Depends(get_db)
):
    try:
        new_product = Product(
            name=product_data.name,
            price=product_data.price
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur: {str(e)}"
        )
        
@app.get("/products/", response_model=List[ProductResponse])  
async def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(models.Product).all()
        return products 
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de base de données: {str(e)}"
        )