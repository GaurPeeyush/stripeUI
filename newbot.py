import config
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    try:
        if config.PAYMENTS_TOKEN.split(":")[1] == "TEST":
            await bot.send_message(message.chat.id, "Test Payment!")

        buttons = [
            types.InlineKeyboardButton("Monthly Subscription", callback_data="monthly"),
            types.InlineKeyboardButton("Yearly Subscription", callback_data="yearly"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await bot.send_photo(
            message.chat.id,
            photo="https://cdn.discordapp.com/attachments/1111003332111241352/1123219793412116520/IMG_20230627_172411_849.jpg",
            caption="Choose a subscription option:",
            reply_markup=keyboard,
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await bot.send_message(message.chat.id, "An error occurred while processing your request. Please try again.")

@dp.callback_query_handler(lambda query: query.data in ["monthly", "yearly"])
async def process_subscription(callback_query: types.CallbackQuery):
    try:
        subscription_type = callback_query.data

        if subscription_type == "monthly":
            price = types.LabeledPrice(label="Monthly Subscription", amount=8 * 100)
            start_parameter = "monthly-subscription"
        elif subscription_type == "yearly":
            price = types.LabeledPrice(label="Yearly Subscription", amount=49 * 100)
            start_parameter = "yearly-subscription"

        await bot.send_invoice(
            callback_query.from_user.id,
            title=price.label,
            description="Simple description",
            provider_token=config.PAYMENTS_TOKEN,
            currency="USD",
            photo_url="https://cdn.discordapp.com/attachments/1111003332111241352/1123219793412116520/IMG_20230627_172411_849.jpg",
            photo_width=416,
            photo_height=234,
            is_flexible=False,
            prices=[price],
            start_parameter=start_parameter,
            payload="test-invoice-payload"
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await bot.send_message(callback_query.from_user.id, "An error occurred while processing your payment. Please try again.")

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=True,
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await bot.send_message(pre_checkout_query.from_user.id, "An error occurred while processing your payment. Please try again.")

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    try:
        print("Successful Payment:")
        payment_info = message.successful_payment
        print(f"Chat ID: {message.chat.id}")
        print(f"Amount Paid: {payment_info.total_amount // 100}")
        print(f"Type of Subscription: {payment_info.invoice_payload}")
        print(f"Transaction ID: {payment_info.provider_payment_charge_id}")
        print(f"Date and Time of Payment: {datetime.now()}")
        print("Payment Status: Successful")

        await bot.send_message(
            message.chat.id,
            f"Payment received! You have purchased the {payment_info.invoice_payload}.",
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await bot.send_message(message.chat.id, "An error occurred while processing your payment. Please try again.")

if __name__ == "__main__":
    executor.start_polling(dp)
