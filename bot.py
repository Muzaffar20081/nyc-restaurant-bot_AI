import os
import asyncio
import logging
import sys

# Настройка логирования для Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Получаем токен из Railway
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    logger.error("❌ ОШИБКА: BOT_TOKEN не найден!")
    logger.info("💡 Добавьте BOT_TOKEN в Railway Variables")
    sys.exit(1)

logger.info(f"✅ Токен получен: {TOKEN[:10]}...")

async def main():
    """Основная функция бота"""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import CommandStart, Command
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Команда /start
    @dp.message(CommandStart())
    async def start_cmd(message: types.Message):
        await message.answer(
            f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
            f"🏪 Добро пожаловать в <b>NYC Restaurant AI</b>!\n\n"
            f"🍔 Бургеры | 🍕 Пицца | 🍣 Суши\n\n"
            f"💬 Напишите /menu чтобы увидеть меню",
            parse_mode="HTML"
        )
    
    # Команда /menu
    @dp.message(Command("menu"))
    async def menu_cmd(message: types.Message):
        menu_text = """
🍽️ <b>МЕНЮ NYC RESTAURANT AI</b>

<b>🍔 БУРГЕРЫ</b>
• Классический - 350₽
• Чизбургер - 400₽
• Бекон - 450₽

<b>🍕 ПИЦЦА</b>
• Маргарита - 550₽
• Пепперони - 600₽
• 4 сыра - 650₽

<b>🍣 СУШИ</b>
• Филадельфия - 450₽
• Калифорния - 480₽
• Сет - 850₽

<b>🥤 НАПИТКИ</b>
• Кола - 150₽
• Сок - 120₽
• Вода - 100₽

💡 <i>Напишите название блюда для заказа</i>
"""
        await message.answer(menu_text, parse_mode="HTML")
    
    # Команда /help
    @dp.message(Command("help"))
    async def help_cmd(message: types.Message):
        help_text = """
🤖 <b>ПОМОЩЬ</b>

<b>Команды:</b>
/start - Начало работы
/menu - Показать меню
/help - Эта справка

<b>Как заказать:</b>
1. Напишите /menu
2. Выберите блюдо
3. Напишите его название
4. Мы свяжемся с вами

<b>Контакты:</b>
📍 NYC, AI Street 123
📞 +1 (212) 555-1234
🕐 10:00-23:00
"""
        await message.answer(help_text, parse_mode="HTML")
    
    # Обработка заказов
    @dp.message()
    async def handle_order(message: types.Message):
        text = message.text.lower()
        
        if "бургер" in text:
            await message.answer("✅ Бургер добавлен в заказ! 🍔")
        elif "пицц" in text:
            await message.answer("✅ Пицца добавлена в заказ! 🍕")
        elif "суши" in text:
            await message.answer("✅ Суши добавлены в заказ! 🍣")
        elif "напиток" in text or "кола" in text or "сок" in text:
            await message.answer("✅ Напиток добавлен в заказ! 🥤")
        else:
            await message.answer("🍽️ Используйте /menu чтобы увидеть меню")
    
    logger.info("🚀 Бот запускается...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("NYC RESTAURANT AI BOT - ЗАПУСК")
    logger.info("=" * 50)
    asyncio.run(main())
