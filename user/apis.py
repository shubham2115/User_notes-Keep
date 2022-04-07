from flask_restful import Resource
from flask import request, make_response, session, json, jsonify, render_template
from user.model import Users
from common.utils import mail_sender, url_short,token_required,get_token



class Error(Exception):
    pass


class PasswordException(Error):
    pass


class Registration(Resource):
    def post(self):
        data_ = Users.objects()
        dataDict = request.get_json()
        username = dataDict['user_name']
        name = dataDict['name']
        email = dataDict['email']
        password1 = dataDict['password1']
        password2 = dataDict['password2']
        if not password2 == password1:
            return make_response(jsonify(message='Password1 and Password2 must be same'), 409)
        session['logged_in'] = False
        data = Users(user_name=username, name=name, email=email, password=password1)
        for itr in data_:
            if itr.user_name == data.user_name:
                return make_response(jsonify(message='UserName Already Taken'), 409)
        for itr in data_:
            if itr.email == data.email:
                return make_response(jsonify(message="Email Already Taken"), 409)
        data.save()
        token = get_token(data.user_name)
        short_token = url_short(token)
        # token_url = r"http://127.0.0.1:80/activate?token=" + f"{short_token}"
        # msg_text = f"Hello! {dataDict['name']} click the link to activate your account {token_url}"
        template = render_template('index.html')
        print("hey")
        mail_sender(email, template)
        return {'message': 'User Added Check your registered mail id to activate account', 'code': 200}


class Login(Resource):
    def post(self):
        dataDict = request.get_json()
        if not session['logged_in']:
            username = dataDict['username']
            password = dataDict['password']
            data_ = Users.objects.filter(user_name=username).first()

            if data_:
                if password == data_.password:
                    session['logged_in'] = True
                    session['user_name'] = data_.user_name
                    token = get_token(dataDict['username'])
                    short_token = url_short(token)
                    return {'message': 'logged_in', 'token': short_token, 'code': 200}
            return {"message": "incorrect password"}


class Activate(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_name, email):
        data = Users.objects.filter(user_name=user_name, email=email).first()
        data.update(is_active=True)

        msg_text = f"Hello! {user_name} Your account is activated"
        mail_sender({email}, msg_text)

        return {'message': 'Your Account is Active.Now you can login', 'code': 200}


class LogOut(Resource):
    def get(self):
        session['logged_in'] = False
        return {'message': 'logged out'}


class ChangePassword(Resource):
    def patch(self):
        if session['logged_in']:
            dataDict = request.get_json()
            user_name = session['user_name']
            new_password = dataDict['new_password']
            data = Users.objects.filter(user_name=user_name).first()
            if data:
                data.update(password=new_password)
                return {'message': 'password changed successfully', 'code': 200}
        else:
            return {"message": "User is not logged in"}
