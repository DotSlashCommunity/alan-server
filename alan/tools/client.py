# @author ksdme
# alan tools, does much
from sys import argv
from peewee import *
from random import randint
from alan.db.models import *

# db connection
slash = SqliteDatabase('slash.db')

# various models
Reply = ReplyModel.getModel(slash)
Detail = DetailModel.getModel(slash)
Question = QuestionModel.getModel(slash)

if "--create" in argv:
    slash.connect()
    slash.create_tables([Reply, Detail, Question])

if "--clear" in argv:
	if raw_input("Are you sure [y/n]? ").strip() == "y":
		
		query = Reply.delete()
		query.execute()

		query = Detail.delete()
		query.execute()

		query = Question.delete()
		query.execute()

if "--fill" in argv:

	# fill samples in the database
	reply = Reply.create(roll=925602715)
	replies = reply.replies
	replies[0] = ReplyModel.CORRECT
	replies[5] = ReplyModel.CORRECT
	replies[6] = ReplyModel.WRONG
	reply.save()

	# fill new detail
	detail = Detail.create(
		year=3,
		branch="CSE",
		roll=925602715,
		phone=9911027503,
		name="Kilari Teja",
		email="kilariteja9@gmail.com")

	# fill sample questions
	for _ in xrange(20):
		Question.create(
			question="{}: Why is this Kolaveri Di ?".format(_),
			opt_a="{}".format(_),
			opt_b="{}".format(_+1),
			opt_c="{}".format(_+2),
			opt_d="{}".format(_+3),
			answer="{}".format(_+randint(0, 3)))
