import inflect
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.results import AlignmentResult
from transcription_compare.utils import SimpleReferenceCombinationGenerator
from transcription_compare.utils.digit_util import DigitUtil
# digit_util = DigitUtil()


def update_alignment_result(alignment_result):
    #   alignment_result = result.alignment_result
    aligned_tokens_list = alignment_result.aligned_tokens_list

    calculator = UKKLevenshteinDistanceCalculator(
                tokenizer=WordTokenizer(),
                get_alignment_result=False
            )
    output_string = alignment_result.get_outputs_str()
    old_distance = alignment_result.calculate_three_kinds_of_distance()[0]
    generator = SimpleReferenceCombinationGenerator()
    tmp_result = None
    for index in range(0, len(alignment_result)):
        # if aligned_tokens_list[index].reference.isdigit() is True:
        result_digit = our_is_digit(aligned_tokens_list[index].reference)
        if result_digit is not False:
            for r in result_digit:
                generator.add_new_token_options(r)
        else:
            generator.add_new_token_options(aligned_tokens_list[index].reference)
        # print('generator.get_all_reference()', generator.get_all_reference())
        for x in generator.get_all_reference():
            x = " ".join(x)
            distance = calculator.get_distance(x, output_string).distance
            # print('x', x)
            # print('output_string', output_string)
            # print('distance', distance)

            if distance < old_distance:
                old_distance = distance
                tmp_result = x
    if tmp_result is None:
        return None
    calculator2 = UKKLevenshteinDistanceCalculator(
        tokenizer=WordTokenizer(),
        get_alignment_result=True
    )
    update_result = calculator2.get_distance(tmp_result, output_string).alignment_result
    return update_result




p = inflect.engine()

alignment_result = AlignmentResult()

alignment_result.add_token(ref_token="w", output_tokens=["w"], add_to_left=False)
alignment_result.add_token(ref_token="5", output_tokens=["e"], add_to_left=False)
alignment_result.add_token(ref_token="r", output_tokens=["r"], add_to_left=False)
alignment_result.add_token(ref_token="g", output_tokens=[], add_to_left=False)
alignment_result.add_token(ref_token="2", output_tokens=[], add_to_left=False)
alignment_result.add_token("1", ["one"])

alignment_result.add_token("21", ["twenty-one", 'a', 'c'], add_to_left=False)

alignment_result.add_token("312", ["three", "one", "two"], add_to_left=False)
alignment_result.add_token(ref_token="e", output_tokens=["e", " ", " "], add_to_left=False)
alignment_result.add_token(ref_token="w", output_tokens=["w"], add_to_left=False)
alignment_result.add_token(ref_token="7", output_tokens=["o"], add_to_left=False)
alignment_result.add_token("1990s", ['nineteen', 'nineties'], add_to_left=False)

alignment_result.add_token("10,000", ["ten", "thousand"], add_to_left=False)
alignment_result.add_token("H2o2", ['H', 'two', 'o', 'two'], add_to_left=False)
alignment_result.add_token(ref_token="l", output_tokens=["l"], add_to_left=False)
alignment_result.add_token(ref_token="f", output_tokens=["f"], add_to_left=False)
print(alignment_result)
error_list = alignment_result.get_error_section_list()
for e in error_list:
    print("+++++++++++++++")
    print(e.original_alignment_result)
    # updated_alignment_result = update_alignment_result(e.original_alignment_result)
    updated_alignment_result = update_alignment_result(e.original_alignment_result)
    e.set_correction(updated_alignment_result)

alignment_result.apply_error_section_list(error_list)

print(alignment_result)

# for aligned_token in error_list:
#     print(aligned_token.reference)


# print(error_list.get_reference())
#aligned_tokens = alignment_result.aligned_tokens_list
#aligned_tokens = error_list.alignment_result_error_section_list
#print('list', aligned_tokens)

