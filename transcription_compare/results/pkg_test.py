import pkg_resources
import csv

filter_file_names = ['names_csv/filter_female_first_names.csv',
                     'names_csv/filter_male_first_names.csv',
                     'names_csv/filter_all_names.csv']
filter_file_name_path = []
for filter_file_names in filter_file_names:
    filter_file_name_path.append(pkg_resources.resource_filename(__name__, filter_file_names))
print(filter_file_name_path)


def get_name_files(file_names):
    result = set()
    for file_name2 in file_names:
        with open(file_name2, "r") as csv_file:
            reader = csv.reader(csv_file)
            for item in reader:
                result.add(item[0].lower())
                break
    return result

print(get_name_files(filter_file_name_path))