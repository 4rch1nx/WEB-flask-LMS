from data import db_session

from data.users import User

from flask_restful import reqparse, abort


def abort_if_not_found(user, resource_class, resource_id):
    session = db_session.create_session()
    results = session.query(resource_class).filter(User.id == user.id).filter(resource_class.id == resource_id).first()
    if not results:
        abort(404, message=f"Resource {resource_id} not found in your account")


def check_api_key(api_key):
    db_sess = db_session.create_session()
    available_keys = [user.api_key for user in db_sess.query(User).all()]
    if api_key not in available_keys:
        abort(404,
              message=f"""API Key '{api_key}' not found! You can't use API without API key! Log in to your account or register on the website WEBRobotics and check your API Key!""")


def get_user_by_api_key(api_key):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.api_key == api_key).first()
    return user


class ArgumentsParsers:
    questions_arguments_parser = reqparse.RequestParser()
    questions_arguments_parser.add_argument('api_key', required=True, type=str)
    questions_arguments_parser.add_argument('question_id', required=False, type=int)
    questions_arguments_parser.add_argument('theme', required=False, type=str)
    questions_arguments_parser.add_argument('question', required=False, type=str)

    answers_arguments_parser = reqparse.RequestParser()
    answers_arguments_parser.add_argument('api_key', required=True, type=str)
    answers_arguments_parser.add_argument('answer_id', required=False, type=int)

    saved_algorithms_arguments_parser = reqparse.RequestParser()
    saved_algorithms_arguments_parser.add_argument('api_key', required=True, type=str)
    saved_algorithms_arguments_parser.add_argument('algorithm_id', required=False, type=int)
    saved_algorithms_arguments_parser.add_argument('algorithm_name', required=False, type=str)
    saved_algorithms_arguments_parser.add_argument('algorithm', required=False, action='append')

    saved_devices_arguments_parser = reqparse.RequestParser()
    saved_devices_arguments_parser.add_argument('api_key', required=True, type=str)
    saved_devices_arguments_parser.add_argument('device_id', required=False, type=int)
    saved_devices_arguments_parser.add_argument('device_ssid', required=False, type=str)


parsers = ArgumentsParsers()
