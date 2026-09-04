import unittest
from arithmetic_operations import add, subtract, multiply, divide


class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-1, -3), -4)

    def test_zero(self):
        self.assertEqual(add(0, 5), 5)


class TestSubtract(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_negative(self):
        self.assertEqual(subtract(-1, -3), 2)

    def test_zero(self):
        self.assertEqual(subtract(0, 5), -5)


class TestMultiply(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_negative(self):
        self.assertEqual(multiply(-2, 3), -6)

    def test_zero(self):
        self.assertEqual(multiply(0, 5), 0)


class TestDivide(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(divide(6, 3), 2)

    def test_negative(self):
        self.assertEqual(divide(-6, 3), -2)

    def test_zero_dividend(self):
        self.assertEqual(divide(0, 5), 0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as ctx:
            divide(5, 0)
        self.assertEqual(str(ctx.exception), "Cannot divide by zero")


if __name__ == "__main__":
    unittest.main()
