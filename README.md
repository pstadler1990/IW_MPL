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