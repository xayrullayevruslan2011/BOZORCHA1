from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Frontend bilan bog'lanish uchun ruxsat berish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Buyurtmalar uchun ma'lumotlar modeli
class Order(BaseModel):
    user_name: str
    phone: str
    product: str
    price: str
    size: str

# Vaqtincha buyurtmalarni saqlash uchun ro'yxat
db_orders = []

@app.get("/")
def read_root():
    return {"status": "Ruslan Market Backend ishlamoqda!", "payme_integration": "active"}

@app.post("/api/orders")
async def create_order(order: Order):
    # 1. Buyurtmani terminalda chiqarish va bazaga qo'shish
    print(f"Yangi buyurtma qabul qilindi: {order.user_name} - {order.product}")
    db_orders.append(order.dict())
    
    # 2. To'lov summasini raqamga aylantirish (masalan: "250 000" -> 250000)
    try:
        clean_price = int(''.join(filter(str.isdigit, order.price)))
    except ValueError:
        clean_price = 0

    # 3. Payme checkout linkini generatsiya qilish
    # DIQQAT: 'ruslan_market' o'rniga o'z kassa nomingizni yozishingiz mumkin
    merchant_id = "ruslan_market" 
    amount_tiyin = clean_price * 100  # Payme summani tiyinda qabul qiladi
    
    # Payme talab qiladigan formatni tayyorlash
    pay_params = f"m={merchant_id};ac.order_id={len(db_orders)};a={amount_tiyin}"
    
    # Base64 formatiga kodlash
    encoded_params = base64.b64encode(pay_params.encode()).decode()
    payme_checkout_url = f"https://checkout.payme.uz/{encoded_params}"

    return {
        "status": "ok",
        "message": "Buyurtma bazaga saqlandi",
        "pay_url": payme_checkout_url
    }

@app.get("/api/admin/orders")
async def get_all_orders():
    # Barcha buyurtmalarni ko'rish uchun (Admin uchun)
    return db_orders
