import lexer
import grammar

#TODO: - Add stack with predefined variables, like BPM
#TODO: - Add rules and grammar (each slot needs to be a specific type)
#TODO: - Add function pointer, call from rule (to remove if-/else path)

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
        ]""")

        g = grammar.Grammar()
        g.parse(l)



if (__name__ == "__main__"):
    s = Synthie()
