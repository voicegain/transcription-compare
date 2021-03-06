from abc import ABC, abstractmethod


class ReferenceCombinationGenerator(ABC):

    @abstractmethod
    def add_new_token_options(self, list_of_options):
        """
        add_new_token_options(list_of_options=["one", "first"])
        add_new_token_options(list_of_options=["two", "second"])
        :param list_of_options:
        :return:
        """
        pass

    @staticmethod
    def get_all_reference(self):
        """
        Return all reference list
        :param self:
        :return: [["one", "two"], ["first", "two"], ["one", "second"], ["first", "second"]]
        """
        pass


class TreeReferenceCombinationGenerator(ReferenceCombinationGenerator):
    def add_new_token_options(self, list_of_options):
        raise NotImplementedError()

    def get_all_reference(self):
        raise NotImplementedError()


class SimpleReferenceCombinationGenerator(ReferenceCombinationGenerator):

    def __init__(self):
        self.reference_list = []

    def add_new_token_options(self, set_of_options):
        """
        :param set_of_options: Set / List of options, each option can be a string or a list
        :return:
        """
        if len(self.reference_list) == 0:
            # add_new_token_options(list_of_options=["one", "first"])
            # want to get [["one"], ["first"]]
            for option in set_of_options:
                if isinstance(option, str):
                    option = [option]
                self.reference_list.append(option)
                # print(self.reference_list)
        else:
            new_reference_list = []
            for ref in self.reference_list:
                for option in set_of_options:
                    if isinstance(option, str):
                        option = [option]
                    ref_copy = ref.copy()
                    ref_copy += option
                    new_reference_list.append(ref_copy)
            self.reference_list = new_reference_list

    def get_all_reference(self):
        return self.reference_list


# generator = SimpleReferenceCombinationGenerator()
# generator.add_new_token_options(["one", "first"])
# generator.add_new_token_options(["of"])
# generator.add_new_token_options(["two", "second"])
# l = generator.get_all_reference()
# print(l)
