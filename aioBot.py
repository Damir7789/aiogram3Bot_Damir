import logging
import asyncio
import datetime
from time import sleep
# from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile
from random import randint
from aiogram.types import ChatPermissions

TELEGRAM_TOKEN = "6263696820:AAGfWdezicdY9eLKp-uM_UjHfqOjht-dIa8"

# test grp
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
    await bot.send_message(message.chat.id, "Hello from Damir")

# обработка бработка команды рандом
# /rand
@dp.message(Command(commands=["random", "rand", "rnd"]))
async def get_random(message: types.Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split("-")]
    num = randint(a, b)
    await message.reply(f"Случайное число получилось:\t {num}")

# команда бан    
@dp.message(Command(commands=["ban"]))
async def zabanit(message: types.Message):
    # user_status = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    user_status = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id) 
    if isinstance(user_status, types.chat_member_owner.ChatMemberOwner) or isinstance(user_status, types.chat_member_administrator.ChatMemberAdministrator):
        print ("\n\n Owner not Admin - TRUE \n\n")
    else:
        print ("\n\n not Owner not Admin\n\n")
        await message.reply(f"{message.from_user.first_name}, Ты не админ")
        return 
    
    if not message.reply_to_message:
        await message.reply("Пиши команду ban в ответ на сообщение")
        return 
    banned_user = message.reply_to_message.from_user.first_name
    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.reply_to_message.reply(f'Пользователь {banned_user} забанен')

# mute 
@dp.message(Command(commands=["mute"]))
async def mute(message: types.Message, command: CommandObject, bot:Bot):
    userADMIN = message.from_user.first_name
    userID = message.reply_to_message.from_user.id
    userNAME = message.reply_to_message.from_user.first_name
    # kak_dolgo = 3
    # разбываем аргументи на long и kak dolgo
    long, kak_dolgo = [n for n in command.args.split("-")]
    kak_dolgo = int(kak_dolgo)
    vremya = datetime.timedelta(hours = kak_dolgo)
    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=userID, permissions=ChatPermissions(can_send_messages=False), until_date=vremya)
    await message.reply(f"{userADMIN} замутил {userNAME} на {kak_dolgo} часа !!!!!")
    
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