import unittest
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.results import AlignmentResult


class TestCerFirst(unittest.TestCase):
    """
    """

    def setUp(self) -> None:
        self.calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=CharacterTokenizer(),
            get_alignment_result=True
        )
        self.wer_calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=WordTokenizer(),
            get_alignment_result=True
        )

    def test_files(self):
        """
        """
        file1 = open('r_file.txt', 'r')
        R = file1.read()

        file2 = open('o_file.txt', 'r')
        O = file2.read()

        result = self.wer_calculator.get_distance(R, O)
        print(result.distance)
        self.assertEqual(result.distance, 373)

        expected_alignment_result = AlignmentResult()
        expected_alignment_result.load_from_file('resultoffilr.txt', expected_alignment_result)
        distance, substitution, insertion, deletion =expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
       # self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_first(self):
        """
        """
        result = self.calculator.get_distance('abc', 'dfg')
        self.assertEqual(result.distance, 3)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="a", output_tokens=["d"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="b", output_tokens=["f"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="c", output_tokens=["g"], add_to_left=False)
        # result.alignment_result == expected_alignment_result
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)

        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_2nd(self):
        """
        """
        result = self.calculator.get_distance('AV', 'Abc')
        self.assertEqual(result.distance, 2)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="A", output_tokens=["A", "b"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="V", output_tokens=["c"], add_to_left=False)
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_3(self):
        """
        """
        result = self.calculator.get_distance('batman', 'b')
        self.assertEqual(result.distance, 5)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="b", output_tokens=["b"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="t", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="m", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="n", output_tokens=[], add_to_left=False)
        expected_alignment_result.merge_none_tokens()
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_4(self):
        """
        """
        result = self.calculator.get_distance('b', 'batman')
        self.assertEqual(result.distance, 5)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="b", output_tokens=["b", "a", "t", "m", "a", "n"], add_to_left=False)
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_5(self):
        """
        """
        result = self.calculator.get_distance('AVERY', 'GARVEY')
        self.assertEqual(result.distance, 3)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="A", output_tokens=["G", "A", "R"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="V", output_tokens=["V"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="E", output_tokens=["E"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="R", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="Y", output_tokens=["Y"], add_to_left=False)
        expected_alignment_result.merge_none_tokens()
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_6(self):
        """
        """
        result = self.calculator.get_distance('ernest', 'nester')
        self.assertEqual(result.distance, 4)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="e", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="r", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="n", output_tokens=["n"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["e"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="s", output_tokens=["s"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="t", output_tokens=["t", "e", "r"], add_to_left=False)
        expected_alignment_result.merge_none_tokens()
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_7(self):
        """
        """
        result = self.calculator.get_distance('werewolf', 'were  wolf')
        self.assertEqual(result.distance, 2)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="w", output_tokens=["w"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["e"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="r", output_tokens=["r"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["e", " ", " "], add_to_left=False)
        expected_alignment_result.add_token(ref_token="w", output_tokens=["w"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="o", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="l", output_tokens=["l"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="f", output_tokens=["f"], add_to_left=False)
        expected_alignment_result.merge_none_tokens()
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_8(self):
        """
        """
        result = self.calculator.get_distance('jijizhazha', 'hahahaaaa???')
        self.assertEqual(result.distance, 10)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="j", output_tokens=[], add_to_left=False)
        expected_alignment_result.add_token(ref_token="i", output_tokens=["h"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="j", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="i", output_tokens=["h"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="z", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="h", output_tokens=["h"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="z", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="h", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["a", "?", "?", "?"], add_to_left=False)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_9(self):
        """
        """
        result = self.calculator.get_distance('helloa a a ?', 'HHHHHHHoooooo')
        self.assertEqual(result.distance, 12)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="h", output_tokens=["H", "H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="l", output_tokens=["H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="l", output_tokens=["H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="o", output_tokens=["H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["H"], add_to_left=False)
        expected_alignment_result.add_token(ref_token=" ", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token=" ", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token=" ", output_tokens=["o"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="?", output_tokens=["o"], add_to_left=False)
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)

    def test_10(self):
        """
        """
        result = self.calculator.get_distance('happyeveryday', 'happybirthday')
        self.assertEqual(result.distance, 5)
        expected_alignment_result = AlignmentResult()
        expected_alignment_result.add_token(ref_token="h", output_tokens=["h"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="p", output_tokens=["p"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="p", output_tokens=["p"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="y", output_tokens=["y"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["b"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="v", output_tokens=["i"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="e", output_tokens=["r"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="r", output_tokens=["t"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="y", output_tokens=["h"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="d", output_tokens=["d"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="a", output_tokens=["a"], add_to_left=False)
        expected_alignment_result.add_token(ref_token="y", output_tokens=["y"], add_to_left=False)
        distance, substitution, insertion, deletion = expected_alignment_result.calculate_three_kinds_of_distance()
        print(distance, substitution, insertion, deletion)
        print(result.alignment_result)
        print(expected_alignment_result)
        self.assertEqual(result.alignment_result, expected_alignment_result)


if __name__ == '__main__':
    unittest.main()
