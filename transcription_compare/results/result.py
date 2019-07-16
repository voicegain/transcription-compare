from .alignment_result import AlignmentResult


class Result:

    def __init__(self, distance: int, is_final: bool, len_ref: int, alignment_result: AlignmentResult = None):
        self.distance = distance
        if len_ref == 0:
            self.error_rate = None
        else:
            self.error_rate = self.distance / len_ref
        self.is_final = is_final
        self.alignment_result = alignment_result

    def to_json(self):
        return {
            "distance": self.distance,
            "is_final": self.is_final,
            "alignment_result": self.alignment_result.to_json()
        }

    def __str__(self):
        return "distance: {}\nerror rate: {}\nis_final: {}\nalignment_result:\n{}".format(
            self.distance, self.error_rate, self.is_final, self.alignment_result)
