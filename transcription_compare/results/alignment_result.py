from typing import List
import json


class AlignmentResult:
    """
    Result of alignment, used by edit distance algorithm
    """

    def __init__(self, aligned_tokens_list=None):
        if aligned_tokens_list is None:
            self.aligned_tokens_list = []
        else:
            self.aligned_tokens_list = aligned_tokens_list

    def __iter__(self):
        return self.aligned_tokens_list.__iter__()

    def __len__(self):
        return len(self.aligned_tokens_list)

    def __getitem__(self, item):
        return AlignmentResult(self.aligned_tokens_list[item])

    def __add__(self, other):
        return AlignmentResult(self.aligned_tokens_list + other.aligned_tokens_list)

    def get_reference(self):
        return [i.reference for i in self.aligned_tokens_list]

    def get_reference_str(self):
        return " ".join(self.get_reference())

    def get_outputs(self):
        outputs = []
        for i in self.aligned_tokens_list:
            outputs += i.outputs
        return outputs

    def get_outputs_str(self):
        return " ".join(self.get_outputs())

    def get(self, i):
        return self.aligned_tokens_list[i]

    @staticmethod
    def load_from_file(file_path, result_name):
        with open(file_path, "r") as f:
            for x in f:
                x_list = x.split()
                result_name.add_token(
                            ref_token=x_list[0],
                            output_tokens=x_list[1:],
                            add_to_left=False)
                # print(result_name)
        return result_name

    def add_token(self, ref_token, output_tokens: List, add_to_left: bool = True):
        """
        Add one ref-output pair to the alignmentResult list
        :param ref_token: string. The ref token
        :param output_tokens: list of String. Can be empty
        :param add_to_left:
            If True, add the new token to the left end of the list
            Otherwise, add it to the right end
        :return:
        """
        new_aligned_token = AlignedToken(ref_token, output_tokens)
        if add_to_left:
            self.aligned_tokens_list.insert(0, new_aligned_token)
        else:
            self.aligned_tokens_list.append(new_aligned_token)

    def extend_existing_token(self, output_tokens: List, ind: int = 0, extend_output_token_to_left: bool = True):
        """
        Add several output tokens into existing ref-output pair
        :param output_tokens: list of string. New output tokens
        :param ind: The index of tokens in the existing token list to be extended to
                    Normally, set ind to 0 to extend the first token
                              set ind to -1 to extend the last token
        :param extend_output_token_to_left:
                If True, extend new output tokens to the left of existing output_tokens list
                Otherwise, extend it to the right
        :return:
        """
        token_to_extend = self.aligned_tokens_list[ind]
        token_to_extend.extend_output_tokens(output_tokens, extend_output_token_to_left)

    def to_json(self):
        """
        Output to the following json format
        [
            {"ref": <reference_token>, "out": [<output_token>]},
            {"ref": <reference_token>, "out": [<output_token>]}
        ]
        :return:
        """
        json_list = []
        for aligned_token in self.aligned_tokens_list:
            json_list.append(aligned_token.to_json())
        return json_list

    def to_html(self):
        message = """<html>
         <head>
         <style>
         table {
           font-family: arial, sans-serif;
           border-collapse: collapse;
           width: 100%;
         }

         td, th {
           border: 1px solid #dddddd;
           text-align: left;
           padding: 8px;
         }

         </style>
         </head>
         <body>

         <h2>transcription-compare Table</h2>

         <table>
           <tr>
             <th>Reference</th>
             <th>Output</th>
             <th>distance</th>
             <th>substitution</th>
             <th>insertion</th>
             <th>deletion</th>
           </tr> """
        all_substitution = 0
        all_insertion = 0
        all_deletion = 0
        all_distance = 0
        for aligned_token in self.aligned_tokens_list:
            message_single, substitution, insertion, deletion = aligned_token.to_html()
            # message += aligned_token.to_html()
            message += message_single
            all_substitution += substitution
            all_insertion += insertion
            all_deletion += deletion
            all_distance += substitution + insertion + deletion
            # print(message)
        message += '\n<tr>\n<td colspan="2">' + 'total' + '</td>'
        message += '\n<td>' + str(all_distance) + '</td>'
        message += '\n<td>' + str(all_substitution) + '</td>'
        message += '\n<td>' + str(all_insertion) + '</td>'
        message += '\n<td>' + str(all_deletion) + '</td>\n</tr>'
        message += '\n</body>\n</html>'
        return message

    def __str__(self):
        return self.to_pretty_str()

    def to_pretty_str(self):
        s = ""
        for aligned_token in self.aligned_tokens_list:
            tokens = [str(aligned_token.reference)] + aligned_token.outputs
            s += ("\t".join(tokens) + "\n")
        return s

    def to_file(self, output_file_path: str):
        """
        Output to a file in following format:

        reference_1   output_1_0    output_1_1
        reference_2
        reference_3   output_3_0

        :param output_file_path:
        :return:
        """
        with open(output_file_path, "w") as f:
            f.write(self.to_pretty_str())

    def merge_none_tokens(self):
        """
        merge all alignedToken whose reference is None into their neighborhood
        If possible, they are preferred to be merged into the token before it.
        # TODO: might move it out of this method
        Also move mistakes around to increase the number of lines that correct
        :return:
        """
        new_aligned_token_list = []
        for (M, aligned_token) in enumerate(self.aligned_tokens_list):
            if aligned_token.reference is None:
                if len(new_aligned_token_list) == 0:
                    new_aligned_token_list.append(aligned_token)
                else:
                    new_aligned_token_list[-1].extend_output_tokens(
                        output_tokens=aligned_token.outputs,
                        extend_output_token_to_left=False
                    )
            else:
                new_aligned_token_list.append(aligned_token)
        if (len(new_aligned_token_list) > 1) and (new_aligned_token_list[0].reference is None):
            first_token = new_aligned_token_list.pop(0)
            new_aligned_token_list[0].extend_output_tokens(
                output_tokens=first_token.outputs,
                extend_output_token_to_left=True
            )

        # handle the case that reference is empty
        for token in new_aligned_token_list:
            if token.reference is None:
                token.reference = ""

        self.aligned_tokens_list = new_aligned_token_list

        for i in range(1, len(self.aligned_tokens_list)):
            if (not self.aligned_tokens_list[i].match()) and (not self.aligned_tokens_list[i-1].match()):
                # print(self.aligned_tokens_list[i-1].reference)
                # print(self.aligned_tokens_list[i - 1].outputs[1:])
                if len(self.aligned_tokens_list[i-1].outputs) > 0 and self.aligned_tokens_list[i-1].reference == self.aligned_tokens_list[i-1].outputs[0]:
                    self.aligned_tokens_list[i].extend_output_tokens(
                                                output_tokens=self.aligned_tokens_list[i-1].outputs[1:],
                                                extend_output_token_to_left=True
                                            )
                    self.aligned_tokens_list[i-1].outputs = [self.aligned_tokens_list[i-1].outputs[0]]
                    # print('r', self.aligned_tokens_list[i - 1].reference,
                    # 'o', self.aligned_tokens_list[i - 1].outputs)
                    # print('ri', self.aligned_tokens_list[i].reference, 'oi', self.aligned_tokens_list[i].outputs)



    def __eq__(self, other):
        # not the same instance
        if not isinstance(other, AlignmentResult):
            return False
        # token length
        if len(self.aligned_tokens_list) != len(other.aligned_tokens_list):
            return False
        # compare alignedToken
        for i in range(len(self.aligned_tokens_list)):
            t1 = self.aligned_tokens_list[i]
            t2 = other.aligned_tokens_list[i]
            if t1 != t2:
                return False
        return True

    def calculate_three_kinds_of_distance(self):
        substitution = 0
        insertion = 0
        deletion = 0
        distance = 0
        for aligned_token in self.aligned_tokens_list:
            tmp_distance, tmp_substitution, tmp_insertion, tmp_deletion \
                = aligned_token.calculate_three_kinds_of_distance()
            substitution += tmp_substitution
            insertion += tmp_insertion
            deletion += tmp_deletion
            distance += tmp_distance
        return distance, substitution, insertion, deletion

    def get_error_section_list(self):
        """
        get AlignmentResultErrorSectionList
        :return:
        """
        not_match_n = 0
        error_section_list = AlignmentResultErrorSectionList()
        for (M, aligned_token) in enumerate(self.aligned_tokens_list):
            if aligned_token.match():
                if not_match_n > 0:
                    start_ind = M - not_match_n
                    error_section_list.add(
                        alignment_result_error_section=AlignmentResultErrorSection(
                            original_alignment_result=AlignmentResult(self.aligned_tokens_list[start_ind:M]),
                            start_ind=start_ind,
                            end_ind=M
                        )
                    )
                not_match_n = 0
            else:
                not_match_n += 1
        if not_match_n > 0:
            error_section_list.add(
                alignment_result_error_section=AlignmentResultErrorSection(
                    original_alignment_result=AlignmentResult(self.aligned_tokens_list[-not_match_n:]),
                    start_ind=len(self.aligned_tokens_list) - not_match_n,
                    end_ind=len(self.aligned_tokens_list)
                )
            )
        return error_section_list

    def apply_error_section_list(self, error_section_list):
        """
        Apply AlignmentResultErrorSectionList back to the alignment result
        :return:
        """
        start_ind = 0
        output_aligned_tokens_list = []
        for error_section in error_section_list:
            if error_section.alignment_result_correction is not None:
                output_aligned_tokens_list += self.aligned_tokens_list[start_ind:error_section.start_ind]
                output_aligned_tokens_list += error_section.alignment_result_correction.aligned_tokens_list
                start_ind = error_section.end_ind
        output_aligned_tokens_list += self.aligned_tokens_list[start_ind:]
        self.aligned_tokens_list = output_aligned_tokens_list

    def window(self, step, width):  # -> List[AlignmentResult]
        output_list = list()

        print('step', step)
        if width >= len(self.aligned_tokens_list):
            return [self]

        for i in range(0, len(self.aligned_tokens_list), step):
            if i+width <= len(self.aligned_tokens_list):
                output_list.append(AlignmentResult(self.aligned_tokens_list[i:i+width]))
        return output_list


