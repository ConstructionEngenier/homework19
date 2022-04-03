from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200

    @admin_required
    def post(self):
        req_json = request.json
        new_director = director_service.create(req_json)
        return f"Созданный id: {new_director.id}", 201

@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        director = director_service.get_one(rid)
        if director:
            return director_schema.dump(director), 200
        return "", 404

    @admin_required
    def put(self, uid: int):
        req_json = request.json
        if not req_json.get('id'):
            req_json['id'] = uid
        if director_service.update(req_json):
            return f"Обновленный id: {uid}", 201
        return "not found", 404

    @admin_required
    def delete(self, uid: int):
        if director_service.delete(uid):
            return "", 204
        return "not found", 404