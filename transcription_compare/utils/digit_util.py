import re
import inflect
p = inflect.engine()


def number_to_word(num):
    words = set()
    words.add(p.number_to_words(num))
    words.add(p.number_to_words(num, group=1))  # only have 3 group
    words.add(p.number_to_words(num, group=2))  # 好像可以, getlist=True
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
    number = re.findall('\d+', input_string)
    #     if if_number_inside(input_string) is True:
    if len(number) > 0:
        if input_string.replace(',', '').isdigit() is True:

            return [number_to_word(input_string)]
        elif input_string[-2:] in ('st', 'nd', 'rd', 'th'):
            return [number_to_word(input_string)]
        elif input_string[-1] == 's':
            return [century(input_string)]
        else:
            string = re.findall(r'[0-9]+|[a-z]+|[A-Z]+', input_string)
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