class AlignedToken:
    """
    (reference, output) token pair
    """
    def __init__(self, reference, outputs: List):
        self.reference = reference
        self.outputs = outputs

    def to_json(self):
        """
        Return json representation of an alignedToken
        {"ref": <reference_token>, "out": [<output_token>]}
        :return:
        """
        return {
            "ref": self.reference,
            "out": self.outputs
        }

    def to_html(self):
        """
        Return str representation of an alignedToken
        <reference_token>, [<output_token>]
        :return:
        """

        distance, substitution, insertion, deletion = self.calculate_three_kinds_of_distance()

        if deletion > 0:# blue
            message = '\n<tr bgcolor=#00c3ff>\n<td>' + self.reference + '</td>'
        elif substitution > 0 and insertion == 0:#yellow
            message = '\n<tr bgcolor="#f7fb00">\n<td>' + self.reference + '</td>'
        elif substitution > 0 and insertion > 0: # orange
            message = '\n<tr bgcolor="#fb7900">\n<td>' + self.reference + '</td>'
        elif substitution == 0 and insertion > 0:  # red
            message = '\n<tr bgcolor=#fb0000>\n<td>' + self.reference + '</td>'
        else:
            message = '\n<tr>\n<td>' + self.reference + '</td>'
        message += '\n<td>' + " ".join(self.outputs) + '</td>'
        message += '\n<td>' + str(distance) + '</td>'
        message += '\n<td>' + str(substitution) + '</td>'
        message += '\n<td>' + str(insertion) + '</td>'
        message += '\n<td>' + str(deletion) + '</td>\n</tr>'

        return message, substitution, insertion, deletion

    def __str__(self):
        return json.dumps(self.to_json())

    def __eq__(self, other):
        if not isinstance(other, AlignedToken):
            return False
        if self.reference != other.reference:
            return False
        if len(self.outputs) != len(other.outputs):
            return False
        for i in range(len(self.outputs)):
            if self.outputs[i] != other.outputs[i]:
                return False
        return True

    def extend_output_tokens(self, output_tokens: List, extend_output_token_to_left: bool):
        if extend_output_token_to_left:
            self.outputs = output_tokens + self.outputs
        else:
            self.outputs = self.outputs + output_tokens

    def match(self) -> bool:
        if len(self.outputs) == 1:
            if self.reference == self.outputs[0]:
                return True
        return False

    def calculate_three_kinds_of_distance(self):
        substitution = 0
        insertion = 0
        deletion = 0
        if not self.match():
            if len(self.outputs) == 0:
                deletion += 1
            elif len(self.outputs) > 1:
                if self.reference == '':
                    insertion += len(self.outputs)
                else:
                    insertion += len(self.outputs) - 1
                    if self.reference not in self.outputs:
                        substitution += 1
            else:
                substitution += 1
        distance = substitution + insertion + deletion
        return distance, substitution, insertion, deletion


