from flask import jsonify, request

from data import db_session

from data.users import User
from data.questions import Question, Answer
from data.saved_algorithms import Saved_algorithm
from data.devices import Devices

from flask_restful import reqparse, abort, Resource

#from api.base import *


questions_parser_ = reqparse.RequestParser()
questions_parser_.add_argument('apikey', required=True, type=str)

class QuestionsResource(Resource):
    def get(self):
        args = "None"
        try:
            args = questions_parser_.parse_args()
        except BaseException as e:
            args = {"apikey": e.__class__.__name__}
        # check_api_key(args["api_key"])
        # user = get_user_by_api_key(args["api_key"])
        # abort_if_not_found(user, Question, args["question_id"])
        # session = db_session.create_session()
        # question = session.query(Question).filter(Question.user_id == user.id).filter(
        #     Question.id == args["question_id"]).first()
        # return jsonify({'question': question.to_dict(
        #     only=('theme', 'question'))})
        return jsonify({'api_key': args["apikey"]})

    # def delete(self):
    #     args = questions_parser.parse_args()
    #     check_api_key(args["api_key"])
    #     user = get_user_by_api_key(args["api_key"])
    #     abort_if_not_found(user, Question, args["question_id"])
    #     session = db_session.create_session()
    #     question = session.query(Question).filter(Question.user_id == user.id).filter(
    #         Question.id == args["question_id"]).first()
    #     session.delete(question)
    #     session.commit()
    #     return jsonify({'success': 'OK'})


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        questions = session.query(Question).all()
        return jsonify({'questions': [item.to_dict(only=('theme', 'question', 'user.name')) for item in questions]})
