from abc import ABC, abstractmethod
from ..results import Result
from ..tokenizer import AbstractTokenizer
from typing import List


class AbstractLevenshteinDistanceCalculator(ABC):

    def __init__(self, tokenizer: AbstractTokenizer, get_alignment_result: bool = False):
        self.tokenizer = tokenizer
        self.get_alignment_result = get_alignment_result

    def get_distance(self, ref_tokens: str, output_tokens: str) -> Result:

        return self.get_result_from_list(
            self.tokenizer.tokenize(ref_tokens),
            self.tokenizer.tokenize(output_tokens)
        )

    @abstractmethod
    def get_result_from_list(self, ref_tokens_list: List, output_tokens_list: List) -> Result:
        pass
