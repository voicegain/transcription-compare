from .abstract_tokenizer import AbstractTokenizer
from nltk.tokenize import word_tokenize


class WordTokenizer(AbstractTokenizer):

    def tokenize(self, token_string, to_lower=False, remove_punctuation=False):
        """

        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase
        :param remove_punctuation: false means we don't need to remove all the punctuation
        :return:split token_string
        """
        if remove_punctuation is True:
            punctuation = r"""!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
            token_string = token_string.translate(str.maketrans('', '', punctuation))

        if to_lower is True:
            token_string = token_string.lower()
        # print('token_string.split()',len(token_string.split()))
        # return token_string.split()
        return word_tokenize(token_string)