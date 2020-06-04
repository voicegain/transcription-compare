import requests
from bs4 import BeautifulSoup
import csv

# def replace_all(text, mydict):
#     for gb, us in mydict.items():
#         text = text.replace(us, gb)
#     return text


def get_dic_from_web(link, output_path):

    fileobject = open(output_path, 'w', newline="")
    csv_writer = csv.writer(fileobject)

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    # all_texts = soup.find_all('tr', class_='Body')
    all_texts = soup.find('tr', class_='Body')
    texts = all_texts.find_all('td')
    # texts = soup.find_all('td', valign='top')
    # print(len(texts))
    key = []
    for i in texts:
        key.append(str(i.text))
    # print(len(key[0]))
    uk = key[0].split()
    us = key[1].split()
    # print(len(uk))
    # print(uk[:5])
    # print(len(us))
    # print(us[:5])

    uk_us = {}
    for i in range(len(uk)):
        if uk[i] == '/' and us[i] == '/':
            continue
        uk_us[uk[i]] = us[i]
        csv_writer.writerow([uk[i]] + [us[i]])
    print(uk_us)
    print(len(uk_us))
    return uk_us



url = 'http://www.tysto.com/uk-us-spelling-list.html'

get_dic_from_web(url, 'uk_us_english.txt')
