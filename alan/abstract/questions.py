# @author ksdme
# abstracts methods on question model
from random import shuffle
from alan.db.models import ReplyModel

def getQuestion(qno, qmodel):
	"""
		read a question from the
		given qmodel 
	"""

	try:
		return qmodel.get(qmodel.id == qno)
	except qmodel.DoesNotExist:
		return None

def getOffset(using, cycle=20):
	"""
		calculates the offset using
		a number 'using' subject
	"""

	val = int(using)
	val *= int(str(val)[0])
	while val > cycle:
		using = map(int, str(val))
		val = sum(using)

	return val

def getOffsettedQuestion(roll, qno, qmodel, cycle=20):
	"""
		calculates the question that
		corrosponds to the databse
		entry
	"""

	# ensure the qno is in range
	if qno > cycle or qno < 1:
		return None

	return getQuestion(
		(((getOffset(roll, cycle) + qno)%cycle) + 1), qmodel)


def shuffledAnswers(question):
	"""
		simply shuffles the ans
		and returns the list
	"""

	answers = [
		question.opt_a,
		question.opt_b,
		question.opt_c,
		question.opt_d
	]

	shuffle(answers)
	return answers

def getQuestionStatus(roll, qno, rmodel, cycle=20):
	"""
		this here lets you know the current
		status of the question, i.e it has
		been answered or is editable etc,

		!!!you don't need offsetted qno!!!
	"""

	# ensure qno
	if qno > cycle or qno < 1:
		return None

	try:
		reply = rmodel.get(rmodel.roll == roll)
		return reply.replies[qno]
	except rmodel.DoesNotExist:
		return None

def isEditableQuestion(roll, qno, rmodel, cycle=20):
	"""
		check if the question is editable,
		i.e returns true if it was unanswered
	"""

	status = getQuestionStatus(roll, qno, rmodel, cycle)

	# ignore errors
	if status is None:
		return False

	# if it still is unanswered
	if status == ReplyModel.UNANSWERED:
		return True

	return False

def verifyAnswer(question, answer):
	"""
		requires a question instance and
		the submitted answer, validates it
	"""

	return question.answer == answer

def getPresentableQuestion(roll, qno, qmodel, rmodel, cycle=20):
	"""
		completely abstracts away the
		question selection and forming
		process, questions and options
	"""

	question = getOffsettedQuestion(
		roll, qno, qmodel, cycle)

	# ensure max
	if question is None:
		return { "e": True }

	return {
	    "q": question.question,
	    "o": shuffledAnswers(question)
	    "l": not isEditableQuestion(roll, qno, rmodel, cycle)
	}

def getPresentableSubmission(roll, qno, answer, qmodel, rmodel, cycle=20):
	"""
		validates and lets you know if
		the submitted answer was right
	"""

	# non-offset qno, now do it only if it is an editable one
	if not isEditableQuestion(roll, qno, rmodel, cycle):
		return { "e": True, "m": "l" }

	question = getOffsettedQuestion(
		roll, qno, qmodel, cycle)

	# if bad question no
	if question is None:
		return { "e": True }

	# verify the answer and do recording
	if verifyAnswer(question, answer):
		pass	

	# let the guy know we
	# didn't get any error
	return { "e": False }
