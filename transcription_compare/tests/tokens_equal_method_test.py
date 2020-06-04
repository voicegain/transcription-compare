import unittest
from transcription_compare.tokens import Token


class TestCerFirst(unittest.TestCase):

    def test_uk_uk(self):
        """
        """
        t1 = Token("accessorising", use_alternative_spelling=True)
        t2 = Token("accessorise", use_alternative_spelling=True)
        self.assertFalse(t1 == t2)

    def test_uk_uk_equal(self):
        """
        """
        t1 = Token("accessorising", use_alternative_spelling=True)
        t2 = Token("accessorising", use_alternative_spelling=True)
        self.assertTrue(t1 == t2)

    def test_uk_us(self):
        """
        """
        t1 = Token("accessorising", use_alternative_spelling=True)
        t2 = Token("hi", use_alternative_spelling=True)
        self.assertFalse(t1 == t2)

    def test_uk_us_equal(self):
        """
        """
        t1 = Token("accessorise", use_alternative_spelling=True)
        t2 = Token("accessorize", use_alternative_spelling=True)
        self.assertTrue(t1 == t2)

    def test_us_uk(self):
        """
        """
        t1 = Token("hello", use_alternative_spelling=True)
        t2 = Token("aerogrammes", use_alternative_spelling=True)
        self.assertFalse(t1 == t2)

    def test_us_uk_equal(self):
        """
        """
        t1 = Token("accessorize", use_alternative_spelling=True)
        t2 = Token("accessorise", use_alternative_spelling=True)
        self.assertTrue(t1 == t2)

    def test_us_us(self):
        """
        """
        t1 = Token("hello", use_alternative_spelling=True)
        t2 = Token("hi", use_alternative_spelling=True)
        self.assertFalse(t1 == t2)

    def test_us_us_equal(self):
        """
        """
        t1 = Token("hello", use_alternative_spelling=True)
        t2 = Token("hello", use_alternative_spelling=True)
        self.assertTrue(t1 == t2)

    def test_flier_flier(self):
        """
        """
        t1 = Token("flier", use_alternative_spelling=True)
        t2 = Token("flier", use_alternative_spelling=True)
        self.assertTrue(t1 == t2)


if __name__ == '__main__':
    unittest.main()
