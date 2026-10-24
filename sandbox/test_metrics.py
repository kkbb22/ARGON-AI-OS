import unittest
from metrics import calculate_bmi, categorize_bmi

class TestClinicalMetrics(unittest.TestCase):
    def test_bmi_normal(self):
        bmi = calculate_bmi(70, 1.75)
        self.assertEqual(bmi, 22.86)
        self.assertEqual(categorize_bmi(bmi), 'NORMAL')

    def test_bmi_underweight(self):
        bmi = calculate_bmi(50, 1.75)
        self.assertEqual(bmi, 16.33)
        self.assertEqual(categorize_bmi(bmi), 'UNDERWEIGHT')

    def test_invalid_height(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)

if __name__ == '__main__':
    unittest.main()
