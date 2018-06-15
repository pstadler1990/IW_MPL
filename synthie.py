#!/usr/bin/python
import lexer
import grammar
import sys
from playback import Playback

#TODO: Would be nice to have variables for notes as well, i.e.  my_riff: [c3 c4 c3 . c4]
#                                                               Notes Intro [ my_riff ]

class Synthie:

    def __init__(self, file):
        with open(file, 'r') as f:
            data = f.read()
        l = lexer.Lexer()
        l.scan(data)

        g = grammar.Grammar(l)
        status = g.parse()
        if status:
            """Begin playback"""
            song = g.get_song()
            instruments = g.get_instruments()
            bpm = g.stack["BPM"]
            playback = Playback(song, instruments, bpm)
            playback.play()


if __name__ == "__main__":
    sys.argv.append("example.syn")
    if len(sys.argv) > 1:
        s = Synthie(str(sys.argv[1]))
    else:
        print("ERROR. No script file given.")
        print("----------------------------")
        print("Usage: ")
        print("python3 synthie.py <your-file.syn>")
        print("Example: python3 synthie.py example.syn")
