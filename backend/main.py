from fastapi import FastAPI, Depends
from .database import engine, Base, get_db  
from .models.product import Product  
from sqlalchemy.orm import Session
from fastapi import HTTPException  
from . import schemas
from .schemas.product import ProductCreate
from fastapi.encoders import jsonable_encoder
from typing import List  

app = FastAPI()


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
@app.get("/products/", response_model=List[schemas.ProductResponse])  
async def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(models.Product).all()
        return jsonable_encoder(products)  
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de base de données: {str(e)}"
        )