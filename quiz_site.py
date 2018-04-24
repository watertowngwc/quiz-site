import copy
import flask
import json
import os
import random
import search
from MultipleChoiceQuiz import MultipleChoiceQuiz
from SorterQuiz import SorterQuiz

app = flask.Flask(__name__)
quiz_dir = 'quizzes'


def load_quizzes():
    quizzes = {}
    for quiz in os.listdir(quiz_dir):
        print('Loading {}'.format(quiz))
        quiz_json = json.loads(open(os.path.join(quiz_dir, quiz)).read())
        quiz_type = quiz_json.get('quiz_type', 'multiple_choice')
        if quiz_type == 'multiple_choice':
            quizzes[quiz] = MultipleChoiceQuiz(quiz_json)
        elif quiz_type == 'sorter_quiz':
            quizzes[quiz] = SorterQuiz(quiz_json)
        else:
            print("Invalid quiz type for quiz {} (quiz_type {})".format(quiz, quiz_type))
    return quizzes


quizzes = load_quizzes()
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
    answers = flask.request.form

    # Print to console for debugging
    # print(flask.request.form)
    # print(answers)

    # Redirect them back to the quiz page if no questions were answered
    if len(answers) == 0:
        return flask.redirect(flask.url_for('quiz', quiz_name=quiz_name))

    quiz = copy.deepcopy(quizzes[quiz_name])
    quiz.check_quiz(answers)
    template_to_render = quiz.get_template()
    return flask.render_template(template_to_render, quiz=quiz)


if __name__ == '__main__':
    app.run(debug=True) #, host='0.0.0.0', port=5000)

