from enum import Enum
from nltk.stem import SnowballStemmer
import csv
from nltk.corpus import wordnet as wn
import inflect
import pkg_resources

filter_file_names = ['names_csv/filter_female_first_names.csv',
                     'names_csv/filter_male_first_names.csv',
                     'names_csv/filter_all_names.csv']
filter_file_name_path = []
for filter_file_names in filter_file_names:
    filter_file_name_path.append(pkg_resources.resource_filename(__name__, filter_file_names))

original_file_names = ['names_csv/female_first.csv',
                       'names_csv/male_first.csv',
                       'names_csv/all_names.csv']
original_file_name_path = []
for original_file_names in original_file_names:
    original_file_name_path.append(pkg_resources.resource_filename(__name__, original_file_names))

same_meaning_file = 'names_csv/same_meaning.csv'
same_meaning_file_path = pkg_resources.resource_filename(__name__, same_meaning_file)

be_verb = {'am': ['was'], 'is': ['was'], 'are': ['were'],
           'was': ['am', 'is'], 'were': ['are']}


class ErrorType(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, display_name):
        self.display_name = display_name

    def get_display_name(self):
        return self.display_name

    NUMBER = "number"
    DOUBLE = "double"
    SPLIT = "split"
    BE_VERB = "be"
    PLURAL = "plural"
    IS_BOTH_NAME = "both are name"
    IS_REFERENCE_NAME = "reference is name"
    SAME_MEANING = "same meaning"
    SAME_STEM_OTHER = "having same stem"
    NOT_IN_WORD_NET = "reference is a difficult word"
    UNKNOWN = "unknown"
    NA = "N/A"


class AlignedTokenClassifier:

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AlignedTokenClassifier.__instance is None:
            AlignedTokenClassifier()
        return AlignedTokenClassifier.__instance

    def __init__(self):
        if AlignedTokenClassifier.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.st = SnowballStemmer(language="english")
            self.p = inflect.engine()
            self.classifier_list_one = [
                self.is_number, self.is_be_verb, self.is_plural, self.is_same_meaning, self.is_same_stem,
                self.is_name, self.is_difficult_word
            ]
            self.classifier_list_two = [
                self.is_double, self.is_same_meaning, self.is_split
            ]
            self.filter_names = self._get_name_files(filter_file_name_path)
            self.original_names = self._get_name_files(original_file_name_path)
            self.same_meaning_dic = self._get_dictionary_files(same_meaning_file_path)
            AlignedTokenClassifier.__instance = self

    def error_type_classify(self, aligned_token):
        """
        len(aligned_token.outputs must be >= 1
        :param aligned_token:
        :return:
        """
        if len(aligned_token.outputs) == 1:
            for classifier in self.classifier_list_one:
                result = classifier(aligned_token)
                if result is not None:
                    return result
        else:
            for classifier in self.classifier_list_two:
                result = classifier(aligned_token)
                if result is not None:
                    return result

        return ErrorType.UNKNOWN

    @staticmethod
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
        if aligned_token.reference[-2:] == "th":
            if aligned_token.reference[:-2] == aligned_token.outputs[0]:
                return ErrorType.NUMBER
        return None

    @staticmethod
    def is_be_verb(aligned_token):
        if aligned_token.reference in be_verb:
            if aligned_token.outputs[0] in be_verb[aligned_token.reference]:
                return ErrorType.BE_VERB
        return None

    def is_plural(self, aligned_token):
        if self.p.compare(aligned_token.outputs[0], aligned_token.reference) is not False:
            if self.p.compare(aligned_token.outputs[0], aligned_token.reference) != "p:p":
                return ErrorType.PLURAL
            return None
        return None

    def is_name(self, aligned_token):
        reference = self._check_is_name(aligned_token.reference, filtered=True)
        if reference:
            outputs = self._check_is_name(aligned_token.outputs[0], filtered=False)
            if outputs:
                return ErrorType.IS_BOTH_NAME
            else:
                return ErrorType.IS_REFERENCE_NAME
        return None

    def is_difficult_word(self, aligned_token):
        reference_in_word_net = self._check_in_word_net(aligned_token.reference)
        if reference_in_word_net is False:
            return ErrorType.NOT_IN_WORD_NET
        return None

    def is_same_stem(self, aligned_token):
        """
        ???? Something weird like hop hope hopeful. I think it is wrong...
        :param aligned_token:
        :return:
        """
        if self.st.stem(aligned_token.reference) == self.st.stem(aligned_token.outputs[0]):
            return ErrorType.SAME_STEM_OTHER
        return None

    def is_same_meaning(self, aligned_token):
        """
        TODO: we will load the same meaning dictionary from a file
        :param aligned_token:
        :return:
        """
        reference_outputs = self.same_meaning_dic
        # reference_outputs = {"oh": ["o"], "ante": ["anti"], "gonna": ["going", "to"], "alright": ["all", "right"]}
        if len(aligned_token.outputs) == 2:
            if aligned_token.reference.replace("'s", "") == \
                    aligned_token.outputs[0] and aligned_token.outputs[1] == "is":
                return ErrorType.SAME_MEANING
        if aligned_token.reference in reference_outputs.keys():
            if reference_outputs[aligned_token.reference] == aligned_token.outputs:
                return ErrorType.SAME_MEANING
        return None

    @staticmethod
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

    @staticmethod
    def is_split(aligned_token):
        if "".join(aligned_token.outputs) == aligned_token.reference:
            return ErrorType.SPLIT
        return None

    @staticmethod
    def _check_in_word_net(string):
        result = wn.synsets(string)
        if len(result) == 0:
            return False
        else:
            return True

    def _check_is_name(self, string, filtered):
        if filtered:
            return string in self.filter_names
        else:
            return string in self.original_names

    @staticmethod
    def _get_name_files(file_names):
        result = set()
        for file_name in file_names:
            with open(file_name, "r") as csv_file:
                reader = csv.reader(csv_file)
                for item in reader:
                    result.add(item[0].lower())
        return result

    @staticmethod
    def _get_dictionary_files(file_names):
        result = {}
        with open(file_names, "r") as csv_file:
            reader = csv.reader(csv_file)
            for item in reader:
                result[item[0]] = item[1].split()
        return result
