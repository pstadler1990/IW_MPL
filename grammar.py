#TODO:
# - Nested blocks funktionieren noch nicht! -> er geht zwar in die blöcke, kommt aber dann beim rücksprung mit dem block_closed durcheinander


import tok
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

    def parse(self):
        self.progm()

    def progm(self):
        while self.lexer.hasNext():
            if self.current_token.token.typ == tok.IDENTIFIER:
                self.statement()
            elif self.current_token.token.typ == tok.KEYWORD:
                self.block()
            else:
                print("error")
                break
        print("End of file")


    def statement(self):
        #statement:
        #   identifier assign value
        #   identifier assign identifier
        token_identifier = str(self.current_token.token.value)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.ASSIGN)

        if self.current_token.token.typ == tok.VALUE:
            token_value = self.current_token.token.value
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.VALUE)
        elif self.current_token.token.typ == tok.IDENTIFIER:
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        else:
            print("ERROR in statement!")

        self.stack[token_identifier] = token_value


    def block(self):
        #block:
        #    keyword identifier[ statement(s) ]
        #    keyword identifier[ block(s) ]
        #    keyword identifier[ note_identifier(s) ]
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.KEYWORD)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.IDENTIFIER)
        self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_OPEN)

        print("Opened block")

        # Case 1: keyword identifier[ statement(s) ]
        if self.current_token.token.typ == tok.IDENTIFIER:
            self.statement()
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_CLOSE)
        # Case 2: keyword identifier[ block(s) ]
        elif self.current_token.token.typ == tok.KEYWORD:
            self.block()
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_CLOSE)
        elif self.current_token.token.typ == tok.NOTE_IDENTIFIER:
            self.notes()
            self.current_token = self.lexer.eat(self.current_token.token.typ, tok.BLOCK_CLOSE)
        else:
            print("ERROR at block!")


        #print("Closed block")


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

