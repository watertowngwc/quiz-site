from Quiz import *


class MultipleChoiceOption(Option):

    def __init__(self, json_list):
        self.is_correct = False  # whether this is the correct answer to the question
        Option.__init__(self, json_list)

    def parse_json(self, json_list):
        self.text = json_list[0]
        if len(json_list) > 1:
            self.is_correct = json_list[1]
        else:
            self.is_correct = False
        self.chosen = False


class MultipleChoiceQuestion(Question):

    def __init__(self, json_dict):
        self.options = []
        self.answered_correctly = False
        Question.__init__(self, json_dict)

    def parse_json(self, json_dict):
        self.text = json_dict['text']
        self.options = []
        for option_json in json_dict['options']:
            new_option = MultipleChoiceOption(option_json)
            self.options.append(new_option)
        self.answered_correctly = False

    def grade(self):
        self.answered_correctly = True
        for option in self.options:
            print("{}: {} {}".format(option.text, option.is_correct, option.chosen))
            if option.is_correct != option.chosen:
                self.answered_correctly = False
                break
        return self.answered_correctly


class MultipleChoiceQuiz(Quiz):

    def make_new_question(self, question_json):
        return MultipleChoiceQuestion(question_json)

    def check_quiz(self, answers):
        for entry in answers.lists():
            question_num = entry[0]
            for option_num in entry[1]:
                self.questions[int(question_num)].options[int(option_num)].chosen = True

        for question in self.questions:
            question.grade()

    def get_template(self):
        return 'check_quiz.html'
