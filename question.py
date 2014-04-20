from random import shuffle


class Question:
    def __init__(self, level, text, answers):
        self.level = level
        self.text = text
        #self.answers is a list of Answer objects
        self.answers = answers

    def __eq__(self, other):
        return self.text == other.text

    def shuffle_answers(self):
        self.answers = shuffle(self.answers)
