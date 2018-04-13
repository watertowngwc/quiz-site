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
# no
style_button = json.loads(open(os.path.join('config', 'config.json')).read())

@app.route('/')
def index():
    return flask.render_template('index.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())), style_button=style_button)
# no
@app.route('/highscore')
def highscore():
    scoreboard= [["Maeve",235634],["Rebecca", 784356789]]# no
    return flask.render_template('highscore.html',scoreboard=scoreboard)
# no
@app.route('/about')
def about():
    return flask.render_template('about.html',)

@app.route('/change_style', methods=['POST'])
def change_style():
    global style_button
    if style_button == True:
        style_button = False
        # no
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
    print(all_quizzes)# no
    print(type(all_quizzes))
    search_results = {}
    for idno in all_quizzes:
        if flask.request.form["search"].lower() in all_quizzes[idno].lower():
            search_results[idno] = all_quizzes[idno]
            print(search_results)
    return flask.render_template('search.html',quiz_names=search_results)
# no
@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    quiz = copy.deepcopy(quizzes[id])

    # create dict of the user's answers, with those answer details from the 
    #   official quiz dict, which includes whether they are correct
    answers = {}
    for k, v in flask.request.form.items():
        answers[int(k)] = quiz['questions'][int(k)]['options'][int(v)]

    # debug prints
    print(flask.request.form)
    print(quiz['questions'])
    print("answers dict:")
    print(answers)
    
    # redirect to the quiz page if no questions were answered
    if not len(answers.keys()):
        return flask.redirect(flask.url_for('quiz', id=id))

    # if a question was un-answered, set as incorrect
    for k in range(len(quiz['questions'])):
        if k not in answers:
            answers[k] = [None, False]

    # answers list is created as a list of lists, each list containing the answer 
    #   and a bool  for correct option/incorrect option
    answers_list = [ answers[k] for k in sorted(answers.keys()) ]
    number_correct = len([ a for a in answers_list if a[1] == True])

    return flask.render_template('check_quiz.html', 
                                 quiz=quiz, 
                                 question_answer=zip(quiz['questions'], answers_list), 
                                 correct=number_correct, 
                                 total=len(answers_list)
                                 )# no


if __name__ == '__main__':
    app.run(debug=True)#, host='0.0.0.0', port=5000)

