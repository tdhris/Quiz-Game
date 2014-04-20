# from question import Question
from sql_adapter import SQLAdapter


class QuizGame:
    def __init__(self):
        self.adapter = SQLAdapter()
        self.load_questions()

    def load_questions(self):
        self.questions = []
        for level in range(1, 16):
            question = self.adapter.load_level_question(int(level))
            self.questions.append(question)

    def get_next_question(self):
        for question in self.questions:
            yield question


# def main():
#     QuizGame()

# if __name__ == '__main__':
#     main()
