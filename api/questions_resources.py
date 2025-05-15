from flask import jsonify

from data import db_session

from data.questions import Question, Answer

from flask_restful import Resource

from api.base import *


class QuestionsResource(Resource):

    def check_arguments(self, check_resource=True):
        args = parsers.questions_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        if check_resource:
            abort_if_not_found(user, Question, args["question_id"])
        return args, user

    def get(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        question = session.query(Question).filter(Question.user_id == user.id).filter(
            Question.id == args["question_id"]).first()
        json_answer = {'question': question.to_dict(only=('theme', 'question', 'is_answered'))}
        answer = session.query(Answer).filter(Answer.question_id == question.id).first()
        if answer:
            json_answer["answer"] = {'answer': answer.answer, "answer_id": answer.id}
        else:
            json_answer["answer"] = {'answer': None, "answer_id": None}
        return jsonify(json_answer)

    def delete(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        question = session.query(Question).filter(Question.user_id == user.id).filter(
            Question.id == args["question_id"]).first()
        deleted_question = question.question
        deleted_question_theme = question.theme
        session.delete(question)
        session.commit()
        return jsonify({'success': 'OK', 'deleted_question_theme': deleted_question_theme, 'deleted_question': deleted_question})

    def post(self):
        args, user = self.check_arguments(check_resource=False)
        session = db_session.create_session()
        question = Question(
            theme=args["theme"],
            question=args["question"]
        )
        user.questions.append(question)
        session.merge(user)
        session.commit()
        return jsonify({'success': 'OK', 'theme': question.theme, "question": question.question})

    def put(self):
        args, user = self.check_arguments(check_resource=False)
        session = db_session.create_session()
        question = session.query(Question).filter(Question.id == args["question_id"]).first()
        question.theme = args["theme"]
        question.question = args["question"]
        session.commit()
        return jsonify({"success": "OK",
                        "theme": question.theme,
                        "question": question.question,
                        "id": args["question_id"]})


class QuestionsListResource(Resource):
    def get(self):
        args = parsers.questions_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        session = db_session.create_session()
        questions = session.query(Question).filter(Question.user_id == user.id).all()
        return jsonify({'questions': [item.to_dict(only=('id', 'theme', 'question')) for item in questions]})
