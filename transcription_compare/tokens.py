

class Token:
    """
    Token used in edit distance calculator.

    NOTE:
        All kinds of tokens with __eq__ method implemented can be used in edit distance calculator
        Normally, using string as token is the simplest approach.
        This Token class is just a wrapper of str.
        This class can be extended to achieve other functions
    """

    __slots__ = ("token_str", )

    def __init__(self, token_str: str):
        self.token_str = token_str

    def __eq__(self, other):
        if isinstance(other, Token) and (other.token_str == self.token_str):
            return True
        if isinstance(other, str) and (other == self.token_str):
            return True
        return False


class MetaToken(Token):
    """
    Token with a map to store meta data
    """

    __slots__ = ("token_str", "metadata")

    def __init__(self, token_str: str, metadata: dict):
        super().__init__(token_str)
        self.metadata = metadata

    def get_metadata(self, key):
        return self.metadata.get(key)
