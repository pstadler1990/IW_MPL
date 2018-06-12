# IW_MPL
Informationswissenschaft Python Projekt: Music Programming Language

Important notes
===============
Variable names MUST start with a CAPITAL letter!

Some examples of valid variable names in IW_MP:
`MyVariable: 3`
`NEWTYPE: BASS`

Invalid variable names are note identifiers, keywords and variables not starting with a capital letter and/or containing
other characters than `a-z A-Z 0-9 _`

Examples of invalid variable names:
`myVariable: 3`
`c3: 4`

It is also forbidden to use keywords as the beginning of a variable name, like:
`Instrument2: 4`

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

## Comments
You can write comments by using a semicolon.

Note: The comment reaches until the next line break, so any
code after a comment will also be ignored!

Example comment:
`BPM: 80    ;This is my example comment on this variable assignment`

## Arranging songs
To create a song, you have to arrange a sequence of music pieces together. This can be done with the Song keyword:

`Song Example [
    Piano.Intro + Harp.Intro, Harp.Intro, Piano.Chorus + Piano.Outro
]`

where a plus sign (+) plays multiple pieces in parallel, while a comma (,) starts a new sequence.

You refer to a specific music piece by writing the instrument's name and the name of the notelist, concatenated by a dot (.).
