import logging
import asyncio
from time import sleep
# from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

TELEGRAM_TOKEN = "6263696820:AAGfWdezicdY9eLKp-uM_UjHfqOjht-dIa8"

# вывод отладочних сообщений в терминал
logging.basicConfig(level=logging.INFO)

# cоздали обэкт бот
bot = Bot(token=TELEGRAM_TOKEN)

# создаем обэкт дисплечер
dp = Dispatcher()

# обработка старт
@dp.message(Command("start"))
async def upload_forto(message: types.Message):
    image_from_pc = FSInputFile("sticker.webp")
    await message.answer_photo(image_from_pc, caption="Пообщаемся?)")
    await asyncio.sleep(2)
    await message.answer("рад тебя видеть !!!")    

# ping pong
@dp.message()
async def echo(message: types.Message):
    await message.answer("Бот Дамира услышал: "+message.text)

# непреривный режим работы бота
async def main():
    await dp.start_polling(bot)

# основной цикл
if __name__ == '__main__':
    asyncio.run(main())