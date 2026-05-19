from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime

from database import engine, get_db
from db_models import ProductORM, Base
from model import Product, ProductCreate, ProductUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getallproducts")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(ProductORM).all()


@app.get("/getproductbyid/{id}")
def get_product_by_id(id: UUID, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/addproduct", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductORM(
        id=str(uuid4()),
        name=product.name,
        description=product.description,
        price=product.price,
        is_active=product.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete("/deleteproduct/{id}")
def delete_product(id: UUID, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product '{product.name}' deleted successfully"}


@app.put("/updateproduct/{id}", response_model=Product)
def update_product(id: UUID, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    if data.is_active is not None:
        product.is_active = data.is_active

    product.updated_at = datetime.now()
    db.commit()
    db.refresh(product)
    return product


