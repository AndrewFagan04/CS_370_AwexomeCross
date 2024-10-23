import unittest
import sys

from .. import player

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.islower())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestPlayerAttributes(unittest.TestCase):

    def test_lives(self):
        testPlayer = Player(600,600)
        testPlayer.lives = 3
        self.assertEqual(testPlayer.lives == 3)

if __name__ == '__main__':
    unittest.main()