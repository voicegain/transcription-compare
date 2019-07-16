from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer


calculator = UKKLevenshteinDistanceCalculator(
    tokenizer=CharacterTokenizer(),
    get_alignment_result=True
)

print(calculator.get_distance("abc", "abd"))
print(calculator.get_distance("abc", "abcd"))
print(calculator.get_distance("AV", "Abc"))

print(calculator.get_distance('batman', 'b'))

print(calculator.get_distance('b', 'batman'))
print(calculator.get_distance('batman', 'b'))
print(calculator.get_distance('AVERY', 'GARVEY'))
print(calculator.get_distance('ernest', 'nester')) #except this one; befor the 1 c
print(calculator.get_distance('werewolf', 'were  wolf'))
print(calculator.get_distance('jijizhazha', 'hahahaaaa???'))#excep; befor the 1 c
print(calculator.get_distance('helloa a a ?', 'HHHHHHHoooooo'))
print(calculator.get_distance('happyeveryday', 'happybirthday'))
