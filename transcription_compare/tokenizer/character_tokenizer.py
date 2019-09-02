from .abstract_tokenizer import AbstractTokenizer
import string


class CharacterTokenizer(AbstractTokenizer):

    def tokenize(self, token_string, brackets_list, to_lower=False, remove_punctuation=False):
        """
        :param brackets_list,
        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase.
        :param remove_punctuation: false means we don't need to remove all the punctuation.
        :return:split token_string
        """

        if remove_punctuation is True:
            token_string = token_string.translate(str.maketrans('', '', string.punctuation))

        if to_lower is True:
            token_string = token_string.lower()
        # print('list(token_string)', len(list(token_string)))
        return list(token_string)
