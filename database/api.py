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
def create_assessmentForm(chat_id, name):
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
def get_all_deadlines(chat_id):
    lst = select(a for a in Deadline if a.linked_chat.chat_id == chat_id and a.deadline_time >= datetime.now())[:]
    return [(ddl.subject.name, ddl.assessment_form.name, ddl.deadline_time)
            for ddl in select(ddl for ddl in Deadline if ddl.linked_chat.chat_id == chat_id)]


@db_session
def get_all_subjects(chat_id):
    return [subj.name for subj in select(subj for subj in Subject if subj.chat_id.chat_id == chat_id)]


@db_session
def get_all_assessmentform(chat_id):
    return [assform.name for assform in select(assform for assform in AssessmentForm if assform.chat_id.chat_id \
                                               == chat_id)]

