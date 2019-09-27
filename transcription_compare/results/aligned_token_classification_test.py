import unittest

from transcription_compare.results.aligned_token_classifier import ErrorType
from transcription_compare.results.alignment_result import AlignedToken

class TestCerFirst(unittest.TestCase):
    """
    """
    def test_1(self):
        """
        """
        aligned_token = AlignedToken(reference="lords", outputs=["lord's"])
        print("lords, outputs=[lord's]", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_2(self):
        """
        I think we can add more typr
        """
        aligned_token = AlignedToken(reference="i've", outputs=["ive"])
        print("i've, outputs=[ive", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.NOT_IN_WORD_NET)

    def test_double(self):
        """
        """
        aligned_token = AlignedToken(reference="to", outputs=["to", "to"])
        self.assertEqual(aligned_token.classify(), ErrorType.DOUBLE)

    def test_number(self):
        """
        """
        # pass
        aligned_token = AlignedToken(reference="eighteenth", outputs=["eighteen"])
        print("eighteen", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.NUMBER)

    def test_same_stem(self):
        """
        """
        aligned_token = AlignedToken(reference="hope", outputs=["hopeful"])
        print('hope", outputs=["hopeful', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_same_stem2(self):
        """
        """
        aligned_token = AlignedToken(reference="asking", outputs=["ask"])
        print('asking", outputs=["ask', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_same_meaning(self):
        """
        """
        pass
        aligned_token = AlignedToken(reference="gonna", outputs=["going", "to"])
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_MEANING)

    def test_split(self):
        """
        """
        aligned_token = AlignedToken(reference="todo", outputs=["to", "do"])
        print('todo', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SPLIT)

    def test_possessive(self):
        """
        """
        aligned_token = AlignedToken(reference="daniel", outputs=["daniel's"])
        print("reference=daniel, outputs=[daniel's]", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_name(self):
        """
        """
        pass
        aligned_token = AlignedToken(reference="cindy", outputs=["sindy"])
        print("daryl", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.IS_BOTH_NAME_MATCH)

    def test_name2(self):
        """
        """
        aligned_token = AlignedToken(reference="daryl", outputs=["H"])
        print("daryl", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.IS_REFERENCE_NAME)

    def test_difficult_word(self):
        """
        """
        pass
        aligned_token = AlignedToken(reference="that", outputs=["but"])
        print("that", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.UNKNOWN)

    def test_verb_tense(self):
        """
        """
        aligned_token = AlignedToken(reference="long", outputs=["longed"])
        print('reference="long", outputs=["longed"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)
        # ???????????????????????????????????????????????????????

    def test_verb_tense_BE(self):
        """
        MAYBE WE CAN HAVE ONE MOE FOR be
        """
        aligned_token = AlignedToken(reference="are", outputs=["were"])
        print('reference="are", outputs=["were"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.BE_VERB)
        # self.assertEqual(error_type_classify(aligned_token), ErrorType.VERB_TENSE)

    def test_verb_tense2(self):
        """
        """
        aligned_token = AlignedToken(reference="deposes", outputs=["deposed"])
        print('reference="deposes", outputs=["deposed"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_plural(self):
        """
        """
        aligned_token = AlignedToken(reference="lords", outputs=["lord"])
        print('reference="lords", outputs=["lord"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.PLURAL)

    def test_plurals(self):
        """
        """
        aligned_token = AlignedToken(reference="apple", outputs=["apples"])
        print('apple', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.PLURAL)

    def test_plural2(self):
        """
        """
        aligned_token = AlignedToken(reference="mean", outputs=["means"])
        print('reference="mean", outputs=["means"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.PLURAL)

    def test_plural3(self):
        """
        """
        aligned_token = AlignedToken(reference="nebuchadnezzar's", outputs=["nebuchadnezzars's"])
        print("reference=nebuchadnezzar's, outputs=[nebuchadnezzars's]", aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.SAME_STEM_OTHER)

    def test_plural4(self):
        """
        """
        aligned_token = AlignedToken(reference="men", outputs=["man"])
        print('reference="men", outputs=["man"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.PLURAL)

    def test_plural5(self):
        """
        """
        aligned_token = AlignedToken(reference="enable", outputs=["enables"])
        print('reference="enable", outputs=["enables"]', aligned_token.classify())
        self.assertEqual(aligned_token.classify(), ErrorType.PLURAL)






