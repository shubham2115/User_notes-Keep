from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField,SequenceField
import datetime


class Users(Document):
    user_id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    name = StringField(max_length=50)
    email = EmailField()
    password = StringField()
    is_active = BooleanField(default=False)
    is_super_user = BooleanField(default=False)
    dt_created = DateTimeField(default=datetime.datetime.now)


    def to_dict(self):
        user_dict = {
            'user_id':self.user_id,
            'user_name': self.user_name,
            'name': self.name,
            'email': self.email,
            'dt_created': self.dt_created
        }
        return user_dict
