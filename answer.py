class Answer:
    def __init__(self, text, correct=False):
        self.text = text
        self.is_correct = correct

    def __eq__(self, other):
        return self.text == other.text

    def __repr__(self):
        return self.text
