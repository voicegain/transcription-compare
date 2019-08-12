from enum import Enum
from nltk.stem import SnowballStemmer
import csv

filter_file_names = ['names_csv/filter_female_first_names.csv',
                     'names_csv/filter_male_first_names.csv',
                     'names_csv/filter_all_names.csv']
original_file_names = ['names_csv/female_first.csv',
                       'names_csv/male_first.csv',
                       'names_csv/all_names.csv']


class ErrorType(Enum):
    NUMBER = 1
    DOUBLE = 2
    SPLIT = 3
    is_both_name = 4
    is_reference_name = 5
    SAME_MEANING = 6
    SAME_STEM_OTHER = 7
    UNKNOWN = 8


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
            self.classifier_list_one = [
                self.is_number, self.is_same_meaning, self.is_name, self.is_same_stem
            ]
            self.classifier_list_two = [
                self.is_double, self.is_same_meaning, self.is_split
            ]
            self.filter_names = self._get_name_files(filter_file_names)
            self.original_names = self._get_name_files(original_file_names)
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
        return None

    def is_name(self, aligned_token):
        reference = self._check_is_name(aligned_token.reference, filtered=True)
        if reference:
            outputs = self._check_is_name(aligned_token.outputs[0], filtered=False)
            if outputs:
                return ErrorType.is_both_name
            else:
                return ErrorType.is_reference_name

    def is_same_stem(self, aligned_token):
        """
        ???? Something weird like hop hope hopeful. I think it is wrong...
        :param aligned_token:
        :return:
        """
        if self.st.stem(aligned_token.reference) == self.st.stem(aligned_token.outputs[0]):
            return ErrorType.SAME_STEM_OTHER
        return None

    @staticmethod
    def is_same_meaning(aligned_token):
        """
        TODO: we will load the same meaning dictionary from a file
        :param aligned_token:
        :return:
        """
        reference_outputs = {"oh": ["o"], "ante": ["anti"], "gonna": ["going", "to"], "alright": ["all", "right"]}
        if aligned_token.reference.replace("'s", "") == aligned_token.outputs[0] and aligned_token.outputs[1] == "is":
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
                    # break
        return result
