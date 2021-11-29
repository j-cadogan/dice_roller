

""" Tests for rolls.py """

from subprocess import getstatusoutput
import os
import re
import random
import string

PRG = './rolls.py'
CHAR1 = 'inputs/cleric.txt'
CHAR2 = 'inputs/rogue.txt'
BAD_CHAR = 'inputs/bad.txt'

# --------------------------------------------------
def random_filename():
    """ Generate random filename """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# --------------------------------------------------
def test_exists():
    """Check if the program exists"""
    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Prints usage """
    for flag in ['-h', '--help']:
        rv, out = getstatusoutput('{} {}'.format(PRG, flag))
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_no_args():
    """ Dies on no args """
    rv, out = getstatusoutput(PRG)
    assert rv != 0
    assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_file():
    """ Dies on bad file """
    bad = random_filename()
    rv, out = getstatusoutput('{} {} {} {} {}'.format(
        PRG, bad, 'pers', 'check', '-s 10'
    ))


# --------------------------------------------------
def test_non_int_value():
    """ Raises error and breaks if non-int value found in character file """
    expected = f'Non-integer value found in {BAD_CHAR}.'
    rv, output = getstatusoutput(f'{PRG} {BAD_CHAR} str c')
    assert rv != 0
    assert output == expected


# --------------------------------------------------
def test_adv_and_disadv():
    """ Dies on using -d and -a flags at the same time """
    rv, out = getstatusoutput(f'PRG, CHAR1, str check -a -d -s 3')
    assert rv != 0


# --------------------------------------------------
def test_1():
    """ Test basic saving throw, no proficiency """
    expected = ["You made a Strength save.",
                "",
                "Your total is 9.",
                "You rolled a 8 on the d20 with a +1 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR1} str save -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected


# --------------------------------------------------
def test_2():
    """ Test basic saving throw with full ability name and proficiency """
    expected = ["You made a Dexterity save.",
                "",
                "Your total is 18.",
                "You rolled a 8 on the d20 with a +10 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR2} dexterity save -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected


# --------------------------------------------------
def test_3():
    """ test basic ability check with full ability name """
    expected = ["You made a Charisma check.",
                "",
                "Your total is 8.",
                "You rolled a 8 on the d20 with a +0 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR1} charisma a -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected

# --------------------------------------------------
def test_4():
    """ test skill check with full skill name and proficiency"""
    expected = ["You made an Intimidation check.",
                "",
                "Your total is 16.",
                "You rolled a 8 on the d20 with a +8 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR2} intimidation c -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected


# --------------------------------------------------
def test_5():
    """ test saving throw with advantage and negative modifier """
    expected = ["You made an Intelligence save with advantage.",
                "",
                "Your total is 18.",
                "You rolled a 8 and a 19 on the d20 with a -1 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR1} intelligence save -a -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected


# --------------------------------------------------
def test_6():
    """ test skill check with disadvantage and expertise """
    expected = ["You made a Stealth check with disadvantage.",
                "",
                "Your total is 23.",
                "You rolled a 8 and a 19 on the d20 with a +15 modifier."]
    rv, output = getstatusoutput(f'{PRG} {CHAR2} ste skill -d -s 3')
    assert rv == 0
    assert output.strip().splitlines() == expected