class AlignmentResultErrorSectionList:
    """
    The Error Section list from the alignment result
    In alignment_result, the ErrorSectionList can be get by get_error_section_list method
    After correct the ErrorSectionList, use the apply_error_section_list method to apply the correction
    """
    def __init__(self):
        self.alignment_result_error_section_list = []

    def __iter__(self):
        return self.alignment_result_error_section_list.__iter__()

    def __getitem__(self, item):
        return self.alignment_result_error_section_list[item]

    def add(self, alignment_result_error_section):
        if len(self.alignment_result_error_section_list) > 0:
            last_error_section = self.alignment_result_error_section_list[-1]
            if last_error_section.end_ind >= alignment_result_error_section.start_ind:
                raise ValueError("New alignment_result_error_section.start_ind <= last.end_ind")
        self.alignment_result_error_section_list.append(alignment_result_error_section)


class AlignmentResultErrorSection:
    """
    One error section in the alignment result
    Contain the original alignment_result (error part), and the corrected alignment_result
    """
    def __init__(self, original_alignment_result, start_ind, end_ind):
        self.original_alignment_result = original_alignment_result
        self.start_ind = start_ind
        self.end_ind = end_ind
        self.alignment_result_correction = None
        if self.start_ind >= self.end_ind:
            raise ValueError("AlignmentResultErrorSection start_ind >= end_ind")

    def set_correction(self, alignment_result_correction):
        self.alignment_result_correction = alignment_result_correction


