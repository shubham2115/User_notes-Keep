from mongoengine import Document, StringField, SequenceField


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    tittle = StringField(max_length=100)
    desc = StringField(max_length=10000)

    def __repr__(self):
        return f"{self.id}- {self.tittle}"

    def to_dict(self):
        dict_itr = {'id': self.id, 'topic': self.topic, 'desc': self.desc, 'tittle': self.tittle}
        return dict_itr

