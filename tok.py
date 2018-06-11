KEYWORD, ASSIGN, VALUE, BLOCK_OPEN, BLOCK_CLOSE, IDENTIFIER, NOTE_IDENTIFIER, STATEMENT = (
    "KEYWORD", "ASSIGN", "VALUE", "BLOCK_OPEN", "BLOCK_CLOSE", "IDENTIFIER", "NOTE", "STATEMENT"
)


class Tok(object):

    def __init__(self, typ, value):
        self.typ = typ
        self.value = value
