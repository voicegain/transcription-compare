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

    def calculate_four_things(self):
        distance = 0
        substitution = 0
        insertion = 0
        deletion = 0
        for aligned_token in self.aligned_tokens_list:
            if not aligned_token.match():
                if len(aligned_token.outputs) == 0:
                    deletion += 1
                    distance += 1
                elif len(aligned_token.outputs) > 1:
                    insertion += len(aligned_token.outputs)-1
                    distance += len(aligned_token.outputs)-1
                else:
                    substitution += 1
                    distance += 1
        DISTANCE = substitution + insertion + deletion
        return distance, substitution, insertion, deletion, DISTANCE