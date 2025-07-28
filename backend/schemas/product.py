from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    name: str
    price: float

class Product(ProductBase):
    id: int

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True 
    
