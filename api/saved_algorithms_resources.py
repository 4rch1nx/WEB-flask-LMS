from flask import jsonify

from data import db_session

from data.saved_algorithms import Saved_algorithm

from flask_restful import Resource, abort

from api.base import *

from Other.code_reader import *


def check_algorithm(algorithm_list):
    algorithm = ','.join(algorithm_list)
    error = find_errors_in_code(algorithm)
    if error is not None:
        return abort(400,
                     message=f"Error in transmitted algorithm: '{error}'! You can view the structure of a "
                             f"correctly transmitted algorithm and the rules of writing algorithm on the WEB Robotics "
                             f"website.")
    return algorithm


def check_algorithm_name(user, algorithm_name):
    session = db_session.create_session()
    algorithm = session.query(Saved_algorithm).filter(Saved_algorithm.user_id == user.id).filter(
        Saved_algorithm.name == algorithm_name).first()
    if algorithm:
        abort(400, message=f"Transmitted algorithm name had already been used in your account! Change "
                           f"the algorithm name or use HTTP-method PUT to change existing algorithm!")


class SavedAlgorithmsResource(Resource):

    def check_arguments(self, check_resource=True):
        args = parsers.saved_algorithms_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        if check_resource:
            abort_if_not_found(user, Saved_algorithm, args["algorithm_id"])
        return args, user

    def get(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        algorithm = session.query(Saved_algorithm).filter(Saved_algorithm.user_id == user.id).filter(
            Saved_algorithm.id == args["algorithm_id"]).first()
        return jsonify({'algorithm': algorithm.to_dict(only=('name', 'algorithm', 'saving_DateTime'))})

    def delete(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        algorithm = session.query(Saved_algorithm).filter(Saved_algorithm.user_id == user.id).filter(
            Saved_algorithm.id == args["algorithm_id"]).first()
        deleted_algorithm = algorithm.algorithm
        deleted_algorithm_name = algorithm.name
        session.delete(algorithm)
        session.commit()
        return jsonify(
            {'success': 'OK', 'deleted_algorithm_name': deleted_algorithm_name, 'deleted_algorithm': deleted_algorithm})

    def post(self):
        args, user = self.check_arguments(check_resource=False)
        session = db_session.create_session()
        algorithm = check_algorithm(args["algorithm"])
        check_algorithm_name(user, args["algorithm_name"])
        algorithm = Saved_algorithm(
            name=args["algorithm_name"],
            algorithm=algorithm,
            user_id=user.id
        )
        user.saved_algorithms.append(algorithm)
        session.merge(user)
        session.commit()
        return jsonify({'success': 'OK', "name": algorithm.name, 'algorithm': algorithm.algorithm})

    def put(self):
        args, user = self.check_arguments(check_resource=False)
        session = db_session.create_session()
        saved_algorithm = session.query(Saved_algorithm).filter(Saved_algorithm.id == args["algorithm_id"]).first()
        new_algorithm = check_algorithm(args["algorithm"])
        saved_algorithm.name = args["algorithm_name"]
        saved_algorithm.algorithm = new_algorithm
        session.commit()
        return jsonify({"success": "OK",
                        "algorithm_name": saved_algorithm.name,
                        "algorithm": saved_algorithm.algorithm,
                        "id": args["algorithm_id"]})


class SavedAlgorithmsListResource(Resource):
    def get(self):
        args = parsers.saved_algorithms_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        session = db_session.create_session()
        algorithms = session.query(Saved_algorithm).filter(Saved_algorithm.user_id == user.id).all()
        return jsonify({'saved_algorithms': [item.to_dict(only=('id', 'name', 'algorithm')) for item in algorithms]})
