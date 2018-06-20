# IW_MPL
Informationswissenschaft Python Projekt: Music Programming Language

What it is
==========
IW_MPL is a first approach to a music (or audio) programming language (Wikipedia https://en.wikipedia.org/wiki/List_of_audio_programming_languages). It is a very simple concept and only includes some basic functionality, but it is fully usable for creating and playing easy songs.

What it's not
=============
Unlike ChucK (http://chuck.cs.princeton.edu/), IW_MPL does not contain any programming logic or conditional expressions, like if or while. Basically, IW_MPL is just a small interpreted language that gets converted into notes.

How to use
==========
A valid IW_MPL script consists of (at least) three parts:
1. An instrument
2. Some notes
3. A Song

Creating an instrument
======================
Use the `Instrument` keyword to create a new instrument block.
IW_MPL expects to find an identifier after the `Instrument` keyword, like `Instrument Piano`. 
To specify your instrument, you need to encapsulate it with a block statement `[ ]` (everything between two square brackets is considered a block).

Example:
```
 Instrument Piano [
    ; your instrument details    
 ]
```

Adding notes
============
Each instrument must at least provide one list of notes, identified by the `Notes` keyword, also encapsulated by a block.
You also need to give your notes an identifier. 

Example:
```
Instrument Piano [
        Notes MyNotes [
            ; your notes here
        ]
]
```

Notes
=====
Inside a notes block, you are free to write note names. 
Currently, IW_MPL only supports the following notes:
```
c1 c2 c3 c4 c5 d1 d2 d3 d4 e1 e2 e3 d4 f1 f2 f3 f4 g1 g2 g3 g4 a1 a2 a3 a4 b1 b2 b3 b4
```
and rest `.` (a dot is basically just a skip-the-current-bar note)

Example:
```
Instrument Piano [
        Notes MyNotes [
            c3 d3 e3 f3 g3 . g3 . a3 a3 a3 a3 g3
        ]
]

Arranging songs
===============
To create a song, you have to arrange a sequence of music pieces together. This can be done with the Song keyword:

`Song Example [
    Piano.Intro + Harp.Intro, Harp.Intro, Piano.Chorus + Piano.Outro
]`

where a plus sign (+) plays multiple pieces in parallel, while a comma (,) starts a new sequence.

You refer to a specific music piece by writing the instrument's name and the name of the notelist, concatenated by a dot (.).

PLAY
====
Finally, use the `Play` keyword, to play a specific song.
Example: `Play Example` where example is the name of the song.


Important notes
===============
Variable names MUST start with a CAPITAL letter!

Some examples of valid variable names in IW_MPL:
`MyVariable`
`NEWTYPE`

Invalid variable names are note identifiers, keywords and variables not starting with a capital letter and/or containing
other characters than `a-z A-Z 0-9 _`

Examples of invalid variable names:
`myVariable`
`c3`

It is also forbidden to use keywords as the beginning of a variable name, like:
`Instrument2`

## Assigning values to variables
You can assign any numeric values to a variable:
`MyVar: 5`

You can then assign your variable to another variable:
`MyOtherVar: MyVar`
MyOtherVar will contain the value of MyVar, so 5.

Currently, IW_MPL only supports numeric values for its variables.

## Constants
There are some constant values already assigned:
`PIANO = 1`
`BASS = 2`
`SYNTHESIZER = 3`

These constants can be used as a variable for your instrument's IType variable:
`IType: PIANO`
assigns the piano instrument to your current instrument block.

However, you can modify each of your variables by prepending the `const` keyword, like:
`const MyVar: 3`
A constant can only be assigned once and never changed again.

## Comments
You can write comments by using a semicolon.

Note: The comment reaches until the next line break, so any
code after a comment will also be ignored!

Example comment:
`BPM: 80    ;This is my example comment on this variable assignment`

