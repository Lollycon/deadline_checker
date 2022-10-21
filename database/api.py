from aiogram.types import InlineKeyboardMarkup

import buttons
from database.classes import *


@db_session
def does_chat_exist(chat_id):
    chat_check = select(ch for ch in Chat if ch.chat_id == chat_id).first()
    return chat_check is not None


@db_session
def create_chat(chat_id):
    if does_chat_exist(chat_id):
        return None
    else:
        chat = Chat(chat_id=chat_id)
        commit()
    return True


@db_session
def create_subject(chat_id, name):
    subject_id = Subject(chat_id=chat_id, name=name)
    commit()
    return True


@db_session
def create_assessment_form(chat_id, name):
    assessment_form_id = AssessmentForm(chat_id=chat_id, name=name)
    commit()
    return True


@db_session
def create_deadline(linked_chat, subject, assessment_form, deadline_time):
    deadline_id = Deadline(linked_chat=linked_chat, subject=subject, assessment_form=assessment_form,
                           deadline_time=deadline_time, is_actual=True)
    commit()
    return True


@db_session
def create_deadline_by_names(chat_id, subject_name, assessment_form_name, deadline_time):
    subject = select(subject for subject in Subject if
                     subject.name == subject_name and subject.chat_id.chat_id == chat_id).first()
    assessment_form = select(
        assessment_form for assessment_form in AssessmentForm if
        assessment_form.name == assessment_form_name and assessment_form.chat_id.chat_id == chat_id).first()
    if subject is None or assessment_form is None:
        return False
    return create_deadline(chat_id, subject, assessment_form, deadline_time)

@db_session
def get_all_deadlines(chat_id):
    lst = select(a for a in Deadline if a.linked_chat.chat_id == chat_id and a.deadline_time >= datetime.now())[:]
    return sorted([(ddl.subject.name, ddl.assessment_form.name, ddl.deadline_time.date(), str(ddl.deadline_time.hour).zfill(2) + ':' + str(ddl.deadline_time.minute).zfill(2))
            for ddl in select(ddl for ddl in Deadline if ddl.linked_chat.chat_id == chat_id)], key= lambda x: x[2])


@db_session
def get_all_subjects(chat_id):
    return [subj.name for subj in select(subj for subj in Subject if subj.chat_id.chat_id == chat_id)]


@db_session
def get_all_assessment_form(chat_id):
    return [assform.name for assform in select(assform for assform in AssessmentForm if assform.chat_id.chat_id \
                                               == chat_id)]




@db_session
def get_all_chat_id():
    return [ch for ch in select(ch for ch in Chat)]

# @db_session
# def kick_subject(chat_id, subject_id):
#     Subject.subject_id =
#     return [subj.name for subj in select(subj for subj in Subject if subj.chat_id.chat_id == chat_id)]
