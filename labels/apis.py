from flask_restful import Resource
from flask import request, json, session
from middleware import auth
from .validators import valid_add_label, valid_delete_label
from .models import Label


class AddLabel(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        """
            This API is used to Addlabel
            @param label_id: user_id from session,
            @return: label will added to note
        """
        req_data = request.data
        body = json.loads(req_data)
        body['user_name'] = session['user_name']
        valid_data = valid_add_label(body)
        if valid_data:
            return valid_data
        lb = Label(**body)
        lb.save()
        return {'message': 'label added'}


class DeleteLabel(Resource):
    method_decorators = {'delete': [auth.login_required]}

    def delete(self, label):
        """
            This API is used to delete label
            @param label_id: label id
            @return: label will delete
           """
        valid_data = valid_delete_label(label)
        user_name = session['user_name']
        if valid_data:
            return valid_data
        lb = Label.objects.filter(user_name=user_name, label=label).first()
        lb.delete()
        return {'message': 'label deleted'}