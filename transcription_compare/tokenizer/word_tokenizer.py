from .abstract_tokenizer import AbstractTokenizer
from nltk.tokenize import word_tokenize
from ..tokens import Token
import re
# brackets_allowed = ['[', ']', ')', ">", '(', "<"]


class WordTokenizer(AbstractTokenizer):

    def tokenize(self, token_string, brackets_list, to_lower=False, remove_punctuation=False):
        """
        :param brackets_list,
        :param token_string:
        :param to_lower: false means we don't need to make the input_string lowercase
        :param remove_punctuation: false means we don't need to remove all the punctuation
        :return:split token_string
        """

        def clean_words_dont_have_brackets(s):
            # do punctuation or lower
            # print('exclude_brackets_word', s)
            s = s.strip()
            if remove_punctuation:
                punctuation = r"""!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
                s = s.translate(str.maketrans('', '', punctuation))
            if to_lower:
                s = s.lower()
            s = s.replace(" '", "'")
            s = word_tokenize(s)
            return [(t, False) for t in s]

        def having_brackets_word(s):
            # print('having_brackets_word', s)
            return [(s, True)]

        if len(brackets_list) != 0:
            brackets_allowed = ''
            # print('brackets_list', brackets_list)
            for i, b in enumerate(brackets_list):

                brackets_allowed += r'\{}(.*?)\{}'.format(b[0], b[-1])
                # print('brackets_allowed', brackets_allowed)
                if i != len(brackets_list)-1:
                    brackets_allowed += '|'
                    # r'\((.*?)\)|\[(.*?)\]|\<(.*?)\>'



            # if len(brackets_list) == 0:
            #     return token_string.split()

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
        for i in merged_list:
            # print('i', i)
            if len(i) == 1:
                token_list.append(i["w"])
            else:
                token_list.append(Token(i["w"], prefix=i.get("pre"), postfix=i.get("post")))
        # print('token_list', token_list)
        return token_list
