import datetime
import database.api as api
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types


TOKEN = '5584683916:AAHVZF5f2blhrC29InKwW4-FDMPJsiVV_eU'
bot = Bot(token=TOKEN)

button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)

@dp.message_handler(commands='start')
def strt()

print(api.create_deadline(123123123, 6, 6, datetime.datetime(year=2022, month=10, day=23, hour=23, minute=59,
                                                             second=0, microsecond=0, tzinfo=None)))
print(api.create_chat(123123123))
print(api.create_subject(123123123, 'nice'))
print(api.create_assessmentForm(123123123, 'slice'))

print(api.get_all_deadlines(123123123))
print(api.get_all_subjects(123123123))
print(api.get_all_assessmentform(123123123))
