import re
import tok
import collections

nextToken = collections.namedtuple('nextToken','token token_count')


class Lexer(object):

    matchExpr = {
        "WHITESPACE": r'[ \n\t\r]',
        "NAME": r'[a-zA-Z0-9\.#]',
        "ASSIGN": r'\:',
        "BLOCK_OPEN": r'\[',
        "BLOCK_CLOSE": r']'
    }

    tokens = {
        "WHITESPACE": r'[ \n\t\r]',
        "KEYWORD": r'(Instrument|Notes|Oscillator)',
        "ASSIGN": r'\:',
        "VALUE": r'([0-9])',
        "BLOCK_OPEN": r'\[',
        "BLOCK_CLOSE": r'\]',
        "IDENTIFIER": r'[a-zA-Z_][a-zA-Z_0-9]*',
        "NOTE_IDENTIFIER": r'(\.+)|([a-z]([0-9]|#|(maj|min)[0-9])?)'
    }

    tokenCnt = 0
    foundTokens = []
    scanComplete = False


    def __init__(self):
        pass


    def scan(self, inputString=""):
        t = 0
        tokn = ""
        blockLevel = 0

        while t < len(inputString):

            c = inputString[t]

            if c.isspace():
                pass

            elif re.match(self.matchExpr.get("NAME"), str(c)):

                while re.match(self.matchExpr.get("NAME"), inputString[t]):
                    tokn += inputString[t]
                    t += 1

                if re.match(self.tokens.get("KEYWORD"), tokn):
                    self.foundTokens.append(tok.Tok(tok.KEYWORD, tokn))
                elif re.match(self.tokens.get("VALUE"), tokn):
                    self.foundTokens.append(tok.Tok(tok.VALUE, tokn))
                elif re.match(self.tokens.get("NOTE_IDENTIFIER"), tokn):
                    self.foundTokens.append(tok.Tok(tok.NOTE_IDENTIFIER, tokn))
                elif re.match(self.tokens.get("IDENTIFIER"), tokn):
                    self.foundTokens.append(tok.Tok(tok.IDENTIFIER, tokn))
                else:
                    raise Exception("Illegal character sequence found at " + str(t))

                tokn = ""
                continue

            elif re.match(self.matchExpr.get("ASSIGN"), str(c)):
                self.foundTokens.append(tok.Tok(tok.ASSIGN, tokn))

            elif re.match(self.matchExpr.get("BLOCK_OPEN"), str(c)):
                blockLevel += 1
                self.foundTokens.append(tok.Tok(tok.BLOCK_OPEN, tokn))

            elif re.match(self.matchExpr.get("BLOCK_CLOSE"), str(c)):
                self.foundTokens.append(tok.Tok(tok.BLOCK_CLOSE, tokn))
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

    def next(self):
        if self.scanComplete and self.hasNext():
            retTok = self.foundTokens[self.tokenCnt]
            retCnt = self.tokenCnt
            self.tokenCnt += 1
            return nextToken(token=retTok, token_count=retCnt)
        return None

    def reset(self, tokenCnt):
        self.tokenCnt = tokenCnt

    def hasNext(self):
        return self.tokenCnt < len(self.foundTokens)

    def eat(self, current_token, token_type):
        if self.scanComplete and self.hasNext():
            if current_token == token_type:
                return self.next()