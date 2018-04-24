class Option:

    def __init__(self, json_list):
        self.text = ''           # the text of the option
        self.is_correct = False  # whether this is the correct answer to the question
        self.chosen = False      # whether this option was chosen by the user
        self.parse_json(json_list)

    def parse_json(self, json_list):
        self.text = json_list[0]
        if len(json_list) > 1:
            self.is_correct = json_list[1]
        else:
            self.is_correct = False
        self.chosen = False


class Question:

    def __init__(self, json_dict):
        self.text = ''           # the text of the question
        self.parse_json(json_dict)

    def parse_json(self, json_dict):
        raise NotImplementedError

    def grade(self):
        raise NotImplementedError


class MultipleChoiceQuestion(Question):

    def __init__(self, json_dict):
        Question.__init__(self, json_dict)
        self.options = []
        self.answered_correctly = False

    def parse_json(self, json_dict):
        self.text = json_dict['text']
        self.options = []
        for option_json in json_dict['options']:
            new_option = Option(option_json)
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


class Quiz:

    def __init__(self, json_dict):
        self.questions = []
        self.name = ''
        self.description = ''
        self.style_name = ''
        self.question_type = ''
        self.parse_json(json_dict)

    def make_new_question(self, question_json):
        raise NotImplementedError

    def parse_json(self, json_dict):
        self.name = json_dict['name']
        self.description = json_dict.get('description', '')
        self.style_name = json_dict.get('style_name', 'style')
        self.questions = []
        for question_json in json_dict['questions']:
            new_question = self.make_new_question(question_json)
            # new_question = Question(question_json)
            self.questions.append(new_question)

        self.question_type = json_dict.get('question_type', 'checkbox')  # ['checkbox', 'radio', 'text']

    def get_num_questions(self):
        return len(self.questions)

    def check_quiz(self, answers):
        raise NotImplementedError

    def get_number_correct(self):
        number_correct = 0
        for question in self.questions:
            if question.answered_correctly:
                number_correct += 1
        return number_correct


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
