import unittest

from transcription_compare.results.aligned_token_classifier import ErrorType
from transcription_compare.results.alignment_result import AlignedToken


class TestCerFirst(unittest.TestCase):
    """
    """
    def test_apostrophe(self):
        """
        """
        aligned_token = AlignedToken(reference="lords", outputs=["lord's"])
        self.assertEqual(aligned_token.classify(), ErrorType.APOSTROPHE)

    def test_apostrophe2(self):
        """
        """
        aligned_token = AlignedToken(reference="i've", outputs=["ive"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.APOSTROPHE)

    def test_double(self):
        """
        """
        aligned_token = AlignedToken(reference="to", outputs=["to", "to"])
        self.assertEqual(aligned_token.classify(), ErrorType.DOUBLE)

    def test_number(self):
        """
        """
        pass
        # aligned_token = AlignedToken(reference="todo", outputs=["to", "do"])
        # self.assertEqual(error_type_classify(aligned_token), ErrorType.SPLIT)

    def test_same_stem(self):
        """
        """
        aligned_token = AlignedToken(reference="hope", outputs=["hopeful"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.SAME_STEM_OTHER)

    def test_same_stem2(self):
        """
        """
        aligned_token = AlignedToken(reference="asking", outputs=["ask"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.SAME_STEM_OTHER)

    def test_same_meaning(self):
        """
        """
        pass
        # aligned_token = AlignedToken(reference="gonna", outputs=["going", "to"])
        # self.assertEqual(error_type_classify(aligned_token), ErrorType.SAME_MEANING)

    def test_split(self):
        """
        """
        aligned_token = AlignedToken(reference="todo", outputs=["to", "do"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.SPLIT)

    def test_possessive(self):
        """
        """
        aligned_token = AlignedToken(reference="daniel", outputs=["daniel's"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.POSSESSIVE)

    def test_name(self):
        """
        """
        pass
        # aligned_token = AlignedToken(reference="daniel", outputs=["daniel's"])
        # self.assertEqual(error_type_classify(aligned_token), ErrorType.NAME)

    def test_verb_tense(self):
        """
        """
        aligned_token = AlignedToken(reference="long", outputs=["longed"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.SAME_STEM_OTHER)
        # ???????????????????????????????????????????????????????

    def test_verb_tense_BE(self):
        """
        """
        aligned_token = AlignedToken(reference="are", outputs=["were"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.VERB_TENSE)


    def test_verb_tense2(self):
        """
        """
        aligned_token = AlignedToken(reference="deposes", outputs=["deposed"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.SAME_STEM_OTHER)

    def test_plural(self):
        """
        """
        aligned_token = AlignedToken(reference="lords", outputs=["lord"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.PLURAL)

    def test_plural2(self):
        """
        """
        aligned_token = AlignedToken(reference="mean", outputs=["means"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.PLURAL)

    def test_plural3(self):
        """
        """
        aligned_token = AlignedToken(reference="nebuchadnezzar's", outputs=["nebuchadnezzars's"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.PLURAL)

    def test_plural4(self):
        """
        """
        aligned_token = AlignedToken(reference="men", outputs=["man"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.PLURAL)

    def test_plural5(self):
        """
        """
        aligned_token = AlignedToken(reference="enable", outputs=["enables"])
        self.assertEqual(error_type_classify(aligned_token), ErrorType.PLURAL)






