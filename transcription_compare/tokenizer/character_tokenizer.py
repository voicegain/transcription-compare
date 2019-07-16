from .abstract_tokenizer import AbstractTokenizer


class CharacterTokenizer(AbstractTokenizer):

    def tokenize(self, token_string):
        return list(token_string)
