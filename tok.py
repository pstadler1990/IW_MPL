KEYWORD, ASSIGN, VALUE, BLOCK_OPEN, BLOCK_CLOSE, IDENTIFIER, NOTE_IDENTIFIER, STATEMENT, BLOCK, MUSIC_PIECE, ADD, SEPARATE = (
    "KEYWORD", "ASSIGN", "VALUE", "BLOCK_OPEN", "BLOCK_CLOSE", "IDENTIFIER", "NOTE", "STATEMENT", "BLOCK", "MUSIC_PIECE", "ADD", "SEPARATE"
)


class Tok(object):

    def __init__(self, typ, value):
        self.typ = typ
        self.value = value
