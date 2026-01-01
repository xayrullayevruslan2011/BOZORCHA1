from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Frontend bilan bog'lanish uchun ruxsat berish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    name: str
    phone: str
    product: str
    price: str
    size: str

@app.post("/api/orders")
async def create_order(order: Order):
    print(f"Yangi buyurtma: {order.name} - {order.product}")
    return {"status": "ok", "message": "Buyurtma qabul qilindi"}
