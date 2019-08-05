from .local_optimizer import LocalOptimizer
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer


class LocalCerOptimizer(LocalOptimizer):
    def __init__(self):
        pass

    def update_alignment_result_error_section(self, alignment_result_error_section):
        # print('hahahahahahah')
        alignment_result_options = alignment_result_error_section.get_all_options()
        # print('alignment_result_options', alignment_result_options)
        if alignment_result_options is None:
            return None

        calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=CharacterTokenizer(),
            get_alignment_result=False
        )

        old_distance = alignment_result_error_section.original_alignment_result.get_total_cer(calculator)
        # print('old_distance', old_distance)
        tmp_result = None
        for alignment_result_option in alignment_result_options:
            d = alignment_result_option.get_total_cer(calculator)
            # print('d', d)
            if d < old_distance:
                old_distance = d
                tmp_result = alignment_result_option
        # print('tmp_result', tmp_result)
        return tmp_result
