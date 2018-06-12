import tok
from instrument import Instrument
import collections

from song import Song

StatementReturn = collections.namedtuple('StatementReturn', 'identifier value')

"""
program:
    statement(s)
    block(s)

statement:
    identifier assign value
    identifier assign identifier

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
        self.instrument_stack = []
        self.song_stack = {}
        self.current_local_stack_obj = None
        """Push important constants on the global stack"""
        self.stack["PIANO"] = 1
        self.stack["BASS"] = 2
        self.stack["SYNTHESIZER"] = 3

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
        #statement:
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
        #block:
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
            obj.name = local_identifier
            self.instrument_stack.append(obj)
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
                        self.current_local_stack_obj.instruments = music_list

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
                    current_token = self.lexer.eat(self.current_token.token.typ, tok.MUSIC_PIECE)
                elif self.current_token.token.typ == tok.ADD:
                    current_token = self.lexer.eat(self.current_token.token.typ, tok.ADD)
                    self.current_token = current_token
                    continue
                else:
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
