from pygame import mixer
from time import sleep

class Sound:

    def __init__(self, number_of_instruments, delay_s):
        self.number_of_channels = number_of_instruments * 4     #Create enough channels for a clean playback, so multiply real amount by 4
        mixer.init()
        mixer.set_num_channels(self.number_of_channels)
        self.sound_dict = {}
        self.delay_time_s = delay_s
        self.channel_list = []
        for i in range(0, self.number_of_channels):
            self.channel_list.append(mixer.Channel(i))
        self.current_channel = self.channel_list[0]

    def preload_sound(self, note_identifier):
        if note_identifier is not "." and note_identifier not in self.sound_dict:
            #TODO: Remove hardcoded piano from sound_file and replace it with correct instrument
            sound_file = "data/piano/" + note_identifier + ".wav"
            try:
                self.sound_dict[note_identifier] = mixer.Sound(file=sound_file)
            except:
                print("Unknown sound file!")

    def play_sound(self, note_identifier):
        if note_identifier in self.sound_dict:
            self.current_channel.play(self.sound_dict[note_identifier])
            self.current_channel = self.get_next_channel()
            return True

    def get_next_channel(self):
        idx = self.channel_list.index(self.current_channel)
        if idx + 1 > len(self.channel_list):
            idx = 0
        else:
            idx += 1
        return self.channel_list[idx]