def main():
    # First, you need to create a empty alignment result:
    alignment_result = AlignmentResult()
    print("empty alignment result:")
    print(alignment_result)
    # In your backtracking algorithm, when you get a new (reference_token, output_token) pair like this:
    new_reference_token_example = "a"
    new_output_token_example = "a"
    # you can add it to the left end of alignment result:
    alignment_result.add_token(
        ref_token=new_reference_token_example,
        output_tokens=[new_output_token_example],
        add_to_left=True
    )
    print(alignment_result)
    # since your algorithm is backtracking, normally you only need to add to the left end.
    # However, if you want to add to the right end, you can:
    alignment_result.add_token(
        ref_token="b",
        output_tokens=["b"],
        add_to_left=False
    )
    print(alignment_result)
    # Notice that the output_tokens is a list of string. So you can add zero or more than one output tokens:
    alignment_result.add_token(
        ref_token="c",
        output_tokens=["c", "d"],
        add_to_left=True
    )
    print(alignment_result)
    # Sometimes, you might want to extend more output tokens to the existing ref-output pair
    # For example
    # Currently, the first token is {"out": ["c", "d"], "ref": "c"}
    # and you find an insertion error, and want to extend the first token to: {"out": ["f", "c", "d"], "ref": "c"}
    alignment_result.extend_existing_token(
        output_tokens=["f"],
        ind=0,
        extend_output_token_to_left=True
    )
    print(alignment_result)
    # If you want to extend a "g" to the right side of output tokens to get:
    #  {"out": ["f", "c", "d", "g"], "ref": "c"}
    alignment_result.extend_existing_token(
        output_tokens=["g"],
        ind=0,
        extend_output_token_to_left=False
    )
    print(alignment_result)

    # add None
    alignment_result.add_token(ref_token=None, output_tokens=["1"], add_to_left=True)
    alignment_result.add_token(ref_token=None, output_tokens=["2"], add_to_left=True)
    alignment_result.add_token(ref_token=None, output_tokens=["3"], add_to_left=False)
    alignment_result.add_token(ref_token="1", output_tokens=["4"], add_to_left=False)
    alignment_result.add_token(ref_token=None, output_tokens=["5"], add_to_left=False)
    print(alignment_result)
    # merge
    alignment_result.merge_none_tokens()
    print(alignment_result)

    print(len(alignment_result))
    print(alignment_result[0:2])
    print(alignment_result.get_reference())
    print(alignment_result.get_reference_str())
    print(alignment_result.get_outputs())
    print(alignment_result.get_outputs_str())

    print(alignment_result + alignment_result)

    print("error_section_list examples")
    alignment_result_with_error = AlignmentResult()
    alignment_result_with_error.add_token(ref_token="on", output_tokens=["on"], add_to_left=False)
    alignment_result_with_error.add_token(ref_token="1", output_tokens=["one"], add_to_left=False)
    alignment_result_with_error.add_token(ref_token="2", output_tokens=["two"], add_to_left=False)
    alignment_result_with_error.add_token(ref_token="on", output_tokens=["on"], add_to_left=False)
    alignment_result_with_error.add_token(ref_token="3", output_tokens=["three"], add_to_left=False)
    print(alignment_result_with_error)

    error_list = alignment_result_with_error.get_error_section_list()

    for e in error_list:
        print(e.original_alignment_result)

    # fix first one
    correct_r = AlignmentResult()
    correct_r.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
    correct_r.add_token(ref_token="two", output_tokens=["two"], add_to_left=False)
    error_list[0].set_correction(correct_r)

    # fix second one
    correct_r = AlignmentResult()
    correct_r.add_token(ref_token="three", output_tokens=["three"], add_to_left=False)
    error_list[1].set_correction(correct_r)

    alignment_result_with_error.apply_error_section_list(error_list)
    print(alignment_result_with_error)


if __name__ == "__main__":
    main()
