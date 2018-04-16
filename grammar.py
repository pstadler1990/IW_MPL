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

    def __init__(self):
        pass

    def parse(self, l):
        rCnt = 0
        pCnt = 0
        tokList = []
        t = l.next()
        for r in Rules:
            for tr in r.tokens:
                print ("t: " + str(t.type) + " tr: " + tr)
                while t.type == tr:
                    print ("ok, getting next")
                    tokList.append(t)
                    t = l.next()
                    pCnt+=1

                if pCnt == len(r.tokens):
                    print ("Rule " + str(r.name) + " complete!")
                    if r.name == "ASSIGNMENT_ID" or r.name == "ASSIGNMENT_VALUE":
                        self.assignment(tokList[0].value, tokList[2].value)

                else:
                    rCnt += 1

        if rCnt == len(Rules):
            raise Exception("Syntax error, no rule for ..")

    def assignment(self, identifier, value):
        print("assignment with: " + str(identifier) + " and value: " + str(value))
        try:
            _identifier = str(identifier)
            #TODO: Add both cases (assignment_id and assignment_value)
            _value = int(value)
        except ValueError:
            raise Exception("Value error")

        #TODO: check if variable is in predefined (global) variable stack
        #      if not, create a new (local) variable stack
        # set variable to value





class Rule(object):

    def __init__(self, name, tokens):
        self.name = name
        self.tokens = tokens


Rules = [
    Rule("ASSIGNMENT_ID", [tok.IDENTIFIER, tok.ASSIGN, tok.IDENTIFIER]),
    Rule("ASSIGNMENT_VALUE", [tok.IDENTIFIER, tok.ASSIGN, tok.VALUE]),
]



#Rule for Statement: IDENTIFIER ; ASSIGN ; VALUE | NAME
#if value: check, if there's a variable in the variable stack with the name of IDENTIFIER
    #if yes: set the variable to the new VALUE
    #if no: add the new variable IDENTIFIER to the variable stack and set the value to 0
#if name: check, if there's a variable in the variable stack with the name OF NAME
    # if yes: get the NAME's value and set the IDENTIFIER's value to NAME's value
    # if no: raise exception: Unknown variable NAME


#Rule for Keyword Instrument: KEYWORD Instrument ; IDENTIFIER ; BLOCK_OPEN; STATEMENT(S) | BLOCK(S); BLOCK_CLOSE