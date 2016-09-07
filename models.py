from connectdatabase import ConnectDatabase
from peewee import *


class UserStory(Model):
    story_title = CharField()
    user_story = CharField()
    acceptance_crit = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
