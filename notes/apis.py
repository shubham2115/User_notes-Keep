import json
from flask_restful import Resource
from flask import request, make_response, session, jsonify
from .utils import token_required
from .models import Notes
from user.model import Users
from middleware import auth


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        print(session['user_name'])
        body['user_name'] = session['user_name']
        notes = Notes(**body)
        notes.save()
        return {'message': 'Notes Added'}


class NotesOperation(Resource):
    method_decorators = {'patch': [auth.login_required], 'delete': [auth.login_required]}

    def patch(self, id):
        try:
            note = Notes.objects(id=id)
        except Exception as e:
            return {'Error': str(e)}
        desc = request.form.get('Description')
        note.update(desc=desc)
        return {'message': 'Notes updated'}

    def delete(self, id):
        try:
            note = Notes.objects(id=id).first()
        except Exception as e:
            return {'Error': str(e)}
        note.delete()
        return {'message': 'Notes Deleted'}


class Home(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_name):
        list_notes = []
        data_ = Users.objects.filter(user_name=user_name)

        dict_all = {}
        data_user = Users.objects()
        for data in data_user:
            note = Notes.objects.filter(user_name=data.user_name)
            print(note)
            list_user = []
            for itr in note:
                dict_itr = itr.to_dict()
                list_user.append(dict_itr)
                dict_all[data.user_name] = list_user

        return make_response(dict_all)
        # data_ = Notes.objects.filter(user_name=user_name).first()
