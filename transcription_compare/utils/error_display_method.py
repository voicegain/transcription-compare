
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.results import AlignmentResult
from transcription_compare.results import AlignedToken
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
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
# alignment_result.add_token(ref_token="one", output_tokens=["one", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["la", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["xi"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["ays"], add_to_left=False)
alignment_result.merge_none_tokens()
print('alignment_result', alignment_result)


error_list = alignment_result.get_error_section_list()
for e in error_list:
    alignment_result_options = e.get_all_options()

    if alignment_result_options is None:
        continue

    calculator = UKKLevenshteinDistanceCalculator(
        tokenizer=CharacterTokenizer(),
        get_alignment_result=False
    )

    old_distance = e.original_alignment_result.get_total_cer(calculator)

    tmp_result = None
    for alignment_result_option in alignment_result_options:
        d = alignment_result_option.get_total_cer(calculator)
        if d < old_distance:
            old_distance = d
            tmp_result = alignment_result_option

    if tmp_result is None:
        continue
    e.set_correction(tmp_result)

    #  correct后的或者一开始就没有进去的都会apply back
alignment_result.apply_error_section_list(error_list)

print(alignment_result)


