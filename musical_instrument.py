class MusicalInstrument:

    def __init__(self, typ, name):
        self.typ = typ
        self.notes = {}
        self.name = name

    def play(self, seq, bar):
        if bar >= len(self.notes[str(seq)]): return False
        try:
            print(self.name + ": " + str(self.notes[str(seq)][bar]))
            return True
        except IndexError:
            return False
