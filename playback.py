class Playback:

    def __init__(self, song, instruments):
        """A playback object needs:
            - a song to play (global variable)
            - a list of music pieces containing the instrument.piece identifier
                => this list must be converted into the corresponding note lists
            - a BPM
        """
        self.song = song
        self.instruments = instruments
