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
        print(body)
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
        try:
            data_ = Users.objects.filter(user_name=user_name).first()
        except Exception as e:
            return {'Error': str(e)}
        if data_.is_super_user:
            dict_all = {}
            data_user = Users.objects()
            for data in data_user:
                note = Notes.objects.filter(user_name=data.user_name)
                list_user = []
                for itr in note:
                    dict_itr = {'id': itr.id, 'topic': itr.topic, 'desc': itr.desc, }
                    list_user.append(dict_itr)
                dict_all[data.user_name] = list_user

            return make_response(dict_all)
        data_ = Notes.objects.filter(user_name=user_name).first()
        for data in data_:
            dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': data.label}
            list_notes.append(dict_)

        return make_response(jsonify(list_notes), 200)