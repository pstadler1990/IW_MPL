from musical_instrument import MusicalInstrument
from time import sleep
from math import ceil


class Playback:

    def __init__(self, song, instruments, bpm):
        self.sequences = 0
        self.song = song
        self.instruments = instruments
        self.bpm = bpm[0]
        self.playback_list = []


    def convert_song(self):
        #TODO: Add check, if the notes are already in the current sequence, if they are added by a + (plus)
        instrument_dict = {}
        seq = 0
        current_instrument = None
        for i in self.song.pieces:
            if type(i) == list:
                self.sequences += 1
                for j in i:
                    tmp = j.split(".")
                    tmp_instrument = tmp[0]
                    tmp_piece = tmp[1]
                    if tmp_instrument not in instrument_dict:
                        tmp_itype = self.get_instrument_type_by_name(tmp_instrument)
                        if tmp_itype is not -1:
                            instrument_dict[tmp_instrument] = tmp_itype
                            instrument = MusicalInstrument(tmp_itype, tmp_instrument)
                            self.playback_list.append(instrument)
                            current_instrument = instrument
                        else:
                            return False
                    else:
                        current_instrument = self.find_instrument_by_name(tmp_instrument)

                    """Add notes from current piece to instrument list at specific index"""
                    notes = self.get_notes_by_instrument_and_piece(tmp_instrument, tmp_piece)
                    if current_instrument is not None:
                        current_instrument.notes[str(seq)] = notes
            seq += 1
        return True

    def get_instrument_type_by_name(self, name):
        tmp = self.instruments[name].variables["IType"][0]
        if tmp is not None:
            return tmp
        else:
            return -1

    def get_notes_by_instrument_and_piece(self, instrument, piece):
        return self.instruments[instrument].notes[piece]

    def find_instrument_by_name(self, instrument):
        for i in self.playback_list:
            if i.name == instrument:
                return i

    def find_max_number_of_notes_in_piece(self, seq):
        max_nr = 0
        for i in self.playback_list:
            try:
                if len(i.notes[str(seq)]) > max_nr:
                    max_nr = len(i.notes[str(seq)])
            except KeyError:
                pass
        return max_nr

    def play(self):
        bar = 0
        seq = 0
        delay_time_ms = ceil(60000 / int(self.bpm))
        delay_time_s = delay_time_ms / 1000
        max_notes = self.find_max_number_of_notes_in_piece(seq)
        print("Starting playback")

        while seq <= self.sequences:
            """Play note"""
            for i in self.playback_list:
                try:
                    if i.notes[str(seq)] is not None:
                        if len(i.notes[str(seq)]) >= bar:
                            i.play(seq, bar)
                except KeyError:
                    pass

                if bar >= max_notes:
                    seq += 1
                    bar = 0
                    max_notes = self.find_max_number_of_notes_in_piece(seq)
            bar += 1
            sleep(delay_time_s)
        return True
