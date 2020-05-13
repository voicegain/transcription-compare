
# ..
import pkg_resources
uk_us_file = 'utils/alternative_spelling.txt'
uk_us_file = pkg_resources.resource_filename(__name__, uk_us_file)

alternative_spelling_dict = {}  # uk to us

with open(uk_us_file, "r", encoding="utf8") as id_file:
    for line in id_file:
        # print('line',line, len(line))
        line_list = line.strip().split(",")
        # print(line_list)
        alternative_spelling_dict[line_list[0]] = line_list[1]


class Token(str):

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value, prefix=None, postfix=None, use_alternative_spelling=False):
        self.prefix = prefix
        self.postfix = postfix
        # self.value = value
        self.alternative_spelling_set = set()
        if use_alternative_spelling:
            # self.alternative_spelling_set.add('hi')
            # print('value', value)
            if value in alternative_spelling_dict.keys():
                self.alternative_spelling_set.add(alternative_spelling_dict[value])

    def __eq__(self, other):
        if self.alternative_spelling_set:
            self_set = True
        else:
            self_set = False

        if isinstance(other, Token):
            if other.alternative_spelling_set:
                other_set = True
            else:
                other_set = False
        else:
            other_set = False

        if self_set:
            if other_set:
                # need to compare American version not British version
                for word in self.alternative_spelling_set:
                    if word in other.alternative_spelling_set:
                        return True

            else:
                if other in self.alternative_spelling_set:
                    return True
        else:
            if other_set:
                if self in other.alternative_spelling_set:
                    return True

        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

