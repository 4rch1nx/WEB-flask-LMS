from flask import jsonify

from data import db_session

from data.devices import Devices

from flask_restful import Resource

from api.base import *


class SavedDevicesResource(Resource):

    def check_arguments(self, check_resource=True):
        args = parsers.saved_devices_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        if check_resource:
            abort_if_not_found(user, Devices, args["device_id"])
        return args, user

    def get(self):
        args, user = self.check_arguments()
        session = db_session.create_session()
        device = session.query(Devices).filter(Devices.user_id == user.id).filter(Devices.id == args["device_id"]).first()
        return jsonify({'device': device.to_dict(
            only=('name', 'ssid', 'bssid'))})


class SavedDevicesListResource(Resource):
    def get(self):
        args = parsers.saved_devices_arguments_parser.parse_args()
        check_api_key(args["api_key"])
        user = get_user_by_api_key(args["api_key"])
        session = db_session.create_session()
        devices = session.query(Devices).filter(Devices.user_id == user.id).all()
        return jsonify({'saved_devices': [item.to_dict(only=('id', 'name')) for item in devices]})

