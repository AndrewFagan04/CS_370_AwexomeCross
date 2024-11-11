import unittest
import sys
import pygame
import pygame.tests

sys.path.append("Cycle_2")
from main import game_loop
from screens import add_high_score

class TestHighScore(unittest.TestCase):
    def test_high_score(self):
        test_scores = [5000,4000,3000,2000,1000]
        test_scores2 = []
        add_high_score(test_scores,3030)

        add_high_score(test_scores2,500)
        add_high_score(test_scores2,5400)
        add_high_score(test_scores2,500)

        self.assertEqual(test_scores,[5000,4000,3030,3000,2000])
        self.assertEqual(test_scores2,[5400,500,500])


if __name__ == '__main__':
    unittest.main()
    pygame.tests.run()