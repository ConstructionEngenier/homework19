from flask import request, abort
from flask_restx import Resource, Namespace

from service.auth import login_user, refresh_user_token

auth_ns = Namespace('auth')

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        if not request.json:
            abort(400, "Bad Request")
        tokens = login_user(request.json)
        if tokens:
            return tokens, 200
        abort(401, "Authorization Error")

    def put(self):
        if not request.json:
            abort(400, "Bad Request")
        tokens = refresh_user_token(request.json)
        if tokens:
            return tokens, 200
        abort(401, "Authorization Error")