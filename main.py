from typing import List
from fastapi import FastAPI
from src.services.customer_service import CustomerService
from src.types.models import Customer

customer_service = CustomerService()

app = FastAPI(
    title="Customer Management API",
    description="A FastAPI backend with customer management services",
    version="1.0.0"
)

@app.get("/", status_code=200)
async def root():
    return {"message": "Up and running"}

@app.post("/customers", status_code=201)
async def create_customers(customers: List[Customer]):
    result = customer_service.add_customers(customers)
    return {
        "inserted": result["inserted"],
        "failed": result["failed"]
    }

@app.get("/customers", status_code=200)
async def get_customers():
    return {
        "customers": customer_service.get_customers()
    }

@app.delete("/customers", status_code=204)
async def delete_all_customers():
    customer_service.delete_all_customers()
    return