from abc import ABC, abstractmethod


class LocalOptimizer(ABC):

    @abstractmethod
    def update_alignment_result_error_section(self, alignment_result_error_section):
        """
        Optimize the alignment_result_error_section. Return the updated alignment_result
        Return None, if not updated
        :param alignment_result_error_section:
        :return:
        """
        pass
