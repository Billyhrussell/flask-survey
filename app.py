from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def home_page():
    """Display home page. Set "responses" in session as an empty list"""

    session["responses"] = []

    return render_template("survey_start.html", survey = survey)

@app.post("/begin")
def redirect_to_questions():
    """On button click, redirect to questions"""
    return redirect("/questions/0")

@app.get("/questions/<int:index>")
def shows_questions(index):
    """Display questions page with radio form for question choices; redirects to
    current unanswered questions if user attempts to manually navigate away, or
    thank-you page if user finishes the survey"""

    if not index == len(session["responses"]):
        flash("Accessing an invalid question! Please answer current inquiry.")
        return redirect(f"/questions/{len(session['responses'])}")
    elif len(session["responses"]) == len(survey.questions):
        return redirect("/surveycomplete")
    else:
        question = survey.questions[index]
        return render_template("question.html", question = question)

@app.post("/answer")
def submit_answer():
    """Take answer from form and add info to response session. redirect to
        next question. If questions finished, show thank-you page"""
    answer = request.form.get("value")

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    return redirect(f"/questions/{len(session['responses'])}")

@app.get("/surveycomplete")
def end_of_survey():
    "Shows thank-you page upon survey completion"

    return render_template("completion.html")

