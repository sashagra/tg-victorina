from questions import Question, get_question_by_id
import json

with open('questions.json') as f:
    questions = json.load(f)

for q in questions:
    question = Question(q["question"], q["day"], q["answers"])
    question.add()

# print(get_question_by_id(2))
