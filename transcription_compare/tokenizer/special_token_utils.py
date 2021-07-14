from string import punctuation

URL_ = [".com", ".edu", ".net", ".org", ".ai"]

def process_email(word):
    """
    0. strip the "." at the end.
    if "@" exists, replace and dot
    :param word:
    :return:
    """
    word = word.rstrip(punctuation)
    if "@" in word:
        word = word.replace("@", " at ").replace(".", " dot ").replace("-", " dash ")
        return word
    return None


def process_url(word):
    # www.google.com/help
    #
    """
    0. strip the "." at the end.
       "google.com."
    1. what's url???
       ends with ".com", ".edu", ".net", ".org", ".ai"
       # todo
       or ".com", ".edu", ".net", ".org", ".ai" + "/" + something(i dont think people will say slash if nothing )

    2. rules: replace "." -> dot. "slash"
    :param word:
    :return:
    """
    word = word.rstrip(punctuation)
    for one_url in URL_:
        # print("word[-len(one_url):]", word[-len(one_url):])
        if word[-len(one_url):] == one_url:
            word = word.replace(".", " dot ").replace("-", " dash ")
            return word
        if one_url + "/" in word:
            word = word.replace(".", " dot ").replace("/", " slash ").replace("-", " dash ")
            return word

    return None


def process_and(word): # "AT and T"
    if "&" in word:
        word = word.replace("&", " and ")
        return word

    return None


# # test = ["im@haha.com1.?haha.", "test2@gmail", "test3@",
# #  "www.google.com", "computerhope.com/", "vg.ai",
# #  "haha.net/hello", "at&t"]
# test = ["test3@",
#  "www.google.com", "computerhope.com/",
#  "haha.net/hello"]
# methods = [process_email, process_url, process_and]
# for one in test:
#     for method in methods:
#         print("one, ", one)
#         print("method", method, method(one), "\n")
# # test3@
