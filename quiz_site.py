import copy
import flask
import json
import os
import random
import search
from Quiz import *

app = flask.Flask(__name__)
quiz_dir = 'quizzes'

quizzes = {}
for quiz in os.listdir(quiz_dir):
    print('Loading {}'.format(quiz))
    quizzes[quiz] = Quiz(json.loads(open(os.path.join(quiz_dir, quiz)).read()))

style_button = json.loads(open(os.path.join('config', 'config.json')).read())

@app.route('/')
def index():
    # create a list of tuples of (quiz_id, quiz_name) for displaying on the front page
    quiz_names = []
    for quiz_id in quizzes:
        quiz_names.append((quiz_id, quizzes[quiz_id].name))

    return flask.render_template('index.html', quiz_names=quiz_names, style_button=style_button)

@app.route('/highscore')
def highscore():
    scoreboard= [["Maeve",235634],["Rebecca", 784356789]]# no
    return flask.render_template('highscore.html',scoreboard=scoreboard)

@app.route('/about')
def about():
    return flask.render_template('about.html',)

@app.route('/change_style', methods=['POST'])
def change_style():
    global style_button
    if style_button == True:
        style_button = False
    else:
        style_button = True
    return flask.redirect(flask.url_for('index'))

@app.route('/tags')
def tags():
    return flask.render_template('tags.html', categories=search.sites)

@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):
    if quiz_name not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[quiz_name])
    # questions = list(enumerate(quiz["questions"]))
    # quiz["questions"] = map(lambda t: t[1], questions)
    # ordering = list(map(lambda t: t[0], questions))

    return flask.render_template('quiz.html', quiz_name=quiz_name, quiz=quiz)

@app.route('/fun')
def fun():
    return flask.render_template('fun.html')

@app.route("/search", methods=['POST'])
def search():
    print(flask.request.form["search"])
    # create a dictionary of {quiz_id: quiz_name}
    all_quizzes = {}
    for quiz_id in quizzes:
        all_quizzes[quiz_id] = quizzes[quiz_id].name

    print(all_quizzes)
    print(type(all_quizzes))
    search_results = {}
    for idno in all_quizzes:
        if flask.request.form["search"].lower() in all_quizzes[idno].lower():
            search_results[idno] = all_quizzes[idno]
            print(search_results)
    return flask.render_template('search.html',quiz_names=search_results)

@app.route('/check_quiz/<quiz_name>', methods=['POST'])
def check_quiz(quiz_name):
    # Get the  answers from the form. Make them a dictionary.
    # If they chose option # 2 for question # 3, then
    # answers['3'] would be '2'
    answers = dict(flask.request.form.items())
    # Print to console for debugging
    print(flask.request.form)
    print(answers)
    # Redirect them back to the quiz page if no questions were answered
    if len(answers) == 0:
        return flask.redirect(flask.url_for('quiz', quiz_name=quiz_name))

    quiz = copy.deepcopy(quizzes[quiz_name])
    quiz.check_quiz()
    return flask.render_template('check_quiz.html', quiz=quiz)

    # # Get a copy of this quiz
    # # We can make changes to the copy without affecting the original
    # quiz = copy.deepcopy(quizzes[quiz_name])
    # # Print to console for debugging
    # print(quiz)
    # # Every quiz has a list of questions
    # # Every question has its text and a list of options
    # # Now we go through the questions for this quiz
    # number_correct = 0
    # for question_number, question in enumerate(quiz['questions']):
    #     # question_number is a literal number, like for example 4
    #     # We need it to be a string, not a number. '4' is not the same as 4
    #     question_number_str = str(question_number)
    #     # If they gave an answer for this question, what is it?
    #     if question_number_str in answers:
    #         their_answer = answers[question_number_str]
    #     else:
    #         their_answer = None
    #     # Every question has a list of options
    #     # Every option is a list of two values, like:
    #     #   ['The Aristocats', True]
    #     # For this question, we go through its list of options
    #     question_correct = False
    #     for option_number, option in enumerate(question['options']):
    #         # Is this option the one they chose for this question?
    #         if str(option_number) == their_answer:
    #             # Mark this option as chosen
    #             option.append(True)
    #             # If this option is correct, then they got it right!
    #             if option[1] == True:
    #                 question_correct = True
    #                 number_correct = number_correct + 1
    #         # If this option was not chosen...
    #         else:
    #             # Mark this option as not chosen
    #             option.append(False)
    #         # Now every option has a third value that is True or False, like:
    #         #   ['The Aristocats', True, False]
    #     # For this question, question_correct is now either True or False
    #     # We put question_correct in this question's dictionary
    #     question['is_correct'] = question_correct
    # # Print to console for debugging
    # print(quiz['questions'])
    # # Show the results page
    # return flask.render_template('check_quiz.html',
    #                              quiz=quiz,
    #                              correct=number_correct,
    #                              total=len(quiz['questions'])
    #                              )


if __name__ == '__main__':
    app.run(debug=True)#, host='0.0.0.0', port=5000)

