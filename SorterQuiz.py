from Quiz import *


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


class SorterQuiz(Quiz):

    def __init__(self, json_dict):
        self.result = ''  # the final answer of the quiz
        Quiz.__init__(self, json_dict)

    def make_new_question(self, question_json):
        return SorterQuestion(question_json)

    def check_quiz(self, answers):
        for entry in answers.lists():
            question_num = entry[0]
            for option_num in entry[1]:
                self.questions[int(question_num)].options[int(option_num)].chosen = True

        # tally up the total points for each category
        category_totals = {}
        for question in self.questions:
            question_points = question.grade()
            for cat in question_points:
                if cat in category_totals:
                    category_totals[cat] += 1
                else:
                    category_totals[cat] = 1

        # find which category has the highest total
        print(category_totals)
        high_score = 0
        winning_category = ''
        for cat in category_totals:
            if category_totals[cat] > high_score:
                high_score = category_totals[cat]
                winning_category = cat

        self.result = winning_category

    def get_template(self):
        return 'check_sorter_quiz.html'
