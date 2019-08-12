from enum import Enum
import string
import inflect
from nltk.stem import SnowballStemmer
from word2number import w2n
from nltk.stem import WordNetLemmatizer
# from pattern.en import referenced
import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn

p = inflect.engine()
st = SnowballStemmer(language="english")
lemmatizer = WordNetLemmatizer()
# verb = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
# print("deposed" in verb)
# print('eighteen', st.stem('eighteen'), st.stem('eighteenth'))
# print('five', st.stem('five'), st.stem('fifth'))
print('hope', st.stem('hope'), st.stem('hopeful'))
# print('asking', st.stem('asking'), st.stem('asking'))
# print("daniel's", st.stem("daniel is"), st.stem("daniel's"))
# print("men :", lemmatizer.lemmatize("men", pos='v'))
# print("man :", lemmatizer.lemmatize("man", pos='v'))
# print("tests :", lemmatizer.lemmatize("tests", pos='v'))
# print("nebuchadnezzars's :", lemmatizer.lemmatize("	nebuchadnezzars's", pos='v'))

# to do : double error


class ErrorType(Enum):
    APOSTROPHE = 1
    DOUBLE = 2
    SPLIT = 3
    NUMBER = 4
    SAME_STEM_OTHER = 5
    SAME_MEANING = 6
    POSSESSIVE = 7
    NAME = 8
    VERB_TENSE = 9
    PLURAL = 10
    UNKNOWN = 11


def is_apostrophe(aligned_token):
    """
    We remove all apostrophes from the string and compare
    :param aligned_token:
    :return:
    """
    if aligned_token.outputs[0].replace("'", "") == aligned_token.reference.replace("'", ""):
        return ErrorType.APOSTROPHE
    return None


def is_double(aligned_token):
    """
    TODO : some cases have multiple word doubles, e.g. "have to have to" ??????
    :param aligned_token: the output has to be >= 2
    :return:
    """
    outputs_set = set(aligned_token.outputs)

    if len(outputs_set) == 1:
        output = outputs_set.pop()
        if output == aligned_token.reference:
            return ErrorType.DOUBLE
    return None


def is_number(aligned_token):
    """
    ??????????????????????????????????????
    here only support th....!!???!!!!en
    there is not a package that can be directly used to convert ordinal number to word
    to do. probabily will use number2word unless know how to use infelct
    # TODO: th
    :param aligned_token: the output is ordinary
    :return:
    """
    if aligned_token.outputs[0][-2:] == "th":
        if aligned_token.outputs[0][:-2] == aligned_token.reference:
            return ErrorType.NUMBER
    # if w2n.word_to_num(st.stem(aligned_token.reference)) == w2n.word_to_num(st.stem(aligned_token.outputs)):
    #     return ErrorType.NUMBER
    return None


def is_same_stem(aligned_token):
    """
    ???? Something weird like hop hope hopeful. I think it is wrong...
    :param aligned_token:
    :return:
    """
    if st.stem(aligned_token.reference) == st.stem(aligned_token.outputs[0]):
        return ErrorType.SAME_STEM_OTHER
    return None


def is_same_meaning(aligned_token):
    """
    TODO: we will load the same meaning dictionary from a file
    :param aligned_token:
    :return:
    """
    reference_outputs = {"oh": ["o"], "ante": ["anti"], "gonna": ["going", "to"], "alright": ["all", "right"]}
    if aligned_token.reference.replace("'s", "") == aligned_token.outputs[0] and aligned_token.outputs[1] == "is" :
        return ErrorType.SAME_MEANING
    if aligned_token.reference in reference_outputs.keys():
        if reference_outputs[aligned_token.reference] == aligned_token.outputs:
            return ErrorType.SAME_MEANING
    return None


def is_split(aligned_token):
    if "".join(aligned_token.outputs) == aligned_token.reference:
        return ErrorType.SPLIT
    return None


def is_possessive(aligned_token):
    if aligned_token.reference+aligned_token.outputs[0][aligned_token.outputs[0].find("'"):] == aligned_token.outputs[0]:
    # if aligned_token.outputs[0].replace("'s", "") == aligned_token.reference.replace("'s", ""):
        return ErrorType.POSSESSIVE
    return None


def is_name(aligned_token):
    pass


def is_not_stem_verb_tense(aligned_token):
    if lemmatizer.lemmatize(aligned_token.reference, pos='v') == lemmatizer.lemmatize(aligned_token.outputs[0], pos='v'):
        return ErrorType.VERB_TENSE


def is_plural(aligned_token):
    """
    It should be noted that two distinct singular words
    which happen to take the same plural form are not considered equal,
    nor are cases where one (singular) word's plural is the other (plural) word's singular.
    -----
    can only compare singular and plural respectively
    :param aligned_token:
    :return:
    """
    if aligned_token.outputs[0][aligned_token.outputs[0].find("'"):] == \
            aligned_token.reference[aligned_token.reference.find("'"):]:
            aligned_token.reference = aligned_token.reference.replace("'s", "")
            aligned_token.outputs[0] = aligned_token.outputs[0].replace("'s", "")
            print("both have 's")
    # else:
    #     reference = aligned_token.reference
    #     output = aligned_token.outputs[0]
    print(aligned_token.outputs[0], aligned_token.reference)
    print(p.compare(aligned_token.outputs[0], aligned_token.reference))
    if p.compare(aligned_token.outputs[0], aligned_token.reference) is not False:
        if p.compare(aligned_token.outputs[0], aligned_token.reference) != "p:p":
            return ErrorType.PLURAL
        return None
    return None


classifier_list_one = [is_apostrophe, is_number, is_plural, is_same_meaning,
                       is_possessive, is_name, is_not_stem_verb_tense, is_same_stem]
# plural need to be in front of the is_same_stem

classifier_list_two = [is_double, is_same_meaning, is_split]


def error_type_classify(aligned_token):
    """
    len(aligned_token.outputs must be >= 1
    :param aligned_token:
    :return:
    """
    if len(aligned_token.outputs) == 1:
        for classifier in classifier_list_one:
            result = classifier(aligned_token)
            if result is not None:
                return result
    else:
        for classifier in classifier_list_two:
            result = classifier(aligned_token)
            if result is not None:
                return result

    return ErrorType.UNKNOWN


