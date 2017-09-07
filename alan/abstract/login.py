# @author ksdme
# login system

# simply in-memory session counter to prevent
# multiple logins
ACTIVE_SESSIONS = {}

def incActiveSession(roll):
	"""
		as the name says, it simply
		increments the no. of sessions
	"""
	if roll is None:
		return

	try:
		ACTIVE_SESSIONS[roll] += 1
	except KeyError:
		ACTIVE_SESSIONS[roll] = 1 

def decActiveSession(roll):
	"""
		decrements the active session counter
	"""
	if roll is None:
		return

	try:
		ACTIVE_SESSIONS[roll] -= 1
	except KeyError:
		ACTIVE_SESSIONS[roll] = 0

	if ACTIVE_SESSIONS[roll] < 0:
		ACTIVE_SESSIONS[roll] = 0

def getActiveSessionCount(roll):
	"""
		returns the no. of active
		sessions of a given user
	"""

	try:
		return ACTIVE_SESSIONS[roll]
	except KeyError:
		return 0

def doLogin(roll, phone, session, dmodel):
	"""
		does the login and sets up
		the session appropriately
	"""

	# ensure that someone hasn't
	# already logged in
	if checkLoggedIn(session):
		return { "e": True, "m": "a" }

	# check that the guy hasn't logged
	# in elsewhere and this aint his
	# second simultaneous login
	if getActiveSessionCount(roll) != 0:
		return { "e": True, "m": "m" }

	# set roll defaulty
	session["roll"] = None

	try:
		player = dmodel.get(dmodel.roll == roll)
		if not player.present:
			return { "e": True, "m": "s" }

	except dmodel.DoesNotExist:
		return { "e": True, "m": "r" }

	# apparently 'phone' is Unicoded
	if unicode(player.phone) != phone:
		return { "e": True, "m": "p" }
	else:
		# no error occoured, log that
		# guy in

		session["roll"] = int(roll)
		incActiveSession(roll)

		return { "e": False }

def checkLoggedIn(session):
	"""
		checks if any player
		has logged in yet
	"""

	try:
		return session["roll"] is not None
	except KeyError:
		session["roll"] = None
		return False

def getLoggedIn(session):
	"""
		check if logged in
		and then return the
		logged roll
	"""

	if checkLoggedIn(session):
		return session["roll"]
	else:
		return False

def doLogout(session):
	"""
		logout the session,
		to make space for new
	"""
	roll = None

	try:
		roll = session["roll"]
	except KeyError: pass

	session["roll"] = None
	decActiveSession(roll)

	return { "e": False }
