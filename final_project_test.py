import unittest
from main_program import *
from data import *


DBNAME = "crimes.db"

class TestDatabase(unittest.TestCase):

    def test_crimes_table(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT CrimeName FROM Crimes'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Assault',), result_list)
        self.assertIn(('Robbery',), result_list)
        self.assertIn(('Theft',), result_list)
        self.assertEqual(len(result_list), 7)
        conn.close()

    def test_crime_cases_table(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT CaseNumber FROM CrimeCases'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('170015307',), result_list)
        self.assertIn(('160043117',), result_list)
        self.assertIn(('160044232',), result_list)
        self.assertEqual(len(result_list), 123)
        conn.close()

    def test_crime_tweets_table(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT RetweetCount FROM CrimeTweets'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('7628',), result_list)
        self.assertIn(('591',), result_list)
        self.assertIn(('98',), result_list)
        self.assertEqual(len(result_list), 120)
        conn.close()


class TestOptionOne(unittest.TestCase):

    def test_option_one(self):
        results = option_one()
        self.assertEqual(results[0], 27)
        self.assertEqual(results[1], 25)
        self.assertEqual(results[2], 6)
        self.assertEqual(results[3], 34)

class TestOptionTwo(unittest.TestCase):

    def test_option_two(self):
        results = option_two()
        self.assertEqual(results[4], 20)
        self.assertEqual(results[5], 7)
        self.assertEqual(results[6], 4)


class TestOptionThree(unittest.TestCase):

    def test_option_three(self):
        results = option_three()
        self.assertEqual(results[0], 11)
        self.assertEqual(results[1], 12)
        self.assertEqual(results[2], 11)

class TestOptionFour(unittest.TestCase):

    def test_option_four(self):
        results = option_four()
        self.assertEqual(results[0], 5)
        self.assertEqual(results[1], 1)
        self.assertEqual(results[2], 1)

unittest.main()
