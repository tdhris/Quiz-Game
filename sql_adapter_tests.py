import unittest
import sql_adapter
from question import Question


class TestAdapter(unittest.TestCase):
    def setUp(self):
        sql_adapter.create_table()

    def tearDown(self):
        sql_adapter.delete_database()

    def test_save_load_question(self):
        answers = {1: '4', 2: '5', 3: '6', 4: '7'}
        q_text = '2 + 2 = ?'
        question = Question(1, q_text, answers, 1)
        sql_adapter.save_question(question)

        self.assertEqual(q_text, sql_adapter.load_question(1).text)


if __name__ == '__main__':
    unittest.main()
