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
    pass


class Rule(object):
    pass


#Rule for Statement: IDENTIFIER ; ASSIGN ; VALUE | NAME
#if value: check, if there's a variable in the variable stack with the name of IDENTIFIER
    #if yes: set the variable to the new VALUE
    #if no: add the new variable IDENTIFIER to the variable stack and set the value to 0
#if name: check, if there's a variable in the variable stack with the name OF NAME
    # if yes: get the NAME's value and set the IDENTIFIER's value to NAME's value
    # if no: raise exception: Unknown variable NAME


#Rule for Keyword Instrument: KEYWORD Instrument ; IDENTIFIER ; BLOCK_OPEN; STATEMENT(S) | BLOCK(S); BLOCK_CLOSE