import unittest
from transcription_compare.tokenizer import WordTokenizer


class TestCerFirst(unittest.TestCase):
    """
    """

    def setUp(self) -> None:
        self.word_tokenizer = WordTokenizer()

    def test_into(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="into", brackets_list=[])
        self.assertEqual(r, ["into"])

    def test_into_2(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="in to", brackets_list=[])
        self.assertEqual(r, ["in", "to"])

    def test_into_3(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="into the monitor", brackets_list=[])
        self.assertEqual(r, ["into", "the", "monitor"])

    def test_into_4(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="into", brackets_list=["()"])
        self.assertEqual(r, ["into"])

    def test_into_5(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="in to", brackets_list=["()"])
        self.assertEqual(r, ["in", "to"])

    def test_into_6(self):
        """
        """
        r = self.word_tokenizer.tokenize(token_string="into the monitor", brackets_list=["()"])
        self.assertEqual(r, ["into", "the", "monitor"])


if __name__ == '__main__':
    unittest.main()
