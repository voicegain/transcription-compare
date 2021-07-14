from .abstract_tokenizer import AbstractTokenizer
from nltk.tokenize import word_tokenize
from .special_token_utils import *
from ..tokens import Token
import re
import string
# brackets_allowed = ['[', ']', ')', ">", '(', "<"]

FILL_WORD_LIST = {"um", "mhmm", "hmm", "uh", "huh"}

whitespace = ' \t\n\r\v\f'
ascii_letters = string.ascii_letters
digits = '0123456789'
pun = "'"
allow_character = set(digits + ascii_letters + whitespace + pun)
es_allow_character = set(digits + ascii_letters + whitespace + "ñáéíóúü")


class TokenWithPrePostFlag:
    def __init__(self, word, should_put_to_pre_post):
        self.word = word
        self.should_put_to_pre_post = should_put_to_pre_post


class WordTokenizer(AbstractTokenizer):

    def __init__(self, lang="en"):
        self.lang = lang

    def tokenize(self, token_string, brackets_list=None, to_lower=False, remove_punctuation=False, use_alternative_spelling=False):
        """
        :param brackets_list,
        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase
        :param remove_punctuation: false means we don't need to remove all the punctuation
        :param use_alternative_spelling: True means we won't count different English version errors.
        :return:split token_string
        """

        split_tokens = token_string.split()
        methods = [process_email, process_url, process_and]
        new_tokens = []
        for token in split_tokens:
            updated = False
            for method in methods:
                updated_word = method(token)
                if updated_word:
                    new_tokens.append(updated_word)
                    # print("method", method)
                    # print("updated_word", token, updated_word)
                    updated = True
                    break
            if not updated:
                new_tokens.append(token)

        token_string = " ".join(new_tokens)

        def clean_words_dont_have_brackets(s):
            # do punctuation or lower
            # print('exclude_brackets_word', s)
            s = s.strip()
            if remove_punctuation:
                # punctuation = r"""!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
                # s = s.translate(str.maketrans('', '', punctuation))
                new_s = ''
                if self.lang == "en":
                    ac = allow_character
                else:
                    ac = es_allow_character
                # todo
                # \d+.\d+
                # two_money = re.findall("\d+.\d+", text)
                for i, one_character in enumerate(s):
                    if one_character in ac:
                        new_s += one_character
                    else:
                        # keep point in digit
                        if one_character == "." and i != 0 and s[i-1] in digits and i != len(s)-1 and s[i+1] in digits:
                            new_s += one_character
                        else:
                            new_s += " "
                s = new_s
            if to_lower:
                s = s.lower()
            s = s.replace(" '", "'")
            s = s.split()

            output_list = []
            for t in s:
                if t in FILL_WORD_LIST:
                    output_list.append(TokenWithPrePostFlag(t, True))
                else:
                    output_list.append(TokenWithPrePostFlag(t, False))

            return output_list

        def having_brackets_word(s):
            # print('having_brackets_word', s)
            return [TokenWithPrePostFlag(s, True)]

        def create_regex_from_brackets_list(brackets_list):
            brackets_allowed = ''
            # print('brackets_list', brackets_list)
            for i, b in enumerate(brackets_list):

                brackets_allowed += r'\{}(.*?)\{}'.format(b[0], b[-1])
                # print('brackets_allowed', brackets_allowed)
                if i != len(brackets_list) - 1:
                    brackets_allowed += '|'
                    # r'\((.*?)\)|\[(.*?)\]|\<(.*?)\>'
            return brackets_allowed

        if brackets_list:
            brackets_allowed = create_regex_from_brackets_list(brackets_list)

            list_s = []
            count = 0
            # for i in re.finditer(r"[{}()<>\[\]]+", case):  # 先看看有没有{}()<>，如果有，分割
            # print('find', re.finditer(brackets_allowed, token_string))
            for i in re.finditer(brackets_allowed, token_string):
                # print('find',i.span())
                if i.span()[0] != 0:
                    list_s += clean_words_dont_have_brackets(token_string[count:i.span()[0]])  # 有些string第一个不是符号呀
                list_s += having_brackets_word(token_string[i.span()[0]:i.span()[1]])
                count = i.span()[1]

            if count != len(token_string):  # 1 上面的for剩下的没有[]的最后部分 2 string本身没有[]的呀。
                # print(s[count:])
                g = token_string[count:]
                list_s += clean_words_dont_have_brackets(g)

        else:
            list_s = clean_words_dont_have_brackets(token_string)
            # print(list_s)
        # print(list_s)

        head_pre_list = []
        merged_list = []

        for token in list_s:
            if token.should_put_to_pre_post is True:
                if len(merged_list) == 0:
                    head_pre_list.append(token.word)
                else:
                    last_merged_token = merged_list[-1]
                    if "post" in last_merged_token:
                        last_merged_token["post"].append(token.word)
                    else:
                        last_merged_token["post"] = [token.word]
            else:
                merged_list.append({"w": token.word})

        # If we only have tokens in head_pre_list, we will ignore them
        if (len(merged_list) > 0) and (len(head_pre_list) > 0):
            merged_list[0]["pre"] = head_pre_list
        # the merged list could be empty, if the sentence only has brackets words.

        token_list = []
        # print('new_merged_list', new_merged_list)
        for i in merged_list:
            # if len(i) == 1:
            #     token_list.append(i["w"])
            # else:
            # print(i)

            token_list.append(Token(i["w"], prefix=i.get("pre"), postfix=i.get("post"),
                                    use_alternative_spelling=use_alternative_spelling))
        # print('token_list', token_list)
        # print('token_list', token_list)
        # print('token_list type', type(token_list[0]))
        return token_list
