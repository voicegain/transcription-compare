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


print(cut_text(reference, 3))


for i in len(reference):

    calculator.get_distance(reference, output, to_lower=False, remove_punctuation=False)