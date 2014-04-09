import unittest
import sql_adapter
from question import Question


class TestAdapter(unittest.TestCase):
    def setUp(self):
        sql_adapter.create_table()

    def tearDown(self):
        sql_adapter.drop_tables()

    def test_save_load_question(self):
        answers = {1: '4', 2: '5', 3: '6', 4: '7'}
        q_text = '2 + 2 = ?'
        question = Question(1, q_text, answers, 1)
        sql_adapter.save_question(question)
        self.assertEqual(1, sql_adapter.count_questions())

    def test_load_question_of_a_certain_level(self):
        answers2 = {1: 'x^2 - e', 2: '1/x', 3: 'xlnx', 4: 'e^x'}
        q2_text = 'The derivative of lnx is?'
        question2 = Question(3, q2_text, answers2, 2)
        sql_adapter.save_question(question2)

        self.assertEqual(question2.text, sql_adapter.load_level_question(3).text)


if __name__ == '__main__':
    unittest.main()
