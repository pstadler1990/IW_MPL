#TODO: Identifiers like Piano are not recognized as a value yet

import tok
from instrument import Instrument
import collections

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

keyword:
    (Instrument|Notes|Oscillator)

identifier:
    [a-zA-Z_][a-zA-Z_0-9]*

assign:
    \:

note_identifier:
    (\.+|[a-zA-Z]([0-9]|#|(maj|min)[0-9])?)

value:
    ([0-9])
"""


class Grammar(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next()
        self.stack = {}
        self.instrument_stack = []

    def parse(self):
        self.progm()

    def progm(self):
        while self.lexer.hasNext():
            if self.current_token.token.typ == tok.IDENTIFIER:
                """Add or update a global variable"""
                identifier, value = self.statement()
                self.stack[identifier] = value
            elif self.current_token.token.typ == tok.KEYWORD:
                self.block()
            else:
                print("error")
                break
        print("End of file")

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
            #TODO: Piano is not a value yet
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        else:
            print("ERROR in statement!")

        return StatementReturn(identifier=token_identifier, value=token_value)

    def block(self):
        #block:
        #    keyword identifier[ statement(s) ]
        #    keyword identifier[ block(s) ]
        #    keyword identifier[ note_identifier(s) ]
        block_type = self.current_token.token.value

        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.KEYWORD)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_OPEN)

        print("Opened block " + str(block_type))

        if block_type == 'Instrument':
            obj = Instrument()
            self.instrument_stack.append(obj)

        while self.current_token.token.typ in (tok.IDENTIFIER, tok.KEYWORD, tok.NOTE_IDENTIFIER):
            # Case 1: keyword identifier[ statement(s) ]
            if self.current_token.token.typ == tok.IDENTIFIER:
                identifier, value = self.statement()
                if obj is not None:
                    obj.variables[identifier] = value
            # Case 2: keyword identifier[ block(s) ]
            elif self.current_token.token.typ == tok.KEYWORD:
                self.block()
            elif self.current_token.token.typ == tok.NOTE_IDENTIFIER:
                self.notes()
                #TODO: obj.notes.append(self.notes())

        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_CLOSE)
        print("Closed block")

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
        # TODO: notes() must return a tuple of identifier and notelist (=> is then used in the enclosing block method)
