# @author ksdme
# holds the methods to administer
# the quiz, for eg: timing, login blocking etc
from time import time

# Global Handler
ADMIN_KEY = "CHANGETHEWORLD"

TIMER_STARTED_AT = -1
QUIZ_PLAYABLE_FLAG = False
USER_LOGABLE_STATE = True
QUIZ_ENDED_FLAG = False

def startTimer(pwd):
	"""
		starts the timer of the
		quiz, nothing happens if
		the time actually crosses
	"""

	if pwd != ADMIN_KEY:
		return { "e": True, "m": "w" }

	# start the timer, I mean
	# hold the timer, ironic, huh
	TIMER_STARTED_AT = int(time())
	return { "e": False, "m": TIMER_STARTED_AT }

def getTimer():

	return { "e": False, "m": TIMER_STARTED_AT }

def setQuizState(pwd, state):
	"""
		sets the quiz state,
		i.e if it is playable etc
	"""
	global QUIZ_PLAYABLE_FLAG

	if pwd != ADMIN_KEY:
		return { "e": True, "m": "w" }

	# set the state here, State is bool
	QUIZ_PLAYABLE_FLAG = state > 0
	return { "e": False, "m": QUIZ_PLAYABLE_FLAG }

def getQuizState():
	"""
		simply gets the current
		quiz state
	"""

	return QUIZ_PLAYABLE_FLAG

def setLoginState(pwd, state):
	"""
		again, like quiz state
		this represents the state
		of a playable quiz game
	"""
	global USER_LOGABLE_STATE

	# ensure that he is our guy
	if pwd != ADMIN_KEY:
		return { "e": True, "m": "w" }

	# set the state
	USER_LOGABLE_STATE = state > 0
	return { "e": False, "m": USER_LOGABLE_STATE }

def getLoginState():
	"""
		gets the state of the logable
		flag
	"""

	return USER_LOGABLE_STATE

def endQuiz(pwd):
	"""
		ends the quiz now itself,
		no one can play from now on
	"""
	global QUIZ_ENDED_FLAG

	# ensure that he is our guy
	if pwd != ADMIN_KEY:
		return { "e": True, "m": "w" }

	QUIZ_ENDED_FLAG = True
	return { "e": False, "m": QUIZ_ENDED_FLAG }

def didQuizEnd():
	"""
		tells if the quiz has ended,
		if a quiz is ended there is no way to
		restart it!!!!!!!!!!!!!!!!!!!!!!!!
	"""

	return QUIZ_ENDED_FLAG
