import json
from flask_restful import Resource
from flask import request, make_response, session, jsonify
from .utils import token_required
from .models import Notes
from user.model import Users
from middleware import auth
from labels import models as md
import redis
from common.utils import do_cache

r = redis.Redis(
    host='localhost',
    port=6379
)


class Error(Exception):
    pass


class CustomError(Error):
    pass


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        # req_data = request.data
        # body = json.loads(req_data)
        # body['user_name'] = session['user_name']
        dataDict = request.get_json()
        topic = dataDict['topic']
        tittle = dataDict['tittle']
        desc = dataDict['desc']
        notes = Notes(topic=topic, tittle=tittle, desc=desc)
        notes.save()
        return {'message': 'Notes Added', 'code': 200}


class NotesOperation(Resource):
    method_decorators = {'patch': [auth.login_required], 'delete': [auth.login_required]}

    def patch(self, id):
        try:
            note = Notes.objects(id=id)
            if note.count() > 0:
                desc = request.form.get('Description')
                note.update(desc=desc)
                return {'message': 'Notes updated', 'code': 200}
            else:
                raise CustomError
        except CustomError:
            return {"Message": "id does not Exist"}

    def delete(self, id):
        try:
            note = Notes.objects(id=id).first()
        except Exception as e:
            return {'Error': str(e)}
        note.delete()
        return {'message': 'Notes Deleted', 'code': 200}

    def get(self, id):
        key = f"get_user{id}"
        print(key)
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data
        note = Notes.objects(id=id).first()
        print(note)
        result = {"user_name": note.user_name, "topic": note.topic, "desc": note.desc, "label":
            [lb.label for lb in note.label]}
        do_cache(key, result, 30)
        return jsonify(result)


class Home(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_name):

        key = f"get_user{user_name}"
        print(key)
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data
        list_notes = []
        data_ = Users.objects.filter(user_name=user_name)

        dict_all = {}
        data_user = Users.objects()
        for data in data_user:
            note = Notes.objects.filter(user_name=data.user_name)
            list_user = []
            for itr in note:
                dict_itr = itr.to_dict()
                list_user.append(dict_itr)
                dict_all[data.user_name] = list_user

        do_cache(key, dict_all, 30)
        return make_response(dict_all)


class NoteLabel(Resource):
    method_decorators = {'post': [auth.login_required], 'patch': [auth.login_required], 'delete': [auth.login_required]}

    def post(self, id):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')
        user_name = session['user_name']
        label_data = md.Label.objects.filter(user_name=user_name, label=label).first()
        if not label_data:
            label_data = md.Label(user_name=user_name, label=label)
            label_data.save()
        try:
            note = Notes.objects.filter(user_name=session['user_name'], id=id).first()
            if not note:
                return {'Error': 'Note is not present', 'code': 400}
        except Exception as e:
            return {'Error': str(e)}
        for data in note.label:
            if data.label == label:
                return {'Error': 'label already present in this note', 'code': '400'}
        note.update(push__label=label_data)
        return {'message': 'label added', 'code': '200'}

    def patch(self, id):
        req_data = request.data
        body = json.loads(req_data)
        old_label = body.get('label')
        new_label = body.get('new_label')
        user_name = session['user_name']
        note = Notes.objects.filter(id=id, user_name=user_name).first()
        label2 = md.Label.objects.filter(user_name=user_name, label=new_label).first()
        if not label2:
            label2 = md.Label(user_name=user_name, label=new_label)
            label2.save()
        label_list = note.label
        for i in label_list:
            if i.label == old_label:
                label_list.remove(i)
                label_list.append(label2)
                note.update(label=label_list)
                return {'message': 'label updated'}
            return {'Error': 'Label not present in given note', 'code': '400'}

    def delete(self, id):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')

        note = Notes.objects.filter(id=id, user_name=session['user_name']).first()

        list_label = note.label
        for data in list_label:
            print(data.label)
            if data.label == label:
                print(data.label)
                list_label.remove(data)
                note.update(label=list_label)
                return {'message': 'label removed', 'code': '200'}
        return {'Error': 'label not found in this note', 'code': '400'}


class GetByLabel(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, label):
        list_notes = []
        note = Notes.objects.filter(user_name=session['user_name'])
        for data in note:
            for lb in data.label:
                if lb.label == label:
                    dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc,
                             'label': [lb.label for lb in data.label]}
                    list_notes.append(dict_)
        return {'data': list_notes}


class PinNote(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, id):
        note = Notes.objects.filter(id=id)
        if not note:
            return {'Error': 'Note not found', 'code': 404}
        note.update(pin=True)
        return {'message': 'Note is pinned', 'code': 200}


class NoteAddTrash(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, id):
        note = Notes.objects.filter(id=id)
        if not note:
            return {'Error': 'Note not found', 'code': 404}
        note.update(is_trash=True)
        return {'message': 'Note is moved to trash', 'code': 200}
