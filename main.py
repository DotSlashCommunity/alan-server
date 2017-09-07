# @author ksdme
# main server script
from peewee import SqliteDatabase

from alan.abstract.login import *
from alan.abstract.scores import *
from alan.abstract.questions import *
from alan.db.models import QuestionModel, DetailModel, ReplyModel

from flask import Flask, jsonify, request, session

# sqlite and models database
slash = SqliteDatabase("slash.db")
Reply = ReplyModel.getModel(slash)
Detail = DetailModel.getModel(slash)
Question = QuestionModel.getModel(slash)

# initialise app
app = Flask(__name__)
app.config.from_pyfile('main.cfg')

# -----------------------------------
# Logging In and Out
# -----------------------------------
@app.route("/login")
def login():

    # the details
    roll = request.args.get("r")
    phone = request.args.get("p")

    # try loggingin in
    return jsonify(doLogin(
        roll, phone, session, Detail))

@app.route("/logout")
def logout():

    return jsonify(doLogout(
        session))

# -----------------------------------
# Questioning and Submitting Section
# -----------------------------------
@app.route("/question/<int:qno>")
def getQuestion(qno):

    if not checkLoggedIn(session):
        return jsonify({ "e": True, "m": "n" })

    return jsonify(getPresentableQuestion(
        getLoggedIn(session), qno, Question, Reply, 20))

@app.route("/submit/<int:qno>")
def submitAnswer(qno):

    if not checkLoggedIn(session):
        return jsonify({ "e": True, "m": "n" })

    return jsonify(getPresentableSubmission(
        getLoggedIn(session), qno, request.args.get("a"), Question, Reply, 20))

# -----------------------------------
# Misc Value Utils
# -----------------------------------
@app.route("/scores")
def getScoresRouter():

    return jsonify(
        getScores(Reply))

app.debug = True
app.run()
