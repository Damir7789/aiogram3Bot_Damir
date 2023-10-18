import logging
import asyncio
from time import sleep
# from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile
from random import randint

TELEGRAM_TOKEN = "6263696820:AAGfWdezicdY9eLKp-uM_UjHfqOjht-dIa8"
GROUP_ID = "-1001674247269"

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
    await message.answer("рад тебя видеть,  <b> {0.first_name} </b> !!!".format(message.from_user), parse_mode="html")    

@dp.message(Command("mygroup"))
async def cmd_to_group(message: types.Message, bot: Bot):
    await bot.send_message(GROUP_ID, "Hello from Damir")

# обработка бработка команды рандом
# /rand
@dp.message(Command(commands=["random", "rand", "rnd"]))
async def get_random(message: types.Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split("-")]
    num = randint(a, b)
    await message.reply(f"Случайное число получилось:\t {num}")

# команда заблок
@dp.message(Command(commands=["ban"]))
async def zabanit(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Пиши команду ban в ответ на сообщение")
        return 
    await message.bot.delete_message(chat_id=GROUP_ID, message_id = message.message_id)
    await message.bot.ban_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)

# ping pong
@dp.message()
async def echo(message: types.Message):
    print("message listened")
    # await message.answer("Бот Дамира услышал от, {0.first_name} : " + message.text)

# непреривный режим работы бота
async def main():
    await dp.start_polling(bot)
    # del all undhaled message
    await bot.delete_webhook(drop_pending_updates=True)

# основной цикл
if __name__ == '__main__':
    asyncio.run(main())