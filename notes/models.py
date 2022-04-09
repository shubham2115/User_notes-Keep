from mongoengine import Document, StringField, SequenceField, ListField, ReferenceField, PULL,URLField,BooleanField
from labels import models


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    tittle = StringField(max_length=100)
    desc = StringField(max_length=10000)
    url = URLField()
    pin = BooleanField(default=False)
    label = ListField(ReferenceField(models.Label, reverse_delete_rule=PULL))
    is_trash = BooleanField(default=False)

    def __repr__(self):
        return f"{self.id}- {self.tittle}"

    def to_dict(self):
        dict_itr = {'id': self.id, 'topic': self.topic, 'desc': self.desc, 'tittle': self.tittle,'is_pin':self.pin}
        return dict_itr
