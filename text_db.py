import db
from helpers import string_time


# print(sql_time["now"]())


# add question
# db.insert("questions", {
#     "question_text": "Today",
#     "day": string_time["today"]()

# })

# get all questions
questions = db.fetchall("users", ['id'])
print(questions)
# get question/s
# data = db.select_by_keys(
#     'questions',
#     ['id', 'question_text', 'day'],
#     {'day': "2021-09-12"}
# )

# print('======================')

# if type(data) is list:
#     for i in data:
#         print(i)
# else:
#     print(data)
