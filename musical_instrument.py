from playsound import playsound

class MusicalInstrument:

    def __init__(self, typ, name):
        self.typ = typ
        self.notes = {}
        self.name = name

    def play(self, seq, bar):
        if bar >= len(self.notes[str(seq)]): return False
        try:
            print(self.name + ": " + str(self.notes[str(seq)][bar]))
            try:
                #playsound("data/piano/" + str(self.notes[str(seq)][bar]) + ".mp3")
                playsound("data/piano/c3.wav", True)
            except:
                pass
            return True
        except IndexError:
            return False
" + str(self.notes[str(seq)][bar]) + "