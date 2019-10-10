# from metaphone import doublemetaphone
# import jellyfish
#
#
# print(type(doublemetaphone("architect")))
# print(doublemetaphone("apple"))
#
# print(doublemetaphone("daryl"), doublemetaphone("darrel"))
# print(doublemetaphone("daryl"), doublemetaphone("darryl"))
# print(doublemetaphone("gerry"), doublemetaphone("gary"))
# print(doublemetaphone("daniel"), doublemetaphone("tane"))
# print(doublemetaphone("daniel"), doublemetaphone("tenniel"))
# print(doublemetaphone("cindy"), doublemetaphone("sindy"))
# print(doublemetaphone("awana"), doublemetaphone("wana"))
# print(doublemetaphone("les"), doublemetaphone("less"))
# print(doublemetaphone("marylin"), doublemetaphone("maryland"))
#
#
# print("MRA")
# print(jellyfish.match_rating_comparison('daryl', 'darrel'))
# print(jellyfish.match_rating_comparison('daryl', 'darryl'))
# print(jellyfish.match_rating_comparison('gerry', 'gary'))
# print(jellyfish.match_rating_comparison('daniel', 'tane'))
# print(jellyfish.match_rating_comparison('daniel', 'tenniel'))
# print(jellyfish.match_rating_comparison('cindy', 'sindy'))
# print(jellyfish.match_rating_comparison('awana', 'wana'))
# print(jellyfish.match_rating_comparison('les', 'less'))
# print(jellyfish.match_rating_comparison('marylin', 'maryland'))
#
# print(jellyfish.match_rating_comparison('be', 'is'))
#
# print('jellyfish.match_rating_codex')
# print(jellyfish.match_rating_codex('daryl'), jellyfish.match_rating_codex('darryl'))
# print(jellyfish.match_rating_codex('daryl'), jellyfish.match_rating_codex('darryl'))
# print(jellyfish.match_rating_codex('gerry'), jellyfish.match_rating_codex('gary'))
# print(jellyfish.match_rating_codex('daniel'), jellyfish.match_rating_codex('tane'))
# print(jellyfish.match_rating_codex('cindy'), jellyfish.match_rating_codex('sindy'))
# print(jellyfish.match_rating_codex('awana'), jellyfish.match_rating_codex('wana'))
# print(jellyfish.match_rating_codex('les'), jellyfish.match_rating_codex('less'))
# print(jellyfish.match_rating_codex('marylin'), jellyfish.match_rating_codex('maryland'))
#
# print('not names')
# print(jellyfish.match_rating_comparison('enriched', 'enrich'))
# print(jellyfish.match_rating_comparison('tonight  ', 'to night '))
# print(jellyfish.match_rating_comparison("daniel's", 'daniel is'))
# print(jellyfish.match_rating_comparison('oh  ', 'o '))
# print(jellyfish.match_rating_comparison('lords', 'lord'))
# print(jellyfish.match_rating_comparison("nebuchadnezzar's", "nebuchadnezzars's"))
# print(jellyfish.match_rating_comparison("i've", 'ive'))
# print(jellyfish.match_rating_comparison('eighteen  ', 'eighteenth '))
# print(jellyfish.match_rating_comparison("Incredible", 'credible'))
# print(jellyfish.match_rating_comparison("I’m", 'I am '))
# print('DM')
# print(doublemetaphone("enriched"), doublemetaphone("enrich"))
# print(doublemetaphone("tonight"), doublemetaphone("to night"))
# print(doublemetaphone("daniel's"), doublemetaphone("daniel is"))
# print(doublemetaphone("oh"), doublemetaphone("o"))
# print(doublemetaphone("lords"), doublemetaphone("lord"))
# print(doublemetaphone("nebuchadnezzar's"), doublemetaphone("nebuchadnezzars's"))
# print(doublemetaphone("i've"), doublemetaphone("ive"))
# print(doublemetaphone("eighteen"), doublemetaphone("eighteenth"))
# print(doublemetaphone("Incredible"), doublemetaphone("credible"))
# print(doublemetaphone("I’m"), doublemetaphone("I am"))
#
# print('they are not same at all')
# print(jellyfish.match_rating_comparison('amen', 'and then'))
# print(jellyfish.match_rating_comparison('amen', 'a an men'))
# print(jellyfish.match_rating_comparison("in", 'yeah'))
# print(jellyfish.match_rating_comparison('us  ', 'so '))
# print(jellyfish.match_rating_comparison("nebuchadnezzar's", ""))
#
# print('DM')
# print(doublemetaphone("amen"), doublemetaphone("and then"))
# print(doublemetaphone("amen"), doublemetaphone("a an men"))
# print(doublemetaphone("in"), doublemetaphone("yeah"))
# print(doublemetaphone("us"), doublemetaphone("so"))
# print(doublemetaphone("nebuchadnezzar's"), doublemetaphone(" "))

from nltk.tokenize import word_tokenize
import re

token_string = 'in to'

remove_punctuation = True
to_lower = True
brackets_list = []
brackets_allowed = ''
print('brackets_list', brackets_list)

def exclude_brackets_word(s):
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
    for i, b in enumerate(brackets_list):

        brackets_allowed += r'\{}(.*?)\{}'.format(b[0], b[-1])
        # print('brackets_allowed', brackets_allowed)
        if i != len(brackets_list)-1:
            brackets_allowed += '|'
            # r'\((.*?)\)|\[(.*?)\]|\<(.*?)\>'
    print('brackets_allowed', brackets_allowed)


    # if len(brackets_list) == 0:
    #     return token_string.split()

    list_s = []
    count = 0
    # for i in re.finditer(r"[{}()<>\[\]]+", case):  # 先看看有没有{}()<>，如果有，分割
    # print('find', re.finditer(brackets_allowed, token_string))
    for i in re.finditer(brackets_allowed, token_string):
        print('find',i.span())
        if i.span()[0] != 0:
            list_s += exclude_brackets_word(token_string[count:i.span()[0]])  # 有些string第一个不是符号呀
        list_s += having_brackets_word(token_string[i.span()[0]:i.span()[1]])
        count = i.span()[1]
    print(list_s)
    if count != len(token_string):  # 1 上面的for剩下的没有[]的最后部分 2 string本身没有[]的呀。
        # print(s[count:])
        g = token_string[count:]
        list_s += exclude_brackets_word(g)
    print(list_s)
else:
    list_s = exclude_brackets_word(token_string)
    print(list_s)

print('......')

for i in re.finditer('', 'abc'):
    print('find',i.span())
