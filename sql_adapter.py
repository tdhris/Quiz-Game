import sqlite3
import json
from random import randint
from question import Question
from answer import Answer

QUESTIONS_FILE = "questions/questions.json"


class SQLAdapter:
    def __init__(self):
        self.conn = sqlite3.connect("quiz_game.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.load_questions_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions\
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT,
                    difficulty_level INTEGER)''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers\
                (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                answer_text TEXT, question_id INTEGER,
                FOREIGN KEY(question_id) REFERENCES questions(id))''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS question_answer\
                   (question_id INTEGER, answer_id INTEGER,\
                    FOREIGN KEY(question_id) REFERENCES questions(id),\
                    FOREIGN KEY(answer_id) REFERENCES answers(id))''')

        self.conn.commit()

    def load_questions_table(self):
        file = open(QUESTIONS_FILE)
        questions = json.load(file)
        file.close()

        for unparsed_question in questions:
            question_level = int(unparsed_question["Level"])
            question_text = unparsed_question['Question']
            wrong_answers = [unparsed_question[key] for key in unparsed_question if 'Answer' in key]
            right_answer_text = unparsed_question['Correct']

            answers = []
            for wrong_answer in wrong_answers:
                answer = Answer(wrong_answer)
                answers.append(answer)
            right_answer = Answer(right_answer_text, correct=True)
            answers.append(right_answer)

            question = Question(question_level, question_text, answers)
            self.save_question(question)

    def drop_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS questions')
        self.cursor.execute('DROP TABLE IF EXISTS answers')
        self.cursor.execute('DROP TABLE IF EXISTS question_answer')
        self.conn.commit()

    def save_question(self, question):
        question_text = question.text
        difficulty_level = question.level
        # right_answer = question.right_answer

        self.cursor.execute("INSERT INTO questions (question,\
                                               difficulty_level)\
                             VALUES (?, ?)", (question_text,
                                              difficulty_level))
        question_id = self.cursor.lastrowid
        self.conn.commit()

        for answer in question.answers:
            self.cursor.execute('INSERT INTO answers(answer_text, question_id)\
                                 VALUES (?, ?)', (answer.text, question_id))
            if answer.is_correct:
                answer_id = self.cursor.lastrowid
            self.conn.commit()

        self.cursor.execute("INSERT INTO question_answer(question_id, answer_id)\
                             VALUES (?, ?)", (question_id, answer_id))
        self.conn.commit()

    def load_question(self, question_id):
        '''1) Load Question'''
        self.cursor.execute("SELECT question, difficulty_level\
                             FROM questions WHERE id = ?", (question_id,))
        unparsed_question = self.cursor.fetchone()
        question_text = unparsed_question[0]
        difficulty_level = unparsed_question[1]

        '''2) Get Correct Answer ID'''
        right_answer_id = self.get_right_answer_id(question_id)

        '''3) Load Answers'''
        answers = self.load_answers(question_id, right_answer_id)
        question = Question(difficulty_level, question_text, answers)

        return question

    def load_level_question(self, level):
        self.cursor.execute("SELECT id FROM questions\
                        WHERE difficulty_level = ?", (level,))
        questions_ids = [fetched_id[0] for fetched_id in self.cursor.fetchall()]
        if not questions_ids:
            return False

        random_id = randint(1, len(questions_ids)) - 1
        question_id = questions_ids[random_id]
        question = self.load_question(question_id)
        return question

    def count_questions(self):
        self.cursor.execute("SELECT Count(id) FROM questions")
        question_count = self.cursor.fetchone()[0]
        return question_count

    def load_answers(self, question_id, right_answer_id):
        '''3) Load Answers'''
        self.cursor.execute("SELECT id, answer_text FROM answers\
                        WHERE question_id = ?", (question_id,))
        unparsed_answers = self.cursor.fetchall()

        answers = []
        for unparsed_answer in unparsed_answers:
            answer_id = unparsed_answer[0]
            answer_text = unparsed_answer[1]
            if answer_id != right_answer_id:
                answer = Answer(answer_text)
            elif answer_id == right_answer_id:
                answer = Answer(answer_text, correct=True)
            else:
                return False
            answers.append(answer)
        return answers

    def get_right_answer_id(self, question_id):
        '''2) Get Correct Answer ID'''
        self.cursor.execute("SELECT answer_id FROM question_answer\
                             WHERE question_id = ?", (question_id,))
        right_answer_id = self.cursor.fetchone()[0]
        return right_answer_id
