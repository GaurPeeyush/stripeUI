import config
import logging

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label="Subscribe", amount=500 * 100)

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(":")[1] == "TEST":
        await bot.send_message(message.chat.id, "Test Payment!")
    await bot.send_invoice(
        message.chat.id,
        title="Subscribe",
        description="Simple description",
        provider_token=config.PAYMENTS_TOKEN,
        currency="USD",
        photo_url="https://cdn.discordapp.com/attachments/1111003332111241352/1123219793412116520/IMG_20230627_172411_849.jpg",
        photo_width=416,
        photo_size=234,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("Successful Payment:")
    payment_info = message.successful_payment
    for key, value in payment_info.items():
        print(f"{key} = {value}")

    await bot.send_message(
        message.chat.id,
        f"Payment for the amount {message.successful_payment.total_amount // 100} {message.successful_payment.currency} passed successfully!!"
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
