import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, MENU

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 FOOD BOT STARTING...")
print(f"🤖 Token: {BOT_TOKEN[:15]}...")
print("=" * 50)

# Хранилище корзин
user_carts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🍔 Бургеры", callback_data='burgers')],
        [InlineKeyboardButton("🍕 Пицца", callback_data='pizza')],
        [InlineKeyboardButton("🍣 Суши", callback_data='sushi')],
        [InlineKeyboardButton("🛒 Корзина", callback_data='cart')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')]
    ]
    
    await update.message.reply_text(
        f"🍽️ Привет, {user.first_name}!\nВыберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if user_id not in user_carts:
        user_carts[user_id] = {}
    
    if data == 'cart':
        await show_cart(query, user_id)
    elif data == 'help':
        await show_help(query)
    elif data == 'back':
        await show_main_menu(query)
    elif data in ['burgers', 'pizza', 'sushi']:
        await show_category(query, data)
    elif data.startswith('add_'):
        item = data[4:]
        await add_to_cart(query, user_id, item)

async def show_cart(query, user_id):
    """Показать корзину"""
    cart = user_carts[user_id]
    
    if not cart:
        text = "🛒 Корзина пуста"
    else:
        text = "🛒 Ваша корзина:\n\n"
        total = 0
        
        for item, qty in cart.items():
            price = 0
            for category in MENU.values():
                if item in category:
                    price = category[item]
                    break
            
            item_total = price * qty
            total += item_total
            text += f"• {item} ×{qty} = {item_total}₽\n"
        
        text += f"\n💵 Итого: {total}₽"
    
    keyboard = [
        [InlineKeyboardButton("✅ Оформить", callback_data='order')],
        [InlineKeyboardButton("⬅️ Меню", callback_data='back')]
    ]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_category(query, category):
    """Показать категорию"""
    items = MENU[category]
    
    keyboard = []
    for name, price in items.items():
        keyboard.append([
            InlineKeyboardButton(f"{name} - {price}₽", callback_data=f"add_{name}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад", callback_data='back'),
        InlineKeyboardButton("🛒 Корзина", callback_data='cart')
    ])
    
    await query.edit_message_text(
        "Выберите блюдо:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def add_to_cart(query, user_id, item):
    """Добавить в корзину"""
    cart = user_carts[user_id]
    
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1
    
    price = 0
    for category in MENU.values():
        if item in category:
            price = category[item]
            break
    
    total_items = sum(cart.values())
    
    await query.edit_message_text(
        f"✅ {item} добавлен!\n"
        f"💰 Цена: {price}₽\n"
        f"🛒 В корзине: {total_items} шт\n\n"
        "Продолжайте:"
    )

async def show_help(query):
    """Показать помощь"""
    text = "🤖 Помощь: /start - начать заказ"
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_main_menu(query):
    """Показать главное меню"""
    keyboard = [
        [InlineKeyboardButton("🍔 Бургеры", callback_data='burgers')],
        [InlineKeyboardButton("🍕 Пицца", callback_data='pizza')],
        [InlineKeyboardButton("🍣 Суши", callback_data='sushi')],
        [InlineKeyboardButton("🛒 Корзина", callback_data='cart')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')]
    ]
    await query.edit_message_text("Выберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте /start для начала заказа!")

def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()