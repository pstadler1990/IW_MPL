KEYWORD, ASSIGN, VALUE, BLOCK_OPEN, BLOCK_CLOSE, IDENTIFIER, NOTE_IDENTIFIER, STATEMENT, BLOCK, MUSIC_PIECE, ADD, SEPARATE, PLAY, CONST = (
    "KEYWORD", "ASSIGN", "VALUE", "BLOCK_OPEN", "BLOCK_CLOSE", "IDENTIFIER", "NOTE", "STATEMENT", "BLOCK", "MUSIC_PIECE", "ADD", "SEPARATE", "PLAY", "CONST"
)


class Tok(object):

    def __init__(self, typ, value):
        self.typ = typ
        self.value = value
