import unittest
import sys
import pygame
import pygame.tests

sys.path.append("Cycle_2")
from player import Player
from main import game_loop


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
    pygame.tests.run()