# @author ksdme
# Calculates Scores

def getScores(rmodel):
	"""
		calculate the scores of all
		the guys and sort them out
	"""

	players, scores = rmodel.select(), {}
	for player in players:
		scores[player.roll] = sum(map(
			lambda l: 0 if l < 0 else l,
			player.replies.values()))

	# send a list of lists,
	# dict may rearrange, list
	# stays ordered!
	return map(list, (sorted(
		scores.iteritems(),
		key=lambda l: l[1], reverse=True)))

def getDetails(dmodel):
	"""
		get the details of the users from
		database, using an dmodel
	"""
	try:
		playas, actual = dmodel.select(), {}
		for player in playas:
			actual[player.roll] = player.name
	except:
		return { "e": True, "m": "z" }

	return actual
