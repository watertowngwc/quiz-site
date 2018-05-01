class Option:

    def __init__(self, json_list):
        self.text = ''           # the text of the option
        self.chosen = False      # whether this option was chosen by the user
        self.parse_json(json_list)

    def parse_json(self, json_list):
        raise NotImplementedError


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


class SorterOption(Option):

    def __init__(self, json_list):
        self.points_toward = ''
        Option.__init__(self, json_list)

    def parse_json(self, json_list):
        self.text = json_list[0]
        if len(json_list) > 1:
            self.points_toward = json_list[1]
        else:
            self.points_toward = None


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


class SorterQuestion(Question):

    def __init__(self, json_dict):
        self.options = []
        Question.__init__(self, json_dict)

    def parse_json(self, json_dict):
        self.text = json_dict['text']
        self.options = []
        for option_json in json_dict['options']:
            new_option = SorterOption(option_json)
            self.options.append(new_option)

    def grade(self):
        results = []
        for option in self.options:
            if option.chosen:
                results.extend(option.points_toward)
        return results


class Quiz:

    def __init__(self, json_dict):
        self.questions = []
        self.name = ''
        self.description = ''
        self.style_name = ''
        self.question_type = ''
        self.tags = ['']   # the empty string allows for filtering for all quizzes when tag = ''
        self.parse_json(json_dict)

    def make_new_question(self, question_json):
        raise NotImplementedError

    def parse_json(self, json_dict):
        self.name = json_dict['name']
        self.description = json_dict.get('description', '')
        self.style_name = json_dict.get('style_name', 'style')
        self.tags.extend(json_dict.get('tags', ''))
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

    def get_template(self):
        raise NotImplementedError


