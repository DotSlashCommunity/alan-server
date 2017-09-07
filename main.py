# @author ksdme
# main server script
# to run using uWSGI
# uwsgi --http :5000 --wsgi-file main.py --callable app
from peewee import SqliteDatabase

from alan.abstract.login import *
from alan.abstract.scores import *
from alan.abstract.questions import *
from alan.abstract.moderator import *
from alan.db.models import QuestionModel, DetailModel, ReplyModel

from flask import Flask, jsonify, request, session
from flask_cors import CORS

# sqlite and models database
slash = SqliteDatabase("slash.db")
Reply = ReplyModel.getModel(slash)
Detail = DetailModel.getModel(slash)
Question = QuestionModel.getModel(slash)

# initialise app
app = Flask(__name__)
app.config.from_pyfile('main.cfg')
CORS(app, supports_credentials=True)

# Make Sessions Permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

# -----------------------------------
# Logging In and Out
# -----------------------------------
@app.route("/login")
def login():

    # check if the quiz event is alive
    if didQuizEnd():
        return jsonify({ "e": True, "m": "qe" })

    # check if logging in has been
    # freezed
    if not getLoginState():
        return jsonify({ "e": True, "m": "lf" })

    # the details
    roll = request.args.get("r")
    phone = request.args.get("p")

    # try loggingin in
    return jsonify(doLogin(
        roll, phone, session, Detail))

@app.route("/logout")
def logout():

    # check if logging in has been
    # freezed
    if not getLoginState():
        return jsonify({ "e": True, "m": "lf" })

    return jsonify(doLogout(
        session))

@app.route("/me")
def getMe():

    return jsonify({ "m": int(getLoggedIn(session)) })

# -----------------------------------
# Questioning and Submitting Section
# -----------------------------------
@app.route("/question/<int:qno>")
def getQuestion(qno):

    # check if the quiz event is alive
    if didQuizEnd():
        return jsonify({ "e": True, "m": "qe" })

    # know if the quiz has started yet,
    # check the flag for it
    if not getQuizState():
        return jsonify({ "e": True, "m": "qf" })

    if not checkLoggedIn(session):
        return jsonify({ "e": True, "m": "n" })

    return jsonify(getPresentableQuestion(
        getLoggedIn(session), qno, Question, Reply, 20))

@app.route("/submit/<int:qno>")
def submitAnswer(qno):

    # check if the quiz event is alive
    if didQuizEnd():
        return jsonify({ "e": True, "m": "qe" })

    # know if the quiz has started yet,
    # check the flag for it
    if not getQuizState():
        return jsonify({ "e": True, "m": "qf" })

    if not checkLoggedIn(session):
        return jsonify({ "e": True, "m": "n" })

    return jsonify(getPresentableSubmission(
        getLoggedIn(session), qno, request.args.get("a"), Question, Reply, ReplyModel, 20))

# -----------------------------------
# Moderator Utils
# -----------------------------------
@app.route("/state/quiz/<int:state>")
def setQuizStateRouter(state):

    # get the password
    paswd = request.args.get("w")

    return jsonify(setQuizState(
        paswd, state))

@app.route("/state/quiz")
def getQuizStateRouter():
    
    return jsonify(
        getQuizState())

@app.route("/state/login/<int:state>")
def setLoginStateRouter(state):

    # get the password
    paswd = request.args.get("w")

    return jsonify(setLoginState(
        paswd, state))

@app.route("/state/login")
def getLoginStateRouter():
    
    return jsonify(
        getLoginState())

@app.route("/timer/start")
def startTimerRouter():

    # get the password
    paswd = request.args.get("w")

    return jsonify(startTimer(
        paswd))

@app.route("/timer")
def getTimerRouter():

    return jsonify(getTimer())

# -----------------------------------
# Misc Value Utils
# -----------------------------------
@app.route("/scores")
def getScoresRouter():

    return jsonify({
        "list": getScores(Reply)})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
