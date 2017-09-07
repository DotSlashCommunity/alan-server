# @author ksdme
# declares models
import json
from peewee import *
from playhouse.sqlite_ext import JSONField

# details model wrapper
class DetailModel(object):

    @staticmethod
    def getModel(db):

        class Detail(Model):

            name = CharField(null=False, max_length=40)
            email = CharField(null=False, max_length=50)
            roll = IntegerField(null=False, unique=True)
            year = IntegerField(null=False, constraints=[Check('year > 0 AND year < 5')])
            branch = CharField(null=False, max_length=3, constraints=[Check('branch IN ("CSE", "ECE", "MAE", "CVE", "EEE")')])
            phone = IntegerField(null=False, unique=True, constraints=[Check('phone >= 7000000000 AND phone <= 9999999999')], index=False)
            present = BooleanField(null=False, default=False)

            class Meta:
                database = db

        # details model
        return Detail

# question model wrapper
class QuestionModel(object):

    @staticmethod
    def getModel(db):

        class Question(Model):

            question = TextField(null=False)
            opt_a = CharField(null=False, max_length=100)
            opt_b = CharField(null=False, max_length=100)
            opt_c = CharField(null=False, max_length=100)
            opt_d = CharField(null=False, max_length=100)
            answer = CharField(null=False, max_length=100, constraints=[Check('answer IN (opt_a, opt_b, opt_c, opt_d)')])

            class Meta:
                database = db

        # question model
        return Question

# score model wrapper
class ReplyModel(object):
    
    UNANSWERED = -1
    CORRECT = 1
    WRONG = 0

    @staticmethod
    def replies_model():
        return dict([(l, ReplyModel.UNANSWERED) for l in xrange(20)])

    @staticmethod
    def getModel(db):

        class Reply(Model):

            roll = IntegerField(null=False, unique=True)
            replies = JSONField(null=False, default=ReplyModel.replies_model)

            class Meta:
                database = db

        # score model
        return Reply
