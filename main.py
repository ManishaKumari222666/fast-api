
from fastapi import Depends, FastAPI
from models import Products
from database import sessionLocal, engine   
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine) #Create Tables

@app.get("/")
def home():
    return "Home Page"

products = [ Products(id=1, name="Notebook", description="Ltimindtree", price=20, quantity= 500),
             Products(id=2, name="Pen", description="Ltimindtree", price=5, quantity= 100),
              Products(id=3, name="Bottle", description="Ltimindtree", price=100, quantity= 500),
               Products(id=4, name="headphone", description="Ltimindtree", price=5000, quantity= 100) ]
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
         db.close()


def db_init():
   db = sessionLocal()
   count = db.query(database_models.Products).count
   if(count == 0):
        for product in products:
            db.add(database_models.Products(**product.model_dump()))
        db.commit()
    

db_init()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product 
    return "product not found"

@app.post("/products")
def add_product(product : Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int ,newProduct : Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db_product.id = newProduct.id
        db_product.name = newProduct.name
        db_product.description = newProduct.description
        db_product.price = newProduct.price
        db_product.quantity = newProduct.quantity
        db.commit()
        return "Product Updated"
    else:
        return "product not found"
    
@app.delete("/products/{id}")
def delete_product(id:int,  db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"
        

