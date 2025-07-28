from fastapi import FastAPI, Depends
from .database import engine, Base, get_db  
from .models.product import Product  
from sqlalchemy.orm import Session
from fastapi import HTTPException  
from .schemas.product import ProductCreate

app = FastAPI()

# Créez les tables
Base.metadata.create_all(bind=engine)


@app.post("/products/", response_model=ProductCreate)
async def create_product(
    product_data: ProductCreate,  # Utilise le schéma
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
@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    return db.query(product.Product).all()