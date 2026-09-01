import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, ADMIN_IDS
from handlers import router as handlers_router
from admin import router as admin_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(handlers_router)

async def main():
    print("=" * 50)
    print("已启动")
    print(f"管理员: {ADMIN_IDS}")
    print("=" * 50)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
