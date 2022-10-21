from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.api import get_all_subjects, get_all_assessment_form


def create_markup_from_lst(lst, buttons_per_row=2):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    length = len(lst)
    for i in range(length // buttons_per_row):
        buttons = [KeyboardButton(text=lst[i * buttons_per_row + j]) for j in range(buttons_per_row)]
        markup.row(*buttons)
    additional_buttons = [KeyboardButton(text=lst[i]) for i in range(length - length % buttons_per_row, length)]
    markup.row(*additional_buttons)

    return markup


def get_assessment_forms_markup(chat_id):
    return create_markup_from_lst(get_all_assessment_form(chat_id))


def get_subject_markup(chat_id):
    return create_markup_from_lst(get_all_subjects(chat_id))


