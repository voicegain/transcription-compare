from abc import ABC, abstractmethod
from ..results import Result
from ..tokenizer import AbstractTokenizer
from typing import List


class AbstractLevenshteinDistanceCalculator(ABC):

    def __init__(self, tokenizer: AbstractTokenizer, get_alignment_result: bool = False):
        self.tokenizer = tokenizer
        self.get_alignment_result = get_alignment_result

    def get_distance(self, ref_tokens: str, output_tokens: str, brackets_list: list = [],
                     to_lower: bool = False,
                     remove_punctuation: bool = False, use_alternative_spelling: bool = False) -> Result:

        return self.get_result_from_list(
            self.tokenizer.tokenize(ref_tokens, brackets_list, to_lower, remove_punctuation, use_alternative_spelling),
            self.tokenizer.tokenize(output_tokens, brackets_list, to_lower, remove_punctuation, use_alternative_spelling)
        )

    @abstractmethod
    def get_result_from_list(self, ref_tokens_list: List,
                             output_tokens_list: List) -> Result:
        pass
