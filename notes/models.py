from mongoengine import Document, StringField, SequenceField


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    desc = StringField(max_length=1000)
