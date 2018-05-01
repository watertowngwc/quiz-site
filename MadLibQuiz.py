from Quiz import *


class MadLibQuestion(Question):

    def __init__(self, json_dict):
        Question.__init__(self, json_dict)
        self.options = ['enter here']

    def parse_json(self, json_dict):
        self.text = json_dict['text']
        self.paragraph = json_dict['paragraph']


    def grade(self):
        self.answered_correctly = True
        for option in self.options:
            print("{}: {} {}".format(option.text, option.is_correct, option.chosen))
            if option.is_correct != option.chosen:
                self.answered_correctly = False
                break
        return self.answered_correctly


class MadLibQuiz(Quiz):

    def make_new_question(self, question_json):
        return MadLibQuestion(question_json)

    def check_quiz(self, answers):
        self.result = ""
        for entry in answers.lists():
            question_num = entry[0]
            print(question_num)
            print(len(self.questions))
            for word in entry[1]:
                self.result = word
                paragraph = self.questions[int(question_num)].paragraph
                paragraph = paragraph.replace('{}', '{0}')
                self.result += paragraph.format(word)


    def get_template(self):
        return 'check_mad_lib.html'
