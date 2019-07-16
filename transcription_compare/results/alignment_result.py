from typing import List
import json


class AlignmentResult:
    """
    Result of alignment, used by edit distance algorithm
    """
    def __init__(self):
        self.aligned_tokens_list = []

    def __iter__(self):
        return self.aligned_tokens_list.__iter__()

    def get(self, i):
        return self.aligned_tokens_list[i]

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

        self.aligned_tokens_list = new_aligned_token_list

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


if __name__ == "__main__":
    main()
