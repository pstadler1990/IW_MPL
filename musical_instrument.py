class MusicalInstrument:

    def __init__(self, typ, name, sound_ref):
        self.typ = typ
        self.notes = {}
        self.name = name
        self.sound = sound_ref

    def play(self, seq, bar):
        if bar >= len(self.notes[str(seq)]):
            return False
        try:
            #print(self.name + ": " + str(self.notes[str(seq)][bar]))
            return self.sound.play_sound(str(self.notes[str(seq)][bar]))
        except IndexError:
            return False
