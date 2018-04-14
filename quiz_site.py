import copy
import flask
import json
import os
import random
import search

app = flask.Flask(__name__)
quiz_dir = 'quizzes'

quizzes = {}
for quiz in os.listdir(quiz_dir):
    print('Loading {}'.format(quiz))
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

style_button = json.loads(open(os.path.join('config', 'config.json')).read())

@app.route('/')
def index():
    return flask.render_template('index.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())), style_button=style_button)

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

@app.route('/quiz/<id>')
def quiz(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[id])
    # questions = list(enumerate(quiz["questions"]))
    # quiz["questions"] = map(lambda t: t[1], questions)
    # ordering = list(map(lambda t: t[0], questions))

    return flask.render_template('quiz.html', id=id, quiz=quiz)

@app.route('/fun')
def fun():
    return flask.render_template('fun.html')

@app.route("/search", methods=['POST'])
def search():
    print(flask.request.form["search"])
    all_quizzes = dict (zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())))
    print(all_quizzes)
    print(type(all_quizzes))
    search_results = {}
    for idno in all_quizzes:
        if flask.request.form["search"].lower() in all_quizzes[idno].lower():
            search_results[idno] = all_quizzes[idno]
            print(search_results)
    return flask.render_template('search.html',quiz_names=search_results)

@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    responses = dict(flask.request.form.items())

    # redirect to the quiz page if no questions were answered
    if len(responses) == 0:
        return flask.redirect(flask.url_for('quiz', id=id))

    quiz = copy.deepcopy(quizzes[id])

    number_correct = 0
    question_number = 0
    for question in quiz['questions']:

        question_correct = False
        option_number = 0
        for option in question['options']:

            if str(question_number) in responses and responses[str(question_number)] == str(option_number):
                option.append(True)

                if option[1] == True:
                    question_correct = True
                    number_correct = number_correct + 1

            else:
                option.append(False)

            option_number = option_number + 1

        if question_correct == True:
            question['is_correct'] = True
        else:
            question['is_correct'] = False

        question_number = question_number + 1

    # debug prints
    print(flask.request.form)
    print(quiz['questions'])
    print(responses)

    return flask.render_template('check_quiz.html', 
                                 quiz=quiz, 
                                 correct=number_correct,
                                 total=len(quiz['questions'])
                                 )


if __name__ == '__main__':
    app.run(debug=True)#, host='0.0.0.0', port=5000)

