# @author ksdme
# server script
from peewee import *
from alan.db.models import *

slash = SqliteDatabase('slash.db')
Reply = ReplyModel.getModel(slash)
Detail = DetailModel.getModel(slash)
Question = QuestionModel.getModel(slash)

if __name__ == "__main__":
    slash.connect()
    slash.create_tables([Reply, Detail, Question])
