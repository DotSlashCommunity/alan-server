# @author ksdme
# declares models
from peewee import *

# custom json model
class JSONField(TextField):
    
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

# details model wrapper
class DetailModel(object):

    @staticmethod
    def getModel(db):

        class Detail(Model):

            serial = IntegerField(null=False, primary_key=True)
            name = CharField(null=False, max_length=40)
            email = CharField(null=False, max_length=50)
            roll = IntegerField(null=False, unique=True)
            year = IntegerField(null=False, constraints=[Check('year > 0 AND year < 5')])
            branch = CharField(null=False, max_length=3, constraints=[Check('branch IN ("CSE", "ECE", "MAE", "CVE", "EEE")')])
            phone = IntegerField(null=False, unique=True, constraints=[Check('phone >= 7000000000 AND phone <= 9999999999')], index=False)

            class Meta:
                database = db

        # details model
        return Detail

# question model wrapper
class QuestionModel(object):

    @staticmethod
    def getModel(db):

        class Question(Model):

            serial = IntegerField(null=False, primary_key=True)
            question = TextField(null=False)
            opt_a = CharField(null=False, max_length=100)
            opt_b = CharField(null=False, max_length=100)
            opt_c = CharField(null=False, max_length=100)
            opt_d = CharField(null=False, max_length=100)
            answer = CharField(null=False, max_length=100)

            class Meta:
                database = db

        # question model
        return Question

# score model wrapper
class ReplyModel(object):

    CORRECT_ANSWER = 1
    WRONG_ANSWER = 0
    UNANSWERED = -1

    @staticmethod
    def replies_model():
        return dict([(l, ReplyModel.UNANSWERED) for l in xrange(20)])

    @staticmethod
    def getModel(db):

        class Reply(Model):

            roll = IntegerField(null=False, unique=True)
            serial = IntegerField(null=False, primary_key=True)
            replies = JSONField(null=False, default=ReplyModel.replies_model)

            class Meta:
                database = db

        # score model
        return Reply
