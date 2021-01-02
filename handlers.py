from pprint import pprint
from main import bot, dp
from aiogram.types import Message, ChatActions, ContentType
import aiogram.types as types 
from config import admin_id
from aiogram.dispatcher.filters import Command, Text
import re
import datetime
import pytz
import db

def list_to_dict(user_list):
        user_list = list(user_list[0][0:])
        for i in range(len(user_list)):
            if user_list[i] == None:
                user_list[i] = ""
        return {
                "user_id": user_list[0],
                "first_name": user_list[1],
                "username": user_list[2],
                "chat_id": user_list[3],
                "time_add_chat": user_list[4]
            }

                
def check_user(user_id, first_name, username, chat_id):
    chuser = db.row("users", {"user_id = ": str(user_id)})
    print(chuser)
    if chuser == None:
        tz = pytz.timezone("Europe/Moscow")
        now = datetime.datetime.now(tz).strftime('%d.%m.%Y.%H:%M')
        print(str(now))
        user = {"user_id": str(user_id),
                "first_name": first_name,
                "username": username,
                "chat_id": str(chat_id),
                "time_add_chat": str(now)
                }
        db.insert("users", user)
        print("add")
    else:
        user = list_to_dict(chuser)
    print("user")
    pprint(user)
    
    return user

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")

@dp.message_handler(content_types=["new_chat_members"])
async def send_welcome(message: Message):
    me = await bot.get_me()
    botme = await bot.get_chat_member(message.chat.id, me.id)
    if botme.status == "administrator" and botme.can_delete_messages == True and botme.can_restrict_members == True:
        for user in message.new_chat_members:
            if me.id != user.id:
                username = ""
                try:
                    username == user.username
                except:
                    pass
                user = check_user(user.id, user.first_name, username, message.chat.id)
                print(user["chat_id"] != str(message.chat.id))
                if user["chat_id"] != str(message.chat.id):
                    answer = await bot.restrict_chat_member(message.chat.id, user["user_id"])
                    await message.reply("Вы отправлены в мьют из-за нарушений правил чата")
    else:
        await message.reply("Что бы я смог работать мне надо выдать разрешения.")
    print(message)
    # await message.reply("new user")

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    me = await bot.get_me()
    print(me)
    botme = await bot.get_chat_member(message.chat.id, me.id)
    print(botme)
    print(message)
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
