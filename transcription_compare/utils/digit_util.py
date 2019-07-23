import re
import inflect
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.utils import SimpleReferenceCombinationGenerator
p = inflect.engine()


def number_to_word(num):
    words = set()
    words.add(p.number_to_words(num))
    words.add(p.number_to_words(num, group=1))
    words.add(p.number_to_words(num, group=2))
    words.add(p.number_to_words(num, group=3))
    try:
        words.add(p.number_to_words(p.ordinal(num)))
    except:
        pass
    words.add(p.number_to_words(num, group=1, zero='oh'))
    words.add(p.number_to_words(num, group=2, zero='oh'))
    words.add(p.number_to_words(num, group=3, zero='oh'))
    words = list(words)
    for index, x in enumerate(words):
        if x.find(",") >= 1:
            words[index] = words[index].replace(",", "")
    return set(words)


def century(number):
    if number[1:-1] == '000':
        result = p.number_to_words(number)
    else:
        result = p.number_to_words(number, group=2)
    if result[-1] != 'y':
        result = result + 's'
    else:
        result = result[:-1] + 'ies'

    result = [result]
    for index, x in enumerate(result):
        if x.find(",") >= 1:
            result[index] = result[index].replace(",", "")
    return set(result)


# def if_number_inside(input_string):
#     return bool(re.compile(r'.*\d+').match(input_string))


def our_is_digit(input_string):
    # TODO: need some improvement
    number = re.findall('\d+', input_string)
    #     if if_number_inside(input_string) is True:
    if len(number) > 0:
        if input_string.replace(',', '').isdigit() is True:
            return [number_to_word(input_string)]
        elif len(number[0])+2 == len(input_string)\
                and (input_string[-3:] in ('1st', '2nd', '3rd') or (input_string[-2:] == 'th')):
            return [number_to_word(input_string)]
        elif len(number[0])+1 == len(input_string) and input_string[-1] == 's':
            return [century(input_string)]
        else:
            string = re.findall(r'[0-9]+|[a-zA-Z]+', input_string)
            result = []
            for character in string:
                if character.isdigit() is False:
                    for i in character:
                        result.append({i})
                else:
                    result.append(number_to_word(character))
        return result
    else:
        return False


def update_alignment_result(alignment_result):
    #   alignment_result = result.alignment_result
    aligned_tokens_list = alignment_result.aligned_tokens_list

    calculator = UKKLevenshteinDistanceCalculator(
                tokenizer=WordTokenizer(),
                get_alignment_result=False
            )
    output_string = alignment_result.get_outputs_str()
    old_distance = alignment_result.calculate_three_kinds_of_distance()[0]
    generator = SimpleReferenceCombinationGenerator()
    tmp_result = None
    for index in range(0, len(alignment_result)):
        # if aligned_tokens_list[index].reference.isdigit() is True:
        result_digit = our_is_digit(aligned_tokens_list[index].reference)
        if result_digit is not False:
            for r in result_digit:
                generator.add_new_token_options(r)
        else:
            generator.add_new_token_options(aligned_tokens_list[index].reference)
        # print('generator.get_all_reference()', generator.get_all_reference())
        for x in generator.get_all_reference():
            x = " ".join(x)
            distance = calculator.get_distance(x, output_string).distance
            # print('x', x)
            # print('output_string', output_string)
            # print('distance', distance)

            if distance < old_distance:
                old_distance = distance
                tmp_result = x
    if tmp_result is None:
        return None
    calculator2 = UKKLevenshteinDistanceCalculator(
        tokenizer=WordTokenizer(),
        get_alignment_result=True
    )
    update_result = calculator2.get_distance(tmp_result, output_string).alignment_result
    return update_result