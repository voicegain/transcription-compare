
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
# from transcription_compare.utils import SimpleReferenceCombinationGenerator

from transcription_compare.results import AlignmentResult
alignment_result = AlignmentResult()
alignment_result.add_token(ref_token=None, output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["3"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["4"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["5"], add_to_left=False)
alignment_result.add_token(ref_token="ha", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["1"], add_to_left=True)
alignment_result.add_token(ref_token="2", output_tokens=["2"], add_to_left=True)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["1"], add_to_left=True)
alignment_result.add_token(ref_token="2", output_tokens=["2"], add_to_left=True)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=True)
alignment_result.add_token(ref_token="two", output_tokens=["two"], add_to_left=True)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)

alignment_result.merge_none_tokens()
print('alignment_result', alignment_result)
error_list = alignment_result.get_error_section_list()
for e in error_list:
    print('e', e.original_alignment_result)

# single
#to do get two line error section

error_list = alignment_result.get_error_section_list()

def update_alignment_result_word(alignment_result):
    # fist check same character
    for row in alignment_result:
        if row.reference in row.output:
            index = list.index(row.reference)
        else:
            index = 0
    # sort
    # return alignment_result
    pass

for e in error_list:
    if len(e) == 2:  # question we make it two lines or just check and use the two line??????????????
        updated_alignment_result = update_alignment_result_word(
            e.original_alignment_result)
    if updated_alignment_result is not None:
        # print(">>>>>>>>>>>>>not None")
        # print(updated_alignment_result)
        e.set_correction(updated_alignment_result)



#calculate cer
distance, substitution, insertion, deletion = alignment_result.calculate_three_kinds_of_distance()
#apply back
alignment_result.apply_error_section_list(error_list)




