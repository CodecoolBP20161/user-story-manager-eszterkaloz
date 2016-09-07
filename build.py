from models import *
from connectdatabase import ConnectDatabase


def create_table():
    ConnectDatabase.db.connect()
    # ConnectDatabase.db.drop_tables([UserStory], safe=True)
    ConnectDatabase.db.create_tables([UserStory], safe=True)
