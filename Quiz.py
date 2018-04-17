class Option():

    def __init__(self, json_list):
        self.parse_json(json_list)

    def parse_json(self, json_list):
        self.text = json_list[0]
        if len(json_list) > 1:
            self.is_correct = json_list[1]
        else:
            self.is_correct = False
        self.answer = None
        self.chosen = False

class Question:

    def __init__(self, json_dict):
        self.parse_json(json_dict)

    def parse_json(self, json_dict):
        self.text = json_dict['text']
        self.options = []
        for option_json in json_dict['options']:
            self.options.append(Option(option_json))
        self.answered_correctly = False

    def grade(self):
        self.answered_correctly = True
        for option in self.options:
            print("{}: {} {}".format(option.text, option.is_correct, option.chosen))
            if option.is_correct != option.chosen:
                self.answered_correctly = False
                break
        return self.answered_correctly


class AnsweredQuestion(Question):

    def __init__(self):
        pass

class Quiz:

    def __init__(self, json_dict):
        self.parse_json(json_dict)

    def parse_json(self, json_dict):
        self.name = json_dict['name']
        self.description = json_dict.get('description', '')
        # self.quiz_type = json_dict.get('quiz_type', 'graded')
        self.style_name = json_dict.get('style_name', 'style')
        self.questions = []
        for question_json in json_dict['questions']:
            self.questions.append(Question(question_json))

        self.question_type = json_dict.get('question_type', 'checkbox')  # ['checkbox', 'radio', 'text']
        pass

    def get_num_questions(self):
        return len(self.questions)

    def check_quiz(self, answers):
        for entry in answers.lists():
            question_num = entry[0]
            for option_num in entry[1]:
                self.questions[int(question_num)].options[int(option_num)].chosen = True

        for question in self.questions:
            question.grade()

    def get_number_correct(self):
        number_correct = 0
        for question in self.questions:
            if question.answered_correctly:
                number_correct += 1
        return number_correct


class AnsweredQuiz(Quiz):

    def __init__(self, quiz, answers):
        pass