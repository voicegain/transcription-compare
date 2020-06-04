from nltk.corpus import wordnet as wn
import csv
import pkg_resources
import string

wiki_words_file = 'frequency_all_words.csv'
wiki_words_file_path = pkg_resources.resource_filename(__name__, wiki_words_file)
print(wiki_words_file_path)

LETTER_LIST = set(string.ascii_letters)

DIGIT_LIST = set(string.digits)

Punctuation_LIST = set(string.punctuation)


def classify_three_type(word):
    """
    detect letter, digit, and other characters in the word
    :param word:
    :return: Three boolean has_letter, has_digit, has_notation
    """

    has_letter = False
    has_digit = False
    has_notation = False

    for c in word:
        if c in LETTER_LIST:
            has_letter = True
        elif c in DIGIT_LIST:
            has_digit = True
        else:
            has_notation = True

    return has_letter, has_digit, has_notation


def search_in_word_net(origin_names_file, output_file_name):
    csv_file = open(origin_names_file, "r")
    reader = csv.reader(csv_file)

    fileobject = open(output_file_name, 'w', newline="")
    csv_writer = csv.writer(fileobject)
    for item in reader:
        # print(item[0])
        if int(item[1]) >= 100:  # I set 100
            has_letter, has_digit, has_notation = classify_three_type(item[0])
            if has_notation and (not has_letter) and (not has_digit):
                print(item[0])
            else:
                result = wn.synsets(item[0])
                if len(result) == 0:  # not in word_net
                    # print(item[0])
                    csv_writer.writerow([item[0]])

    csv_file.close()
    fileobject.close()


not_in_word_net = 'transcription_compare/results/in_wiki_not_in_wordnet.csv'
not_in_word_net_file_path = pkg_resources.resource_filename(__name__, not_in_word_net)
# print(not_in_word_net_file_path)
search_in_word_net(wiki_words_file_path, not_in_word_net_file_path)