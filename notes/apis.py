import json
from flask_restful import Resource
from flask import request, make_response, session, jsonify

from common import logger, swagger
from common.utils import token_required, set_cache
from .models import Notes
from user.model import Users
from middleware import auth
from labels import models as md
import redis
from common.exception import NotExist, EmptyError

r = redis.Redis(
    host='localhost',
    port=6379
)


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        dataDict = request.get_json()
        user_name = session['user_name']
        topic = dataDict['topic']
        tittle = dataDict['tittle']
        desc = dataDict['desc']
        try:
            if not topic:
                raise EmptyError("topic should not be empty", 404)
            notes = Notes(user_name=user_name, topic=topic, tittle=tittle, desc=desc)
            if notes:
                notes.save()
                logger.logging.info('note created')
                return {'message': 'Notes Added', 'code': 200}
        except EmptyError as e:
            return e.__dict__


class NotesOperation(Resource):
    method_decorators = {'patch': [auth.login_required], 'delete': [auth.login_required]}

    def patch(self, id):
        try:
            note = Notes.objects(id=id)
            if note:
                desc = request.form.get('Description')
                note.update(desc=desc)
                logger.logging.info('Notes updated')
                return {'message': 'Notes updated', 'code': 200}
            raise NotExist("Note not exist", 400)
        except NotExist as exception:
            logger.logging.info("Id not Exist Error occur")
            return {"Error": exception.Error, 'code': exception.code}

    def delete(self, id):
        try:
            note = Notes.objects(id=id).first()
            if not note:
                raise NotExist("Note not exist", 400)
            note.delete()
            return {'message': 'Notes Deleted', 'code': 200}
        except NotExist as e:
            return e.__dict__

    def get(self, id):
        if session['logged_in']:
            key = f"get_user{id}"
            value = r.get(key)
            if value:
                data = json.loads(value)
                return data
            note = Notes.objects(id=id).first()
            try:
                if not note:
                    raise NotExist("Note not Exist", 404)
                if note:
                    result = {"user_name": note.user_name, "topic": note.topic, "desc": note.desc, "label":
                        [lb.label for lb in note.label]}
                    set_cache(key, result, 30)
                    return jsonify(result)
            except NotExist as e:
                return e.__dict__


class Home(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_name):

        key = f"get_user{user_name}"
        print(key)
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data

        dict_all = {}
        data_user = Users.objects()
        for data in data_user:
            list_user = []
            pin_note = Notes.objects.filter(pin=True, is_trash=False)
            for note in pin_note:
                dict_itr = note.to_dict()
                list_user.append(dict_itr)
                dict_all[data.user_name] = list_user
            unpinned_note = Notes.objects.filter(pin=False, is_trash=False)
            for note in unpinned_note:
                dict_itr = note.to_dict()
                list_user.append(dict_itr)
                dict_all[data.user_name] = list_user
        set_cache(key, dict_all, 30)
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
                raise NotExist('Note is not present', 400)
        except Exception as e:
            return e.__dict__
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
                    dict_ = {'user_name': data.user_name, 'id': data.id, 'topic': data.topic, 'desc': data.desc,
                             'label': [lb.label for lb in data.label]}
                    list_notes.append(dict_)
        return {'Note': list_notes}


class PinNote(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, id):
        note = Notes.objects.filter(id=id)
        try:
            if not note:
                raise NotExist("Note is not present", 404)
            note.update(pin=True)
            return {'message': 'Note is pinned', 'code': 200}
        except Exception as e:
            return e.__dict__


class GetPinNote(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self):
        dict_all = {}
        data_user = Users.objects()
        for data in data_user:
            note = Notes.objects.filter(user_name=data.user_name)
            list_user = []
            if note.pin:
                for itr in note:
                    dict_itr = itr.to_dict()
                    list_user.append(dict_itr)
                    dict_all[data.user_name] = list_user
                if not note.pin:
                    for itr in note:
                        dict_itr = itr.to_dict()
                        list_user.append(dict_itr)
                        dict_all[data.user_name] = list_user
        return make_response(dict_all)


class NoteAddTrash(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, id):
        note = Notes.objects.filter(id=id)
        try:
            if not note:
                raise NotExist("Note is not present", 404)
            note.update(is_trash=True)
            return {'message': 'Note is moved to trash', 'code': 200}
        except Exception as e:
            return e.__dict__
