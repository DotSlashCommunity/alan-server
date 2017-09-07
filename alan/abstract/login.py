# @author ksdme
# login system

def doLogin(roll, phone, session, dmodel):
	"""
		does the login and sets up
		the session appropriately
	"""

	# ensure that someone hasn't
	# already logged in
	if checkLoggedIn(session):
		return { "e": True, "m": "a" }

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
		session["roll"] = roll
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

	session["roll"] = None
	return { "e": False }
