from nltk.corpus import wordnet as wn
import csv


# word = ['robert', 'John', 'Sophia', 'apple']
# file = []
# for item in word:
#     lexical_filename = set()
#     result = wn.synsets(item)
#     if len(result) == 0:
#         file.append(item)
#     else:
#         for i in result:
#             lexical_filename.add(i.lexname())
#         if len(lexical_filename) == 1:
#             if "noun.person" in lexical_filename:
#                 file.append(item)
# print(file)

#无的 返回 [] 空

def get_name_list(origin_names_file, output_file_name):
    csv_file = open(origin_names_file, "r")
    reader = csv.reader(csv_file)

    fileobject = open(output_file_name, 'w', newline="")
    csv_writer = csv.writer(fileobject)
    for item in reader:
        lexical_filename = set()
        result = wn.synsets(item[0])
        if len(result) == 0:
            csv_writer.writerow(item)
        else:
            for i in result:
                lexical_filename.add(i.lexname())
            if len(lexical_filename) == 1:
                if "noun.person" in lexical_filename:
                    csv_writer.writerow(item)
            # else:
            #     print(item)
    csv_file.close()
    fileobject.close()

get_name_list('female_first.csv', 'filter_female_first_names.csv')
get_name_list('male_first.csv', 'filter_male_first_names.csv')
get_name_list('all_names.csv', 'filter_all_names.csv')