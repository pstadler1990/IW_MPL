import tok
from instrument import Instrument
import collections

from song import Song

StatementReturn = collections.namedtuple('StatementReturn', 'identifier value')

"""
program:
    statement(s)
    block(s)
    command(s)

statement:
    identifier assign value
    identifier assign identifier
    
command:
    keyword identifier

block:
    keyword identifier [ statement(s) ]
    keyword identifier [ block(s) ]
    keyword identifier [ note_identifier(s) ]
    keyword [ music_piece_list ]

keyword:
    (Instrument|Notes|Oscillator|Song)

identifier:
    [a-zA-Z_][a-zA-Z_0-9]*

assign:
    \:

note_identifier:
    (\.+|[a-zA-Z]([0-9]|#|(maj|min)[0-9])?)

value:
    ([0-9])
    
music_piece_list:
    music_piece 
    music_piece_list + music_piece_list
    music_piece_list, music_piece_list
    
music_piece:
    ([a-zA-Z_][a-zA-Z_0-9]+\.[a-zA-Z_][a-zA-Z_0-9]+)

"""


class Grammar(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next()
        self.stack = {}
        self.instrument_stack = {}
        self.song_stack = {}
        self.current_local_stack_obj = None
        """Push important constants on the global stack"""
        self.stack["PIANO"] = 1
        self.stack["BASS"] = 2
        self.stack["SYNTHESIZER"] = 3
        self.stack["PLAY_SONG"] = ""

    def parse(self):
        self.progm()

    def progm(self):
        errors = False
        while self.lexer.hasNext():
            if self.current_token.token.typ == tok.IDENTIFIER:
                """Add or update a global variable"""
                identifier, value = self.statement()
                self.stack[identifier] = value
            elif self.current_token.token.typ == tok.KEYWORD:
                """Keyword Identifier"""
                if self.current_token.token.value == 'Play':
                    self.current_token = self.lexer.eat(self.current_token.token.typ, tok.KEYWORD)
                    song_name = str(self.current_token.token.value)
                    self.stack["PLAY_SONG"] = song_name
                    self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
                    continue
                """Keyword Identifier [ block ]"""
                if not self.block():
                    errors = True
                    break
            else:
                errors = True
                break
        if not errors:
            print("End of file. SUCCESSFULLY parsed the file!")
        else:
            print("Found erros while parsing..")
            print(self.stack)
            print(self.instrument_stack)

    def statement(self):
        # statement:
        #   identifier assign value
        #   identifier assign identifier
        token_value = None
        token_identifier = str(self.current_token.token.value)

        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.ASSIGN)

        if self.current_token.token.typ == tok.VALUE:
            token_value = self.current_token.token.value
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.VALUE)
        elif self.current_token.token.typ == tok.IDENTIFIER:
            tmp_value = self.lookup_local_var(self.current_token.token.value)
            if tmp_value is None:
                tmp_value = self.lookup_global_var(self.current_token.token.value)
                if tmp_value is not None:
                    token_value = tmp_value
            else:
                token_value = tmp_value
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        return StatementReturn(identifier=token_identifier, value=token_value)

    def block(self):
        # block:
        #    keyword identifier[ statement(s) ]
        #    keyword identifier[ block(s) ]
        #    keyword identifier[ note_identifier(s) ]
        obj = None
        block_type = self.current_token.token.value

        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.KEYWORD)
        local_identifier = self.current_token.token.value
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_OPEN)

        if block_type == 'Instrument':
            obj = Instrument()
            self.instrument_stack[local_identifier] = obj
            self.current_local_stack_obj = obj
        elif block_type == 'Song':
            obj = Song()
            self.song_stack[local_identifier] = obj
            self.current_local_stack_obj = obj
        elif block_type == 'Oscillator':
            print("Error. This instrument is not supported yet..")
            return False

        while self.current_token.token.typ in (tok.IDENTIFIER, tok.KEYWORD, tok.NOTE_IDENTIFIER, tok.MUSIC_PIECE):
            # Case 1: keyword identifier[ statement(s) ]
            if self.current_token.token.typ == tok.IDENTIFIER:
                identifier, value = self.statement()
                if self.current_local_stack_obj is not None:
                    self.current_local_stack_obj.variables[identifier] = value
            # Case 2: keyword identifier[ block(s) ]
            elif self.current_token.token.typ == tok.KEYWORD:
                self.block()
            elif self.current_token.token.typ == tok.NOTE_IDENTIFIER:
                notelist = self.notes()
                if notelist is not None:
                    if self.current_local_stack_obj is not None:
                        self.current_local_stack_obj.notes[local_identifier] = notelist
            elif self.current_token.token.typ == tok.MUSIC_PIECE:
                music_list = self.music()
                if music_list is not None:
                    if self.current_local_stack_obj is not None:
                        self.current_local_stack_obj.pieces = music_list

        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_CLOSE)
        return True

    def notes(self):
        note_list = []
        while True:
            current_note = str(self.current_token.token.value)
            current_token = self.lexer.eat(self.current_token.token.typ, tok.NOTE_IDENTIFIER)
            if current_token is not None:
                note_list.append(current_note)
                self.current_token = current_token
            else:
                break
        return note_list

    def music(self):
        music_list = [[]]
        music_list.append(0)
        cur_index = 0
        while True:
            current_music_piece = str(self.current_token.token.value)

            if self.current_token.token.typ in (tok.MUSIC_PIECE, tok.ADD, tok.SEPARATE):
                if self.current_token.token.typ == tok.MUSIC_PIECE:
                    """Check, if the music piece exists in the global context, else quit and print an error"""
                    tmp = current_music_piece.split(".")
                    tmp_instrument = tmp[0]
                    tmp_piece = tmp[1]

                    if not self.lookup_piece(tmp_instrument, tmp_piece):
                        print("Error, unknown music piece and/or instrument")
                        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.MUSIC_PIECE)
                        break

                    current_token = self.lexer.eat(self.current_token.token.typ, tok.MUSIC_PIECE)
                elif self.current_token.token.typ == tok.ADD:
                    """A plus sign adds two (or more) music pieces into the same row (= played in parallel)"""
                    current_token = self.lexer.eat(self.current_token.token.typ, tok.ADD)
                    self.current_token = current_token
                    continue
                else:
                    """A comma separates the current piece and adds a new row to the music_list"""
                    current_token = self.lexer.eat(self.current_token.token.typ, tok.SEPARATE)
                    cur_index += 1
                    music_list.append(cur_index)
                    music_list[cur_index] = []
                    self.current_token = current_token
                    continue

                if current_token is not None:
                    music_list[cur_index].append(current_music_piece)
                    self.current_token = current_token
            else:
                break
        return music_list

    def lookup_global_var(self, identifier):
        return self.stack.get(identifier)

    def lookup_local_var(self, identifier):
        if self.current_local_stack_obj is not None:
            return self.current_local_stack_obj.variables.get(identifier)

    def lookup_piece(self, instrument, piece):
        try:
            for i in self.instrument_stack[instrument].notes:
                if i == piece:
                    return True
        except Exception:
            return False
