import unittest

from transcription_compare.utils.digit_util import DigitUtil


class TestCerFirst(unittest.TestCase):
    """
    """
    def setUp(self) -> None:
        self.digit_util = DigitUtil()

    def test_first(self):
        """
        """
        result = self.digit_util.our_is_digit('1')

        self.assertEqual(result, [{'first', 'one'}])


    def test_2nd(self):
        """
        """
        result = self.digit_util.our_is_digit('0')
        self.assertEqual(result, [{'oh', 'zero', 'zeroth'}])

    def test_3(self):
        """
        """
        result = self.digit_util.our_is_digit('101')
        self.assertEqual(result, [{'one hundred and first',
                                      'one hundred and one',
                                      'one oh one',
                                      'one zero one',
                                      'ten one'}])

    def test_4(self):
        """
        """
        result = self.digit_util.our_is_digit('1st')
        self.assertEqual(result, [{'first'}])

    def test_5(self):
        """
        """
        result = self.digit_util.our_is_digit('12th')
        self.assertEqual(result, [{'one second', 'twelfth'}])
    def test_6(self):
        """
        """
        result = self.digit_util.our_is_digit('3rd')
        self.assertEqual(result, [{'third'}])

    def test_7(self):
        """
        """
        result = self.digit_util.our_is_digit('2000s')
        self.assertEqual(result, [{'two thousands'}])
    def test_8(self):
        """
        """
        result = self.digit_util.our_is_digit('1990s')
        self.assertEqual(result, [{'nineteen nineties'}])
    def test_9(self):
        """
        """
        result = self.digit_util.our_is_digit('40s')
        self.assertEqual(result, [{'forties'}])
    def test_9(self):
        """
        """
        result = self.digit_util.our_is_digit('10,000')
        self.assertEqual(result, [{'one oh oh oh oh',
                                          'one zero zero zero zero',
                                          'ten oh oh oh',
                                          'ten thousand',
                                          'ten zero zero zero'}])

    def test_10(self):
        """
        """
        result = self.digit_util.our_is_digit('h2o')
        self.assertEqual(result, [{'h'}, {'second', 'two'}, {'o'}])

    def test_11(self):
        """
        """
        result = self.digit_util.our_is_digit('m370')
        self.assertEqual(result, [{'m'},
                                     {'thirty-seven oh',
                                      'thirty-seven zero',
                                      'three hundred and seventieth',
                                      'three hundred and seventy',
                                      'three seven oh',
                                      'three seven zero',
                                      'three seventy'}])

if __name__ == '__main__':
    unittest.main()