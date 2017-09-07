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
		key=lambda l: l[1])))
