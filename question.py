class Question:
    def __init__(self, level, text, answers, right_answer):
        self.level = level
        self.text = text
        #answers is a dictionary {answer_id: answer}
        self.answers = answers
        #right answer is an int
        self.right_answer = right_answer

    def __eq__(self, other):
        return self.text == other.text

    def is_answer_correct(self, answer_id):
        return answer_id == self.right_answer
