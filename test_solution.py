import unittest
from exp1_refa_for_lab6 import Solution


class TestSolution(unittest.TestCase):
    def test_simplify_1_1_all(self):
        s = Solution("3x", "!simplify x=3")
        self.assertEqual(s.setup(), "9.0")

    def test_simplify_1_n_all(self):
        s = Solution("x^3", "!simplify x=3")
        self.assertEqual(s.setup(), "27.0")

    def test_simplify_n_1_all(self):
        s = Solution("3x+4y", "!simplify x=3, y=2")
        self.assertEqual(s.setup(), "17.0")

    def test_simplify_n_n_all(self):
        s = Solution("3x^2+4y^2", "!simplify x=3, y=2")
        self.assertEqual(s.setup(), "43.0")

    def test_simplify_n_1_pat(self):
        s = Solution("3x+2y", "!simplify x=3")
        self.assertEqual(s.setup(), "2*y^1+9.0")

    def test_simplify_n_n_pat(self):
        s = Solution("3x^2+4y^3", "!simplify x=3")
        self.assertEqual(s.setup(), "4*y^3+27.0")

    def test_simplify_no_sense(self):
        s = Solution("hahaha", "!simplify x=3")
        self.assertEqual(s.setup(), "Error")

if __name__ == "__main__":
    unittest.main()