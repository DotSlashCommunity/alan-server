# @author ksdme
# alan tools, does much
from sys import argv
from peewee import *
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

	# fill new question
	question = Question.create(
		question="Who is Alan Turing ?",
		opt_a="Computer Scientist",
		opt_b="Mechanic",
		opt_c="Artificial Intelligence",
		opt_d="Mathematician",
		answer="Mathematician")
