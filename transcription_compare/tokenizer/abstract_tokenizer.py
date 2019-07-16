from abc import ABC, abstractmethod
from typing import List


class AbstractTokenizer(ABC):

    @abstractmethod
    def tokenize(self, token_string: str) -> List:
        pass
