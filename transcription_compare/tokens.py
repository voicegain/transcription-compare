

class Token(str):

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value, prefix=None, postfix=None):
        self.prefix = prefix
        self.postfix = postfix
