# @author ksdme
# alan tools, does much
import os
from sys import argv
from peewee import *
from random import randint
from alan.db.models import *

uri, argv = argv[-1], argv[:-1]
if (not os.path.exists(uri)) or os.path.isdir(uri):
	print "Usage: client.py <commands> <sqlite db url>"
	exit()

# db connection
slash = SqliteDatabase(uri)

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

		if raw_input("[?] Delete Questions: (yes/no)") == "yes":
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

# yet, a new mode to note the presence
if "--mark" in argv:

	while True:

		# ask for the roll and then
		try:
			roll = int(raw_input("[+] Enter Roll: "))
		except:
			print "[-] Failed: {}".format(roll)
			continue

		try:
			guy = Detail.get(Detail.roll == roll)
		except Detail.DoesNotExist:
			print "[-] DB Lookup Failed: {}".format(roll)
			continue

		# print his info
		print "\n[:] Name: {}".format(guy.name)
		print "[:] Roll: {}".format(guy.roll)
		print "[:] Year: {}".format(guy.year)
		print "[:] Branch: {}\n".format(guy.branch)


		flag = raw_input("[+] Mark Present ? (y/n): ")
		if flag == "y" or flag == "Y":
			guy.present = 1
			guy.save()

			print "[+] Marked!\n"
		else:
			print "[+] Moving On...\n"

		flag = raw_input("[==] Mark More ? (y/n): ")
		if flag != "y" and flag != "Y":
			print "[+] Bye ;)"
			break

# dumper
if "--import" in argv:
	import csv

	# the order of the csv file columns
	# keeps headers off btw
	# roll, name, email, phone, year, branch
	file = raw_input("[+] Source CSV: ")
	with open(file, 'rb') as csv_source:
		csv_source = csv.reader(csv_source, delimiter=";")
		for detail in csv_source:

			try:
				Detail.create(
					roll=int(detail[0]),
					name=detail[1],
					email=detail[2],
					phone=int(detail[3]),
					year=int(detail[4]),
					branch=detail[5],
					present=0)

				Reply.create(
					roll=int(detail[0]))
			except Exception as e:
				print "[!] Failed: {}; ".format(detail[0]), e
