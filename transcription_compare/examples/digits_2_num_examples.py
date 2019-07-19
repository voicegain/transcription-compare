import inflect
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.results import AlignmentResult

p = inflect.engine()

alignment_result = AlignmentResult()

alignment_result.add_token("1", ["one"])

alignment_result.add_token("2", ["two"], add_to_left=False)

alignment_result.add_token("3", ["three"], add_to_left=False)

for aligned_token in alignment_result:
    print(aligned_token.reference)

aligned_tokens = alignment_result.aligned_tokens_list
print('list', aligned_tokens)
print(aligned_tokens[0].reference)

print(len(aligned_tokens))

def number_to_word(num):
    words = set()
    words.add(p.number_to_words(num))
    words.add(p.number_to_words(num, group=1))#only have 3 group
    words.add(p.number_to_words(num, group=2))#好像可以, getlist=True
    words.add(p.number_to_words(num, group=3))
    words.add(p.number_to_words(p.ordinal(num)))
    return list(words)

reference_string = ''
calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=WordTokenizer(),
            get_alignment_result=True
        )
output_string = alignment_result.get_outputs_str()
reference_we_should_use = None

for index in range(0, len(aligned_tokens)):
    print(aligned_tokens[index])
    if aligned_tokens[index].reference.isdigit() is True:
        print('True', aligned_tokens[index])
        print('True', aligned_tokens[index].reference)
        print('True', number_to_word(aligned_tokens[index].reference))
        current_row = number_to_word(aligned_tokens[index].reference)
        print('current_row', current_row)
        len_of_current_row = len(current_row)
        count = 0
        old_distance = calculator.get_distance(alignment_result.get_reference_str(), output_string).distance
        print('old_distance', old_distance)
        # print('len_of_current_row',len_of_current_row)
        # while count <= len_of_current_row:
        print('before for', reference_we_should_use)
        for value in current_row:
            count += 1
            print('count', count)
            print(value)
            if reference_we_should_use is None:
                print('None', reference_we_should_use)
                reference_string = value
                reference_string += ' '+alignment_result[index+1:].get_reference_str()
                print('None,r', reference_string)
                print('None,o', output_string)
                new_distance = calculator.get_distance(reference_string, output_string).distance
                print('None', 'distance', new_distance)
                if new_distance < old_distance:
                    reference_we_should_use = value
                    distance = new_distance
                    print('None, if', reference_we_should_use)
            else:
                print('yes',value)
                print('yes', reference_we_should_use)
                reference_string += " ".join(value)
                reference_string += alignment_result[index+1:].get_reference_str()
                print('yes,r', reference_string)
                print('yes,o', output_string)
                new_distance = calculator.get_distance(reference_string, output_string).distance
                print('yes', 'distance', new_distance)
                if new_distance < old_distance:
                    reference_we_should_use += " ".join(value)
                    distance = new_distance
        print(reference_we_should_use)
    else:
        print('else',aligned_tokens[index])
print(reference_we_should_use)