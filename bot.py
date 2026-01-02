"""
Ruslam|Market Bot
Asosiy bot fayli - barcha handlerlarni birlashtiradi
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db

# Handlerlarni import qilish
from handlers import user, products, cart, admin

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Botni ishga tushirish"""
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Ma'lumotlar bazasini ishga tushirish
    logger.info("Ma'lumotlar bazasi ishga tushirilmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")
    
    # Routerlarni qo'shish
    dp.include_router(user.router)
    dp.include_router(products.router)
    dp.include_router(cart.router)
    dp.include_router(admin.router)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushirilmoqda...")
    
    try:
        # Eski webhook-larni o'chirish
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Polling rejimida ishga tushirish
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
