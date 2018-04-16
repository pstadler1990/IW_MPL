KEYWORD, ASSIGN, VALUE, BLOCK_OPEN, BLOCK_CLOSE, IDENTIFIER, NOTE_IDENTIFIER = (
    "KEYWORD", "ASSIGN", "VALUE", "BLOCK_OPEN", "BLOCK_CLOSE", "IDENTIFIER", "NOTE"
)


class Tok(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value