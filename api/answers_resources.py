from flask import jsonify

from data import db_session

from data.questions import Answer

from flask_restful import Resource

from api.base import *


class AnswersResource(Resource):

    def check_arguments(self, check_resource=True):
        args = parsers.answers_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        if check_resource:
            abort_if_not_found(user, Answer, args["answer_id"])
        return args, user

    def get(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        answer = session.query(Answer).filter(Answer.user_id == user.id).filter(Answer.id == args["answer_id"]).first()
        return jsonify({'answer': answer.to_dict(
            only=('question_theme', 'question', 'answer', 'question_id'))})


class AnswersListResource(Resource):
    def get(self):
        args = parsers.answers_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        session = db_session.create_session()
        answers = session.query(Answer).filter(Answer.user_id == user.id).all()
        return jsonify({'answers': [item.to_dict(only=('id', 'question', 'answer')) for item in answers]})
