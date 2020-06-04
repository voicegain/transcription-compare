from enum import Enum
import inflect
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
import csv
p = inflect.engine()
st = SnowballStemmer(language="english")
# lemmatizer = WordNetLemmatizer()
# verb = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
# print("deposed" in verb)
print('daryl', st.stem('daryl'), st.stem('darrel'))
print('daryl', st.stem('daryl'), st.stem('darryl'))
print('gerry', st.stem('gerry'), st.stem('gary'))
print('les', st.stem('les'), st.stem('less'))
print('marylin', st.stem('marylin'), st.stem('maryland'))
# print("daniel's", st.stem("daniel is"), st.stem("daniel's"))
# print("men :", lemmatizer.lemmatize("men", pos='v'))
# print("man :", lemmatizer.lemmatize("man", pos='v'))
# print("tests :", lemmatizer.lemmatize("tests", pos='v'))
# print("nebuchadnezzars's :", lemmatizer.lemmatize("	nebuchadnezzars's", pos='v'))

# to do : double error


class ErrorType(Enum):
    NUMBER = 1
    DOUBLE = 2
    SPLIT = 3
    is_both_name = 4
    is_reference_name = 5
    SAME_MEANING = 6
    SAME_STEM_OTHER = 7
    UNKNOWN = 8


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


def is_split(aligned_token):
    if "".join(aligned_token.outputs) == aligned_token.reference:
        return ErrorType.SPLIT
    return None


def get_name_files(i):
    csv_file = open(i, "r")
    reader = csv.reader(csv_file)
    result = []
    for item in reader:
        result.append(item[0].lower())
        # break
    csv_file.close()
    return result


filter_female_first_names = get_name_files('filter_female_first_names.csv')
filter_male_first_names = get_name_files('filter_male_first_names.csv')
filter_all_names = get_name_files('filter_all_names.csv')

print(filter_female_first_names[:5])


# def search_in_word_net(item):
#     result = wn.synsets(item)
#     if len(result) == 1:
#         for i in result:
#             if "noun.person" == i.lexname():
#                 return True
#     return False


def check_is_name(string):
    if string in filter_female_first_names:
        return True
    elif string in filter_male_first_names:
        return True
    elif string in filter_all_names:
        return True
    # elif search_in_word_net(string):
    #     return True
    else:
        return False


def is_name(aligned_token):
    reference = check_is_name(aligned_token.reference)
    if reference:
        outputs = check_is_name(aligned_token.outputs[0])
        if outputs:
            return ErrorType.is_both_name
        else:
            return ErrorType.is_reference_name


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


def is_same_stem(aligned_token):
    """
    ???? Something weird like hop hope hopeful. I think it is wrong...
    :param aligned_token:
    :return:
    """
    if st.stem(aligned_token.reference) == st.stem(aligned_token.outputs[0]):
        return ErrorType.SAME_STEM_OTHER
    return None


classifier_list_one = [is_number, is_same_meaning, is_name,
                       is_same_stem]


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


