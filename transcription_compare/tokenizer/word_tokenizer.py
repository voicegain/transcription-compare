from .abstract_tokenizer import AbstractTokenizer


class WordTokenizer(AbstractTokenizer):

    def tokenize(self, token_string):
        return token_string.split()
