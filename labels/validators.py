from .models import Label


def valid_add_label(body):
    label = body.get('label')
    user_name = body.get('user_name')
    lb = Label.objects.filter(user_name=user_name, label=label).first()
    if lb:
        return {'Error': 'Label already exist'}


def valid_delete_label(label):
    lb = Label.objects.filter(label=label).first()
    if not lb:
        return {'Error': 'Label not Exist'}