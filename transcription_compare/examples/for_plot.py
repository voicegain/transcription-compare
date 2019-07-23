from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.utils.digit_util import DigitUtil
import re

calculator = UKKLevenshteinDistanceCalculator(
    tokenizer=WordTokenizer(),
    get_alignment_result=True,
    digit_util=None
)

reference = 'APPLE BANANA WATER BYE OK NO PROBLEM TIME LOG SEARCH'
output = 'APPLE BANANA HELLO WATER HA NO TIME LOG YES '
length = len(reference)
for i in range(1, length):
    b = re.split(r" +", reference)
    print(b)

def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr


reference = 'APPLE BANANA WATER BYE OK NO PROBLEM TIME LOG SEARCH'
output = 'APPLE BANANA HELLO WATER HA NO TIME LOG YES '
spaces_count = reference.count(' ')
length = len(reference)
print(length)
# print(spaces_count//2) #根据spaces的个数去判断

spaces_spot = [k for k in range(len(reference)) if reference.find(' ', k) == k]
print(spaces_spot)
for i in range(2, len(spaces_spot), 2):  # 应该是3，要-1
    print(i)
    print(spaces_spot[i])
    #     print(i+2)
    #     print(spaces_spot[i+2])
    if i == 2:
        print(reference[0:spaces_spot[i]])
    else:
        print(reference[spaces_spot[i - 2]:spaces_spot[i + 2]])

print(cut_text(reference, 3))


for i in len(reference):

    calculator.get_distance(reference, output, to_lower=False, remove_punctuation=False)