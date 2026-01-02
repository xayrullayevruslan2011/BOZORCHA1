from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    user_name: str
    phone: str
    product: str
    price: str
    size: str

db_orders = []

@app.get("/")
def read_root():
    return {"status": "Ruslan Market Backend is running!"}

@app.post("/api/orders")
async def create_order(order: Order):
    db_orders.append(order.dict())
    
    # Summani raqamga aylantirish (masalan: "250,000 so'm" -> 250000)
    try:
        clean_amount = int(''.join(filter(str.isdigit, order.price))) * 100 # Tiyinda
    except:
        clean_amount = 0

    # PAYME INTEGRATSIYASI
    MERCHANT_ID = "SIZNING_PAYME_ID_SHU_YERGA" # Payme Business-dan oling
    
    # Payme linki formati
    params = f"m={MERCHANT_ID};ac.order_id={len(db_orders)};a={clean_amount}"
    encode_params = base64.b64encode(params.encode()).decode()
    pay_url = f"https://checkout.payme.uz/{encode_params}"

    return {"status": "ok", "pay_url": pay_url}

@app.get("/api/admin/orders")
async def get_all_orders():
    return db_orders
