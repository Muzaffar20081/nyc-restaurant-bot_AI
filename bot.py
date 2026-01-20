import os
import asyncio
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ BOT_TOKEN не найден!")
    sys.exit(1)

async def main():
    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart
    from aiogram.types import Message
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(f"👋 Привет, {message.from_user.first_name}!\nЯ работаю! 🚀")
    
    @dp.message()
    async def echo(message: Message):
        await message.answer(f"Вы: {message.text}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
