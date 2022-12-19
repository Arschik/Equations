import unittest
from equations import *
class Test_equations(unittest.TestCase):
    def test_rang(self):
        self.assertEqual(rang([[1,2],[2,4]]),(1,[0],[0]))
        self.assertEqual(rang([[1,2],[2,4],[3,0]]),(2, [0, 2], [0, 1]))
        self.assertEqual(rang([[0,0,0,0]]),(1,[0],[0]))
    def test_det(self):
        self.assertEqual(check_det([[1,2],[3,4]]),-2)
        self.assertEqual(check_det([[1]]),1)
        self.assertEqual(check_det([[1,2,3],[4,5,6],[7,8,9]]),0)
    def test_inversions(self):
        self.assertEqual(check_inversion([1,2,3,4,5]),2)
        self.assertEqual(check_inversion([2,1,3,4,5]),1)
        self.assertEqual(check_inversion([1]),2)
if __name__ == "__main__":
    unittest.main()