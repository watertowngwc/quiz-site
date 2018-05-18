import copy
import flask
import json
import os
import random
import search
from MultipleChoiceQuiz import MultipleChoiceQuiz
from SorterQuiz import SorterQuiz
from MadLibQuiz import MadLibQuiz

app = flask.Flask(__name__)
quiz_dir = 'quizzes'


def load_quizzes():
    likes = json.loads(open(os.path.join('config', 'likes.json')).read())
    quizzes = {}
    for quiz in os.listdir(quiz_dir):
        print('Loading {}'.format(quiz))
        quiz_json = json.loads(open(os.path.join(quiz_dir, quiz)).read())
        quiz_type = quiz_json.get('quiz_type', 'multiple_choice')
        if quiz_type == 'multiple_choice':
            quizzes[quiz] = MultipleChoiceQuiz(quiz_json)
        elif quiz_type == 'sorter_quiz':
            quizzes[quiz] = SorterQuiz(quiz_json)
        elif quiz_type == 'mad_lib':
            quizzes[quiz] = MadLibQuiz(quiz_json)
        else:
            print("Invalid quiz type for quiz {} (quiz_type {})".format(quiz, quiz_type))
        quizzes[quiz].likes = likes.get(quiz, 0)
    return quizzes


quizzes = load_quizzes()
style_button = json.loads(open(os.path.join('config', 'config.json')).read())


@app.route('/')
@app.route('/categories/<tags>')
def index(tags=''):
    # create a list of tuples of (quiz_id, quiz_name) for displaying on the front page
    quiz_names = []
    for quiz_id in quizzes:
        if tags in quizzes[quiz_id].tags:
            quiz_names.append((quiz_id, quizzes[quiz_id]))

    quiz_names.sort(key=lambda q: q[1].likes, reverse=True)

    return flask.render_template('index.html', quiz_names=quiz_names, style_button=style_button)

@app.route('/highscore', methods=['GET','POST'])
def highscore():
    quizname= flask.request.form['quizname']
    numberofpointscorrect= flask.request.form['numberofpointscorrect']
    personname = flask.request.form['personname']
    scoreboard=[["rddhyf", 45376822222],
                ["hegf",5362719765]]
    quiz = quizzes[quizname]
    highscores = json.loads(open(os.path.join('config', 'highscores.json')).read())
    print(highscores)
    currenthighscore = quiz.highscore.get(personname, 0)
    print(currenthighscore)
    print(numberofpointscorrect)
    newhighscore = currenthighscore + int(numberofpointscorrect)
    quiz.highscore[personname] = newhighscore
    #quizhighscores = highscores[quizname].get
    if quizname not in highscores:
        highscores[quizname]={personname: newhighscore}
    highscores[quizname][personname] = quiz.highscore[personname]
    json.dump(highscores, open(os.path.join('config', 'highscores.json'), 'w'))

    #make sure highscores are sorted
    highscores_sorted= [(name,quiz.highscore[name])for name in quiz.highscore]
    highscores_sorted.sort(key=lambda q: q[1], reverse=True)
    return flask.render_template('highscore.html',scoreboard=highscores_sorted)

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

# @app.route('/tags')
# def tags():
#     return flask.render_template('tags.html', categories=search.sites)

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

@app.route('/like/<quiz_name>', methods=['POST'])
def like(quiz_name):
    print("Someone clicked LIKE for the quiz called {}".format(quiz_name))
    quiz = quizzes[quiz_name]
    likes = json.loads(open(os.path.join('config', 'likes.json')).read())
    print(likes)
    print("This quiz currently has {} likes".format(quiz.likes))
    if  flask.request.form['like'] == 'dislike':
        quiz.likes += 0
    else:
        quiz.likes += 1
    print("NOW this quiz has {} likes".format(quiz.likes))
    likes[quiz_name] = quiz.likes
    json.dump(likes, open(os.path.join('config', 'likes.json'), 'w'))
    return flask.redirect(flask.url_for('index'))

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
    print(answers)
    quiz.check_quiz(answers)
    template_to_render = quiz.get_template()
    quiz.id = quiz_name
    return flask.render_template(template_to_render, quiz=quiz)


if __name__ == '__main__':
    app.run(debug=True) #, host='0.0.0.0', port=5000)

