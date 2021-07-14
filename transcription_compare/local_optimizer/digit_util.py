import re
import inflect
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import WordTokenizer
from transcription_compare.utils import SimpleReferenceCombinationGenerator
from .local_optimizer import LocalOptimizer
from nltk.stem.snowball import SnowballStemmer
keywords_stemmer = SnowballStemmer("english")

class DigitUtil(LocalOptimizer):
    def __init__(self, process_output_digit=True, only_exact_match=False):
        self.p = inflect.engine()
        self.process_output_digit = process_output_digit
        self.only_exact_match = only_exact_match

    def number_to_word(self, num, ordinal=False):
        words = set()
        words.add(self.p.number_to_words(num))
        words.add(self.p.number_to_words(num, group=1))
        words.add(self.p.number_to_words(num, group=2))
        words.add(self.p.number_to_words(num, group=3))
        if ordinal:
            try:
                words.add(self.p.number_to_words(self.p.ordinal(num)))
            except:
                pass
        words.add(self.p.number_to_words(num, group=1, zero='oh'))
        words.add(self.p.number_to_words(num, group=2, zero='oh'))
        words.add(self.p.number_to_words(num, group=3, zero='oh'))
        return set(words)

    def century(self, number):
        if number[1:-1] == '000':
            result = self.p.number_to_words(number)
        else:
            result = self.p.number_to_words(number, group=2)
        if result[-1] != 'y':
            result += 's'
        else:
            result = result[:-1] + 'ies'

        result = [result]
        for index, x in enumerate(result):
            if x.find(",") >= 1:
                result[index] = result[index].replace(",", "")
        return set(result)

    def our_is_digit(self, input_string):
        """
        Check whether the input string contain digits
        :param input_string:
        :return:
        A list of set. One element from each set should be pick to create output string

        """
        # TODO: need some improvement
        number = re.findall(r'\d+', input_string)
        #     if if_number_inside(input_string) is True:
        if len(number) > 0:
            if input_string.replace(',', '').isdigit() is True:
                # After removing , it's digit
                return [self.number_to_word(input_string)], 1

            elif len(number[0])+2 == len(input_string)\
                    and (input_string[-3:] in {'1st', '2nd', '3rd'} or (input_string[-2:] == 'th')):
                # 1st, 2nd, 3rd, 4th ...
                return [self.number_to_word(input_string, ordinal=True)], 1

            elif len(number[0])+1 == len(input_string) and input_string[-1] == 's':
                return [self.century(input_string)], 1

            else:
                # ???
                string = re.findall(r'[0-9.]+|[a-zA-Z]+', input_string)
                result = []
                c = 0
                for character in string:
                    if character.replace(".", "", 1).isdigit() is False:
                        result.append({character})
                    else:
                        c += 1
                        result.append(self.number_to_word(character))
            return result, c
        else:
            return [], 0

    def update_alignment_result_error_section(self, alignment_result_error_section):
        alignment_result = alignment_result_error_section.original_alignment_result

        update_result = self.update_alignment_result(alignment_result, False)
        if update_result is not None:
            alignment_result = update_result

        if self.process_output_digit:
            update_result = self.update_alignment_result(alignment_result, True)
            if update_result is not None:
                alignment_result = update_result

        return alignment_result

    def update_alignment_result(self, alignment_result, process_output_digit):

        word_tokenizer = WordTokenizer()

        calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=None,
            get_alignment_result=False
        )

        # get output token list
        output_token_list = alignment_result.get_outputs()
        reference_token_list = alignment_result.get_reference()

        old_distance = alignment_result.calculate_three_kinds_of_distance()[0]

        generator = SimpleReferenceCombinationGenerator()

        tmp_result = None
        no_digit = True

        if process_output_digit:
            token_list_to_check_digit = output_token_list
            token_list_not_check_digit = reference_token_list
        else:
            token_list_to_check_digit = reference_token_list
            token_list_not_check_digit = output_token_list
        # token_list_to_check_digit = reference_token_list

        digits_count = 0
        for current_str in token_list_to_check_digit:

            result_digit, c = self.our_is_digit(current_str)
            digits_count += c
            if result_digit:

                no_digit = False
                for r in result_digit:
                    # tokenize the string
                    tokenized_r = []
                    for option in r:
                        tokenized_r.append(word_tokenizer.tokenize(option, to_lower=True, remove_punctuation=True))

                    generator.add_new_token_options(tokenized_r)
            else:
                generator.add_new_token_options([current_str])

        if no_digit:
            return None

        for x in generator.get_all_reference():

            expected_new_distance = 0
            if self.only_exact_match:
                expected_distance_dec = digits_count + min(
                    (len(x) - len(token_list_to_check_digit)), 
                    max(0, len(token_list_not_check_digit) - len(token_list_to_check_digit))
                )
                expected_new_distance = old_distance - expected_distance_dec

                if expected_new_distance < 0:
                    continue

            if process_output_digit:
                distance = calculator.get_result_from_list(
                    reference_token_list, x
                ).distance
            else:
                distance = calculator.get_result_from_list(
                    x, output_token_list
                ).distance

            if self.only_exact_match:
                if distance == expected_new_distance:
                    tmp_result = x
                    break
            else:
                if distance < old_distance:
                    old_distance = distance
                    tmp_result = x

        if tmp_result is None:
            return None

        calculator2 = UKKLevenshteinDistanceCalculator(
            tokenizer=None,
            get_alignment_result=True
        )
        if process_output_digit:
            update_result = calculator2.get_result_from_list(
                reference_token_list, tmp_result).alignment_result
        else:
            update_result = calculator2.get_result_from_list(
                tmp_result, output_token_list).alignment_result
        return update_result
