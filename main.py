import datetime

import buttons
import database.api as api
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

TOKEN = '5584683916:AAHVZF5f2blhrC29InKwW4-FDMPJsiVV_eU'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Deadline(StatesGroup):
    subject = State()  # Will be represented in storage as 'Form:name'
    assessment_form = State()  # Will be represented in storage as 'Form:age'
    deadline = State()  # Will be represented in storage as 'Form:gender'


button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    api.create_chat(message.chat.id)
    await message.reply('Назови мне предметы по которым ты хочешь не вылететь')


@dp.message_handler(commands='set_sub')
async def subject(message: types.Message):
    arguments = message.get_args()
    # print(str(message)[:200], '\n', str(message)[200:])
    # print(message['text'])
    # print(message['from']["id"])
    # print(arguments)
    if arguments != '':
        api.create_subject(message['from']['id'], arguments)
        await message.reply('Ага, запомнил 👌).')
    else:
        await message.answer('Чо? Введи название предмета после команды /set_sub (одним сообщением)')


@dp.message_handler(commands='set_ass')
async def assessmentform(message: types.Message):
    arguments = message.get_args()
    # print(message['text'])
    # print(arguments)
    if arguments != '':
        api.create_assessment_form(message['from']['id'], arguments)
        await message.reply('Ага, запомнил 👌).')
    else:
        await message.answer('Чо? Введи форму контроля после команды /set_ass (одним сообщением')


@dp.message_handler(commands='!')
async def deadline(message: types.Message):
    await Deadline.subject.set()
    await message.reply('По какому предмету ты хочешь установить дедлайн?',
                        reply_markup=buttons.get_subject_markup(message.chat.id))


@dp.message_handler(state=Deadline.subject)
async def process_name_subj(message: types.Message, state: FSMContext):
    if message.text not in api.get_all_subjects(message.chat.id):
        await state.finish()
        await message.answer(text='Да-да...я кнопки делал. Давай сначала. Введи /!', reply_markup=ReplyKeyboardRemove())
        return
    async with state.proxy() as data:
        data['subject'] = message.text
    await Deadline.next()
    await message.reply("А теперь форма контроля", reply_markup=buttons.get_assessment_forms_markup(message.chat.id))


@dp.message_handler(state=Deadline.assessment_form)
async def process_name_ass(message: types.Message, state: FSMContext):
    if message.text not in api.get_all_assessment_form(message.chat.id):
        await state.finish()
        await message.answer(text='Да-да...я кнопки делал. Давай сначала. Введи /!', reply_markup=ReplyKeyboardRemove())
        return
    async with state.proxy() as data:
        data['assessment_form'] = message.text

    await Deadline.next()
    await message.reply("А теперь введи дату и время дедлайна", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Deadline.deadline)
async def process_name_ass(message: types.Message, state: FSMContext):
    try:
        date_time_obj = datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except:
        await message.reply("Что-то пошло не так, попробуй ещё раз")
    async with state.proxy() as data:
        created = api.create_deadline_by_names(message.chat.id, data["subject"], data["assessment_form"], date_time_obj)
        if created:
            await message.reply(f"Создал дедлайн {data['subject']} {data['assessment_form']} {date_time_obj}")
        else:
            await message.reply("Что-то пошло не так, попробуй ещё раз")
        await state.finish()




@dp.message_handler(commands=['show'])
async def show_deadlines(message: types.Message):
    await message.reply('Ваши дедлайны: \n' + '\n'.join(['   '.join(map(str, i[:3])) + '  ' + i[3] for i in api.get_all_deadlines(message.chat.id)]))

#
# print(api.create_deadline(123123123, 6, 6, datetime.datetime(year=2022, month=10, day=23, hour=23, minute=59,
#                                                              second=0, microsecond=0, tzinfo=None)))
# print(api.create_chat(123123123))
# print(api.create_subject(123123123, 'nice'))
# print(api.create_assessmentForm(123123123, 'slice'))
#
# print(api.get_all_deadlines(123123123))
# print(*api.get_all_subjects(1185028027))
# print(api.get_all_assessmentform(123123123))
# print(api.get_all_chat_id())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
