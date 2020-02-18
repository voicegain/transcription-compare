from .alignment_result import AlignmentResult


class Result:

    def __init__(self, distance: int, is_final: bool, len_ref: int, len_output: int,
                 alignment_result: AlignmentResult = None, substitution: int = None,
                 insertion: int = None, deletion: int = None):
        self.distance = distance

        # we cannot calculate the error rate, because the word tokenizer make the ref empty

        if (len_ref == 0) and (len_output == 0):
            # we cannot calculate the error rate, because the word tokenizer make the ref and the output empty
            self.error_rate = 0
        elif (len_ref == 0) or (len_output == 0):
            # we cannot calculate the error rate, because the word tokenizer make the ref or the output empty,
            # like the sentence is just "um", or some words inside brackets if set the brackets list
            self.error_rate = 1

        else:
            self.error_rate = self.distance / len_ref
        self.is_final = is_final
        self.alignment_result = alignment_result
        self.substitution = substitution
        self.insertion = insertion
        self.deletion = deletion

    def to_json(self):
        return {
            "distance": self.distance,
            "substitution": self.substitution,
            "insertion": self.insertion,
            "deletion": self.deletion,
            "is_final": self.is_final,
            "alignment_result": self.alignment_result.to_json()
        }

    def to_html(self):
        return self.alignment_result.to_html()

    def __str__(self):
        return "distance: {}\nsubstitution: {}\ninsertion: {}\ndeletion: {}" \
               "\nerror rate: {}\nis_final: {}\nalignment_result:\n{}".format(
                self.distance, self.substitution, self.insertion, self.deletion,
                self.error_rate, self.is_final, self.alignment_result)
