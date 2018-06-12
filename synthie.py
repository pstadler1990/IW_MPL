import lexer
import grammar

#TODO: Would be nice to have variables for notes as well, i.e.  my_riff: [c3 c4 c3 . c4]
#TODO:                                                          Notes Intro [ my_riff ]

class Synthie:

    def __init__(self):
        l = lexer.Lexer()
        l.scan("""
        BPM: 80
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
        Horst: BPM
        """)

        g = grammar.Grammar(l)
        g.parse()


if __name__ == "__main__":
    s = Synthie()
