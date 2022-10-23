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
    await message.reply('Йоу. Я твой виртуальный староста, а вот инструкция как меня абьюзить: \n\n'
                        'При помощи меня ты можешь:\n\n'
                        '✌️ Использовать /help для быстрого доступа ко всем командам\n\n'
                        '🤌 Создавать новые предметы по которым хочешь установить дедлайн командой /set_sub. \n\n'
                        '       Для того чтобы добавить предмет, тебе надо ввести одним \n'
                        '       сообщением команду /set_sub и название предмета\n'
                        '       (Например: /set_sub Дискра)\n\n'
                        '🤌 Создавать новые формы контроля для этих предметов командой \set_ass.\n'
                        '       Для того    чтобы добавить форму контроля, тебе надо ввести \n'
                        '       одним сообщением команду /set_ass и название формы контроля\n'
                        '       (Например: /set_ass домашка)\n\n'
                        '🤌 Создавать новые дедлайны при помощи команды \!\n'
                        '       Чтобы тебе было просто создавать дедлайны, сначала введи все\n'
                        '       предметы и формы контроля которые у тебя есть, но\n'
                        '       ты cможешь их добавить позже если вдруг что-то забыл.\n\n'
                        '   После того как ты создал предметы и формы контроля, тебе надо:\n'
                        '   -  Ввести команду /!\n'
                        '   -  Выбрать на появившейся клавиатуре нужный тебе предмет\n'
                        '   -  Потом выбрать на появившейся клавиатуре нужную тебе форму \n '
                        '      контроля\n'
                        '   -  Ввести дату и время дедлайна в формате dd.mm.yyyy hh:mm\n'
                        '       (Например: 25.08.2023 23:59)\n\n'
                        '🤌 Смотреть свои актуальные дедлайны при помощи команды /show \n'
                        '       Очень важно, просроченные дедлайны ты увидеть уже\n'
                        '       не сможешь. 👉👈'
                        )

@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.reply('/start   - подробный текст о том как использовать бота \n'
                        '/set_sub - создать новый предмет в клавиатуре\n'
                        '/set_ass - создать новый формат контроля в клавиатуре\n'
                        '/!       - создать новый дедлайн\n'
                        '/show:   - показать все актуальные дедлайны\n'
                        )


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
        await message.answer(text='Да-да...я кнопки зря делал. Давай сначала. Введи /!', reply_markup=ReplyKeyboardRemove())
        return
    async with state.proxy() as data:
        data['subject'] = message.text
    await Deadline.next()
    await message.reply("А теперь форма контроля", reply_markup=buttons.get_assessment_forms_markup(message.chat.id))


@dp.message_handler(state=Deadline.assessment_form)
async def process_name_ass(message: types.Message, state: FSMContext):
    if message.text not in api.get_all_assessment_form(message.chat.id):
        await state.finish()
        await message.answer(text='Да-да...я кнопки зря делал. Давай сначала. Введи /!', reply_markup=ReplyKeyboardRemove())
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
