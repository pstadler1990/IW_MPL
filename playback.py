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

        self.convert_song()

    def convert_song(self):
        instrument_dict = {}
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
                            instrument = MusicalInstrument(tmp_itype)
                            self.playback_list.append(instrument)
                        else:
                            print("error...instrument song playback")
            #TODO: Convert the InstrumentName.PieceName into notes and assign these to the instrument notelist (each sequence is a new append!)

    def get_instrument_type_by_name(self, name):
        tmp = self.instruments[name].variables["IType"][0]
        if tmp is not None:
            return tmp
        else:
            return -1

    def play(self):
        bar = 0
        seq = 0
        delay_time_ms = ceil(60000 / int(self.bpm))
        delay_time_s = delay_time_ms / 1000

        while seq is not self.sequences:
            print("play bar " + str(bar) + " at seq: " + str(seq))
            if bar < 3:
                bar += 1
            else:
                bar = 0
                seq += 1
                #TODO: this is just a test; a sequence is only finished, if the last note of it has been played!!
            sleep(delay_time_s)
