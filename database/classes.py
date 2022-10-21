from datetime import datetime

from pony.orm import *

db = Database()


class Chat(db.Entity):
    chat_id = PrimaryKey(int)
    subjects = Set("Subject")
    assessment_forms = Set("AssessmentForm")
    deadline = Set("Deadline")


class Subject(db.Entity):
    subject_id = PrimaryKey(int, auto=True)
    name = Required(str)
    chat_id = Required("Chat")
    deadlines = Set("Deadline")


class AssessmentForm(db.Entity):
    assessment_form_id = PrimaryKey(int, auto=True)
    name = Required(str)
    chat_id = Required("Chat")
    deadlines = Set("Deadline")


class Deadline(db.Entity):
    deadline_id = PrimaryKey(int, auto=True)
    deadline_time = Required(datetime)
    linked_chat = Required("Chat")
    subject = Required("Subject")
    assessment_form = Required("AssessmentForm")
    is_actual = Required(bool)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
