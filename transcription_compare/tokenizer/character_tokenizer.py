from .abstract_tokenizer import AbstractTokenizer
import string


class CharacterTokenizer(AbstractTokenizer):

    def tokenize(self, token_string, to_lower=False, remove_punctuation=False):
        """

        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase.
        :param remove_punctuation: false means we don't need to remove all the punctuation.
        :return:split token_string
        """

        if remove_punctuation is True:
            token_string = token_string.translate(str.maketrans('', '', string.punctuation))

        if to_lower is True:
            token_string = token_string.lower()

        return list(token_string)
