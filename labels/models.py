from mongoengine import Document, StringField, SequenceField


class Label(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    label = StringField(max_length=50)