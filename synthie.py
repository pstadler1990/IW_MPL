import lexer
import grammar

#TODO: - Add stack with predefined variables, like BPM and Piano

class Synthie:

    def __init__(self):
        l = lexer.Lexer()
        l.scan("""BPM: 80
        Instrument Piano [
            Notes Intro [
                c3 c4 c3 . c7 a b# b7 . c3 c4 .. bmaj7
            ]
            Notes Chorus [
                c4 c4 . c4 . cmaj7
            ]
            Notes Outro [
                . . . . . . . cmaj7 b# b7 c3 . c4 ....
            ]
            IType: PIANO
            Horst: 3
        ]
        BPM: 70
        Horst: 5
        """)

        g = grammar.Grammar(l)
        g.parse()



if (__name__ == "__main__"):
    s = Synthie()
