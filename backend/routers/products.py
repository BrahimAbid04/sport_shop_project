from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, Product
from database import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all() 
