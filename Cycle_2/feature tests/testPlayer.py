import unittest
import sys
sys.path.append("Cycle_2")
from player import Player
import pygame

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.islower())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

class TestPlayerAttributes(unittest.TestCase):


    def test_lives(self):
        pygame.init()
        window = pygame.display.set_mode([600, 600])
        testPlayer = Player(600,600)
        
        self.assertEqual(testPlayer.lives, 3)
        print("Lives are: ",testPlayer.lives)

    def test_speed(self):
        pygame.init()
        window = pygame.display.set_mode([600, 600])
        testPlayer = Player(600,600)

        self.assertEqual(testPlayer.speed,7)

if __name__ == '__main__':
    unittest.main()