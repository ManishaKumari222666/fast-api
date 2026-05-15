
from fastapi import FastAPI
from models import Products
from database import sessionLocal, engine   
import database_models

app = FastAPI()

@app.get("/")
def home():
    return "Home Page"

products = [ Products(id=1, name="Notebook", description="Ltimindtree", price=20, quantity= 500),
             Products(id=2, name="Pen", description="Ltimindtree", price=5, quantity= 100),
              Products(id=3, name="Bottle", description="Ltimindtree", price=100, quantity= 500),
               Products(id=4, name="headphone", description="Ltimindtree", price=5000, quantity= 100) ]

database_models.Base.metadata.create_all(bind=engine) #Create Tables

def db_init():
    db = sessionLocal()

    for product in products:
        db.add(database_models.Products(**product.model_dump()))

    db.commit()

db_init()

@app.get("/products")
def get_all_products():
    db = sessionLocal()
    db.query()
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    print(product)  
    return "product not found"

@app.post("/product")
def add_product(product : Products):
    products.append(product)
    return products

@app.put("/product/{id}")
def update_product(id:int ,newProduct : Products):
   for i in range(len(products)):
    if products[i].id == id:
        products[i] = newProduct
        return "updated successfully"

    return "product not found"

@app.delete("/product/{id}")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted"
    return "Product not found"
        

