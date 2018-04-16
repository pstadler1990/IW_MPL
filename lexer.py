import re

class Lexer(object):

    matchExpr = {
        "WHITESPACE" : r'[ \n\t\r]',
        "NAME" : r'[a-zA-Z0-9\.#]',
        "ASSIGN" : r'\:',
        "BLOCK_OPEN" : r'\[',
        "BLOCK_CLOSE" : r']'
    }

    tokens = {
        "WHITESPACE" : r'[ \n\t\r]',
        "KEYWORD" : r'(Instrument|Notes|Oscillator)',
        "ASSIGN" : r'\:',
        "VALUE" : r'([0-9])',
        "BLOCK_OPEN" : r'\[',
        "BLOCK_CLOSE" : r'\]',
        "IDENTIFIER" : r'[a-zA-Z_][a-zA-Z_0-9]*',
        "NOTE_IDENTIFIER" : r'(\.+)|([a-z]([0-9]|#|(maj|min)[0-9])?)'
    }

    tokenCnt = 0
    foundTokens = []
    scanComplete = False

    def __init__(self):
        pass


    def scan(self, inputString=""):
        t = 0
        tok = ""
        blockLevel = 0

        while(t < len(inputString)):

            c = inputString[t]

            if(re.match(self.matchExpr.get("WHITESPACE"), str(c))):
                pass
            elif(re.match(self.matchExpr.get("NAME"), str(c))):
                #Try to read name
                while(re.match(self.matchExpr.get("NAME"), inputString[t])):
                    tok += inputString[t]
                    t+=1
                if re.match(self.tokens.get("KEYWORD"), tok):
                    self.foundTokens.append(["KEYWORD", tok])
                elif re.match(self.tokens.get("VALUE"), tok):
                    self.foundTokens.append(["VALUE", tok])
                elif re.match(self.tokens.get("NOTE_IDENTIFIER"), tok):
                    self.foundTokens.append(["NOTE", tok])
                elif re.match(self.tokens.get("IDENTIFIER"), tok):
                    self.foundTokens.append(["IDENTIFIER", tok])
                else:
                    raise Exception("Illegal character sequence found at " + str(t))
                tok = ""
                continue
            elif(re.match(self.matchExpr.get("ASSIGN"), str(c))):
                #Try to read assign
                self.foundTokens.append(["ASSIGN", ":"])
            elif(re.match(self.matchExpr.get("BLOCK_OPEN"), str(c))):
                #Open block
                blockLevel+=1
                self.foundTokens.append(["BLOCK_OPEN", str(blockLevel)])
            elif(re.match(self.matchExpr.get("BLOCK_CLOSE"), str(c))):
                #Close block
                self.foundTokens.append(["BLOCK_CLOSE", str(blockLevel)])
                openBlock = False
                blockLevel -= 1
                if blockLevel < 0:
                    raise Exception("Wrong indentation at position: " + str(t))
            else:
                raise Exception("Illegal character sequence/symbol at position " + str(t) + ": " + c)

            t += 1

        if blockLevel != 0:
            raise Exception("Missing closing bracket ] for block(s)")

        self.scanComplete = True
        print(self.foundTokens)


    def next(self):
        if self.scanComplete:
            self.tokenCnt+=1
            if(self.tokenCnt <= len(self.foundTokens)):
                return self.foundTokens[self.tokenCnt-1]
        return None