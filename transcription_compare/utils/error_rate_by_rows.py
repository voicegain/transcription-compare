import inflect
p = inflect.engine()
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.utils import SimpleReferenceCombinationGenerator

from transcription_compare.results import AlignmentResult
alignment_result = AlignmentResult()
alignment_result.add_token(ref_token=None, output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["3"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["4"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["5"], add_to_left=False)
alignment_result.add_token(ref_token="ha", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token="two", output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token="2", output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
alignment_result.add_token(ref_token="two", output_tokens=["two"], add_to_left=False)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["some", "day"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
# alignment_result.add_token(ref_token="one", output_tokens=["one", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["la", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["xi"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["ays"], add_to_left=False)
alignment_result.merge_none_tokens()
print('alignment_result', alignment_result)
print('!!!!!!!!!!!!!!')

#  get each rows
#  match?
#  not --> check which one
# incorrect -
correct_count = 0
delete_count = 0
incorrect = 0
split_error = 0
total_count = len(alignment_result)
for rows in alignment_result:
    total_count += 1
    if len(rows.outputs) == 1:
        # correct
        if rows.reference == rows.outputs[0]:
            correct_count += 1
        else:
            # incorrect
            incorrect += 1

    elif len(rows.outputs) == 0:
        delete_count += 1
        # incorrect
        incorrect += 1
    else:
        if "".join(rows.outputs) == rows.reference:
            print('r', rows.reference)
            print('o', rows.outputs)
            split_error += 1
    #  more if to check

# 根据len 进入不同的error_type


def error_type_one_word(new_aligned_token_list):
    """
    单复数， 动词，  inflect
    :param new_aligned_token_list: len == 1
    :return:
    """
    for token in new_aligned_token_list:
        if token.reference:
            pass


def error_type_more_than_two_words(new_aligned_token_list):
    """
    splite or insetion
    :param new_aligned_token_list: len == 1
    :return:
    """
    for token in new_aligned_token_list:
        if token.reference:
            pass
