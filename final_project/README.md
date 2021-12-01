# Final project: rolls.py
This program rolls ability checks, skill checks, and saving throws according to Dungeons & Dragons 5th Edition rules.

## A Quick D&D Dice-Rolling Primer
Dungeons and Dragons (D&D) is a pen-and-paper tabletop roleplaying game in which a group of players each creates their own character with scores in six key statistics. In order to avoid presuming familiarity with game mechanics, here's a brief explanation of dice rolls from the Player's Handbook, in case you want some idea of what's actually going on and why:
> In cases where the outcome of an action is uncertain, the&hellip;game relies on rolls of a 20-sided die, a d20, to determine success or failure.
> 
> Every character in the game has capabilities defined by six <b>ability scores</b>. The abilities are Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma, and they typically range from 3 to 18 for most [characters]&hellip;These ability scores, and the <b>ability modifiers</b> derived from them, are the basis for almost every d20 roll that a player makes on a character's behalf. (<i>Player's Handbook</i>, pg. 7)



There are three steps to each dice roll, but to understand this program, you only need to know the first one: roll the 20-sided die and add a particular modifier. The goal of this program is simply to determine what kind of roll the user would like to make, what modifiers to add to that roll, and then to actually, you know, roll the dice and add the mods.


## Requirements
One input file is required in order to run rolls.py. This file should be a text file containing four lines:
1. The character's proficiency bonus.
2. The character's ability scores
3. The saving throws the character is proficient in.
4. The skills the character is proficient in.

### A note on formatting:
The formatting of the text file is key, and if users create a version for their own character(s), they should follow the format of the provided example file as closely as possible.

Line 1 should only have the character's proficiency bonus.

Line 2 should have their ability scores.

Line 3 should have their save proficiencies.

Line 4 should have skill proficiencies.

Lines 2, 3, and 4 should be in a dictionary-like format, with the keys being abilities/skills and values being integers.

The values for lines 3 and 4 should either be a 1 or a 2. 1 indicates proficiency in that skill/save. 2 indicates expertise. If a skill or save isn't present, that indicates no proficiency.

When run with no arguments, the program will produce a usage statement.
```
$ ./rolls.py
usage: rolls.py [-h] [-a | -d] [-s seed] FILE STR STR
rolls.py: error: the following arguments are required: FILE, STR, STR
```

When run with the -h or --help flag, a longer help document should be printed.
```
$ ./rolls.py -h
usage: rolls.py [-h] [-a | -d] [-s seed] FILE STR STR

Rock the Casbah

positional arguments:
  FILE                  .txt with character info and stats
  STR                   What skill or ability to roll for
  STR                   The type of roll to make (ability or save)

optional arguments:
  -h, --help            show this help message and exit
  -a, --advantage       Roll twice and take the higher number (default: False)
  -d, --disadvantage    Roll twice and take the lower number (default: False)
  -s seed, --seed seed  Optional seed value for testing (default: None)
```

If the file is not valid: 
```
$ ./rolls.py inputs/foo.txt
usage: rolls.py [-h] [-a | -d] [-s seed] FILE STR STR
rolls.py: error: argument FILE: can't open 'inputs/foo.txt': [Errno 2] No such file or directory: 'inputs/foo.txt'
```

If the input for the roll_type or roll_for arguments isn't in the list of acceptable terms:
```
$ ./rolls.py inputs/cleric.txt const save
usage: rolls.py [-h] [-a | -d] [-s seed] FILE STR STR
rolls.py: error: argument STR: invalid choice: 'const' (choose from 'str', 'strength', 'dex', 'dexterity', 'con', 'constitution', 'int', 'intelligence', 'wis', 'wisdom', 'cha', 'charisma', 'acrobatics', 'acr', 'animal handling', 'anh', 'arcana', 'arc', 'athletics', 'ath', 'deception', 'dec', 'insight', 'ins', 'intimidation', 'intim', 'investigation', 'inv', 'medicine', 'med', 'nature', 'nat', 'perception', 'perc', 'performance', 'perf', 'persuasion', 'pers', 'religion', 'rel', 'sleight of hand', 'soh', 'stealth', 'ste', 'survival', 'sur')
```

If the user tries to use the -a | --advantage and -d | --disadvantage flags concurrently, the program will exit and produce an error.
```
$ ./rolls.py inputs/cleric.txt con save -a -d
usage: rolls.py [-h] [-a | -d] [-s seed] FILE STR STR
rolls.py: error: argument -d/--disadvantage: not allowed with argument -a/--advantage
```

If the values in the input file cannot be converted to integers, the program will exit with an error message prompting the user to correct the input file.
```
$ ./rolls.py inputs/bad.txt con save
Non-integer value found in inputs/bad.txt.
```

### Arguments
There's quite a few flags for rolls.py, but those familiar with typical D&D terms should find them fairly intuitive. However, if a user is unfamiliar, a more thorough explanation for each argument might be useful.

1. <b>character:</b> already extensively covered. 
2. <b>roll_for:</b> the user may roll for one of the six base abilities (strength, wisdom, charisma, etc), or a particular skill (athletics, insight, persausion, etc.) The reason for differentiating between abilities and skills is a bit too baroque to get into in a README, but it is important.
3. <b>roll_type:</b> the user may choose to make either a check or a saving throw (often called a save). Again, differentiating between the two isn't especially necessary in here; you just need to know that they're slightly different game mechanics.
4. <b>-a | --advantage and -d | --disadvantage:</b> certain situations in a game might require a player to roll a d20 twice and use the higher or lower number. This is called (dis)advantage. So, I created two mutually exclusive optional boolean arguments to represent that mechanic.
5. <b>-s | --seed</b>: this is purely for testing; since rolling dice is necessarily random, the optional seed argument is used to keep outputs consistent. Or, you know, you could use it to rig your dice rolls if you really wanted to, I guess?

Finally, the wording and ordering of these arguments are deliberate. In a game, the player running the session might tell you to "make a stealth check with disadvantage" or to "roll a wisdom saving throw". This phrasing is very typical, and the ordering of the arguments is meant to mimic it. So, those examples could be entered as:

./rolls.py inputs/rogue.txt stealth check -d
```
$ ./rolls.py inputs/rogue.txt stealth check -d

You made a Stealth check with disadvantage.

Your total is 17.
You rolled a 2 and a 16 on the d20 with a +15 modifier.
```

and

./rolls.py inputs/cleric.txt wisdom save
```
$ ./rolls.py inputs/cleric.txt wisdom save

You made a Wisdom save.

Your total is 11.
You rolled a 2 on the d20 with a +9 modifier.
```

## Author
Jaclyn Cadogan

jaclyncadogan@gmail.com
