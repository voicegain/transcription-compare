from .abstract_tokenizer import AbstractTokenizer
from nltk.tokenize import word_tokenize
from ..tokens import Token
import re
# brackets_allowed = ['[', ']', ')', ">", '(', "<"]

FILL_WORD_LIST = ["um"]

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
pun = "'"
allow_character = digits + ascii_letters + whitespace + pun


class WordTokenizer(AbstractTokenizer):

    def tokenize(self, token_string, brackets_list=None, to_lower=False, remove_punctuation=False, use_alternative_spelling=False):
        """
        :param brackets_list,
        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase
        :param remove_punctuation: false means we don't need to remove all the punctuation
        :param use_alternative_spelling: True means we won't count different English version errors.
        :return:split token_string
        """

        def clean_words_dont_have_brackets(s):
            # do punctuation or lower
            # print('exclude_brackets_word', s)
            s = s.strip()
            if remove_punctuation:
                # punctuation = r"""!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
                # s = s.translate(str.maketrans('', '', punctuation))
                new_s = ''
                for one_character in s:
                    if one_character in allow_character:
                        new_s += one_character
                    else:
                        new_s += " "
                s = new_s
            if to_lower:
                s = s.lower()
            s = s.replace(" '", "'")
            s = s.split()
            return [(t, False) for t in s]

        def having_brackets_word(s):
            # print('having_brackets_word', s)
            return [(s, True)]

        if brackets_list:
            brackets_allowed = ''
            # print('brackets_list', brackets_list)
            for i, b in enumerate(brackets_list):

                brackets_allowed += r'\{}(.*?)\{}'.format(b[0], b[-1])
                # print('brackets_allowed', brackets_allowed)
                if i != len(brackets_list)-1:
                    brackets_allowed += '|'
                    # r'\((.*?)\)|\[(.*?)\]|\<(.*?)\>'

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
            if token[1] is True:
                if len(merged_list) == 0:
                    head_pre_list.append(token[0])
                else:
                    last_merged_token = merged_list[-1]
                    if "post" in last_merged_token:
                        last_merged_token["post"].append(token[0])
                    else:
                        last_merged_token["post"] = [token[0]]
            else:
                merged_list.append({"w": token[0]})

        if (len(merged_list) > 0) and (len(head_pre_list) > 0):
            merged_list[0]["pre"] = head_pre_list

        token_list = []

        new_merged_list = []
        for index, word in enumerate(merged_list):
            #
            # if index == 0:
            #     if word["w"] in FILL_WORD_LIST:
            #         merged_list[index + 1]["pre"] = [word["w"]]

            if word["w"] in FILL_WORD_LIST:
                if index != 0:
                    # print('post', merged_list[index - 1], merged_list[index])
                    if "post" in new_merged_list[-1].keys():

                        new_merged_list[-1]["post"] += [word["w"]]

                    else:
                        new_merged_list[-1]["post"] = [word["w"]]

                    # if len(merged_list[index - 1]["post"]) != 0:

                    # print('post', merged_list[index - 1]["post"])
                    # print('post', type(merged_list[index - 1]["post"]))
                else:
                    if index == len(merged_list) - 1:
                        new_merged_list.append(word)
                    else:
                        merged_list[index + 1]["pre"] = [word["w"]]

            else:
                new_merged_list.append(word)

        # print('new_merged_list', new_merged_list)
        for i in new_merged_list:
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
