import sqlite3
from random import randint
from question import Question

conn = sqlite3.connect("quiz_game.db")
cursor = conn.cursor()


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions\
               (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT,
                right_answer INTEGER, difficulty_level INTEGER,\
                FOREIGN KEY(right_answer) REFERENCES answers(answer_id))''')

    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS answers\
        (answer_id INTEGER PRIMARY KEY AUTOINCREMENT,\
            answer_text TEXT, question_id INTEGER,
            FOREIGN KEY(question_id) REFERENCES questions(id))''')

    conn.commit()


def drop_tables():
    cursor.execute('DROP TABLE IF EXISTS questions')
    cursor.execute('DROP TABLE IF EXISTS answers')
    conn.commit()


def save_question(question):
    question_text = question.text
    difficulty_level = question.level
    right_answer = question.right_answer

    cursor.execute("INSERT INTO questions (question,\
                                           right_answer,\
                                           difficulty_level)\
                    VALUES (?, ?, ?)", (question_text,
                                        right_answer,
                                        difficulty_level))
    question_id = cursor.lastrowid
    conn.commit()
    for answer in question.answers.values():
        cursor.execute('INSERT INTO answers (answer_text, question_id)\
                        VALUES (?, ?)', (answer, question_id))
        conn.commit()


def load_question(question_id):
    cursor.execute("SELECT question, right_answer, difficulty_level\
                    FROM questions WHERE id = ?", (question_id,))
    unparsed_question = cursor.fetchone()
    question_text = unparsed_question[0]
    right_answer = unparsed_question[1]
    difficulty_level = unparsed_question[2]

    cursor.execute("SELECT answer_id, answer_text FROM answers\
                    WHERE question_id = ?", (question_id,))
    unparsed_answers = cursor.fetchall()
    answers = {}
    for unparsed_answer in unparsed_answers:
        answer_id = unparsed_answer[0]
        answer_text = unparsed_answer[1]
        answers[answer_id] = answer_text

    question = Question(difficulty_level, question_text, answers, right_answer)
    return question


def load_level_question(level):
    cursor.execute("SELECT id FROM questions\
                    WHERE difficulty_level = ?", (level,))
    questions_ids = [fetched_id[0] for fetched_id in cursor.fetchall()]
    if not questions_ids:
        return False

    random_id = randint(1, len(questions_ids)) - 1
    question_id = questions_ids[random_id]
    question = load_question(question_id)
    return question


def count_questions():
    cursor.execute("SELECT Count(id) FROM questions")
    question_count = cursor.fetchone()[0]
    return question_count
