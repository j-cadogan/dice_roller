#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-28
Purpose: Roll saving throws, ability checks, and skill checks
         according to Dungeons & Dragons 5th Edition rules.
"""

import argparse
import random
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    skills_and_abilities = ['str', 'strength', 'dex', 'dexterity', 'con',
                            'constitution', 'int', 'intelligence', 'wis',
                            'wisdom', 'cha', 'charisma', "acrobatics", "acr",
                            "animal handling", "anh", "arcana", "arc",
                            "athletics", "ath", "deception", "dec", "insight",
                            "ins", "intimidation", "intim", "investigation",
                            "inv", "medicine", "med", "nature", "nat",
                            "perception", "perc", "performance", "perf",
                            "persuasion", "pers", "religion", "rel",
                            "sleight of hand", "soh", "stealth",
                            "ste", "survival", "sur", 'surv']

    roll_types = ['save', 's', 'saving throw', 'ability',
                  'a', 'skill', 'check', 'c']

    parser.add_argument('character',
                        help='.txt with character info and stats',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('roll_for',
                        metavar='STR',
                        help='What skill or ability to roll for',
                        choices=skills_and_abilities)

    parser.add_argument('roll_type',
                        metavar='STR',
                        help='The type of roll to make (ability or save)',
                        choices=roll_types)

    dis_adv = parser.add_mutually_exclusive_group()
    dis_adv.add_argument('-a',
                         '--advantage',
                         help='Roll twice and take the higher number',
                         action='store_true')

    dis_adv.add_argument('-d',
                         '--disadvantage',
                         help='Roll twice and take the lower number',
                         action='store_true')

    parser.add_argument('-s',
                        '--seed',
                        metavar='seed',
                        help='Optional seed value for testing',
                        type=int)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    roll_for = args.roll_for
    roll_type = args.roll_type
    adv = args.advantage
    disadv = args.disadvantage
    file_name = args.character.name

    abbrevs = {'strength': 'str', 'dexterity': 'dex', 'constitution': 'con',
               'intelligence': 'int', 'wisdom': 'wis', 'charisma': 'cha',
               "acrobatics": "acr", "animal handling": "anh", "arcana": "arc",
               "athletics": "ath", "deception": "dec", "insight": "ins",
               "intimidation": "intim", "investigation": "inv", "medicine":
               "med", "nature": "nat", "perception": "perc", "performance":
               "perf", "persuasion": "pers", "religion": "rel",
               "sleight of hand": "soh", "stealth": "ste", "survival": "sur"}

    # read args.character
    for i, line in enumerate(args.character):
        if i == 0:
            try:
                prof_bonus = int(line.strip())
            except:  # pylint: disable=W0702
                sys.exit(f'Non-integer value found in {file_name}.')
        elif i == 1:
            scores = read_dict(line, file_name)
        elif i == 2:
            save_profs = read_dict(line, file_name)
        elif i == 3:
            skill_profs = read_dict(line, file_name)

    # determine if the roll is an ability check or saving throw,
    # then use the appropriate dictionary of proficiencies
    if roll_type in ['save', 's', 'saving throw']:
        roll_type = 'save'
        relevant_profs = save_profs
    elif roll_type in ['ability', 'a', 'skill', 'check', 'c']:
        roll_type = 'check'
        relevant_profs = skill_profs

    # calculate roll and print results to stdout
    roll_for = std_abbrev(roll_for, abbrevs)
    ability = determine_ability(roll_for)
    prof = calc_prof(roll_for, relevant_profs, prof_bonus)
    pos_neg, mod = calc_mod(scores, ability, prof)
    rolls = roll_dice(adv, disadv, args.seed)
    print_header(roll_for, roll_type, adv, disadv, abbrevs)
    calc_total(rolls, pos_neg, mod)


# --------------------------------------------------
def read_dict(line, file_name):
    """
    Read lines from character .txt file into dicts.
    Turns values into ints when possible.
    dictionary: dict to be returned
    pairs: key-value pairs
    pair[1]: key
    pair[2]: value
    """
    dictionary = {}
    pairs = line.strip().split(', ')
    for i in pairs:
        pair = i.split(":")
        try:
            pair[1] = int(pair[1])
        except:  # pylint: disable=W0702
            sys.exit(f'Non-integer value found in {file_name}.')
        dictionary[pair[0]] = pair[1]
    return dictionary


# --------------------------------------------------
def test_read_dict():
    """ test read_dict() """
    assert read_dict("int:8, wis:20, cha:10", 'file.py') \
        == {"int": 8, "wis": 20, "cha": 10}


# --------------------------------------------------
def std_abbrev(roll_for, abbrevs):
    """
    Standardize ability and skill notation to typical 5e abbreviations.
    roll_for: ability/skill being rolled for
    abbrevs: dict of {full names: abbreviated names}
    """

    if abbrevs.get(roll_for):
        return abbrevs[roll_for]

    return roll_for


# --------------------------------------------------
def test_std_abbrev():
    """ test std_abbrev() """
    ab = {'constitution': 'con', 'intelligence': 'int', 'wisdom': 'wis',
          "animal handling": "anh", "intimidation": "intim",
          "persuasion": "pers"}

    assert std_abbrev("wisdom", ab) == 'wis'
    assert std_abbrev("con", ab) == "con"
    assert std_abbrev("animal handling", ab) == "anh"
    assert std_abbrev("intelligence", ab) == 'int'
    assert std_abbrev("intimidation", ab) == 'intim'
    assert std_abbrev("pers", ab) == "pers"


# --------------------------------------------------
def determine_ability(roll_for):  # pylint: disable=R1710
    """ determine which ability is being used for the roll """
    ability_tbl = {'str': ['str', 'ath'],
                   'dex': ['dex', 'acr', 'soh', 'ste'],
                   'con': ['con'],
                   'int': ['int', 'arc', 'inv', 'nat', 'rel'],
                   'wis': ['wis', 'anh', 'ins', 'med', 'perc', 'sur'],
                   'cha': ['cha', 'dec', 'intim', 'perf', 'pers']}

    for k, _ in ability_tbl.items():
        if roll_for in ability_tbl[k]:  # pylint: disable=R1733
            return ability_tbl[k][0]  # pylint: disable=R1733


# --------------------------------------------------
def test_determine_ability():
    """ test determine_ability() """
    assert determine_ability('con') == 'con'
    assert determine_ability('dec') == 'cha'
    assert determine_ability('dex') == 'dex'
    assert determine_ability('sur') == 'wis'


# --------------------------------------------------
def calc_prof(ability, profs, prof_bonus):
    """
    Determine if proficiency modifier needs to be applied.
    If character has expertise in selected skill, double the proficiency bonus.
    If character has proficiency in selected skill/ability/save,
        prof_mod = prof_bonus (multiply by 1).
    If character has no proficiency in selected skill/ability/save,
        prof_mod = 0 (no bonus).
    """
    if ability in profs.keys():
        prof_mod = profs[ability] * int(prof_bonus)
    else:
        prof_mod = 0

    return prof_mod


# --------------------------------------------------
def test_calc_prof():
    """ test calc_prof() """
    save_profs_cleric = {"wis": 1, "cha": 1}
    save_profs_rogue = {"dex": 1, "int": 1}
    save_profs_none = {}
    skill_profs_none = {}
    skill_profs_rogue = {"ste": 2, "soh": 2, "perc": 1, "dec": 1}

    assert calc_prof("cha", save_profs_cleric, 4) == 4
    assert calc_prof("str", save_profs_rogue, 2) == 0
    assert calc_prof("con", save_profs_none, 3) == 0
    assert calc_prof("perf", skill_profs_none, 5) == 0
    assert calc_prof("ste", skill_profs_rogue, 6) == 12
    assert calc_prof("perc", skill_profs_rogue, 3) == 3


# --------------------------------------------------
def calc_mod(scores, ability, prof_mod):
    """
    Calculate total modifider. If modifier is positive, add a + before it.
    scores: dictionary of ability scores.
    ability: ability used for roll.
    prof_mod: amount to be added based on proficiency. Always 0 or
        more.
    mod: total modifier to be added to base d20 roll. Can be positive
        or negative.
    pos_neg: "+" if modifier is 0 or greater, empty string if less than 0,
        since a "-" will automatically be used. Typical 5e notation.
    """
    # modifier equation
    mod = int((scores[ability] - 10) / 2 + prof_mod)

    # if modifier is 0 or greater, add a + sign in front.
    if mod >= 0:
        pos_neg = "+"
    else:
        pos_neg = ""

    return pos_neg, mod


# --------------------------------------------------
def test_calc_mod():
    """ test calc_mod() """
    scores_standard = {'str': 15, 'dex': 14, 'con': 13, 'int': 12,
                       'wis': 10, 'cha': 8}
    scores_negative = {'str': 9, 'dex': 8, 'con': 7, 'int': 6,
                       'wis': 5, 'cha': 4}
    scores_high = {'str': 20, 'dex': 19, 'con': 18, 'int': 17,
                   'wis': 16, 'cha': 15}

    assert calc_mod(scores_standard, "str", 0) == ("+", 2)
    assert calc_mod(scores_negative, "dex", 0) == ("", -1)
    assert calc_mod(scores_high, "con", 0) == ("+", 4)
    assert calc_mod(scores_negative, "int", 2) == ("+", 0)
    assert calc_mod(scores_standard, "wis", 0) == ("+", 0)
    assert calc_mod(scores_high, "cha", 6) == ("+", 8)
    assert calc_mod(scores_negative, "cha", 2) == ("", -1)


# --------------------------------------------------
def roll_dice(adv, disadv, seed):
    """
    Roll the dice. If advantage or disadvantage flags are used,
    roll the d20 twice and take the higher/lower number.
    """
    if seed:
        random.seed(seed)

    if adv or disadv:
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        if adv:
            roll = max(roll1, roll2)
        else:
            roll = min(roll1, roll2)
        return [roll, roll1, roll2]

    roll = random.randint(1, 20)
    return [roll]


# --------------------------------------------------
def print_header(roll_for, roll_type, adv, disadv, abbrevs):
    """
    Tell user what they made a roll for and whether it was with
    advantage or disadvantage.
    """
    roll_for = ([k for k, v in abbrevs.items()
                 if v == roll_for][0]).capitalize()

    if roll_for[0] in ['A', 'E', 'I', 'O', 'U']:
        article = "an"
    else:
        article = "a"

    if adv:
        dis_adv = " with advantage"
    elif disadv:
        dis_adv = " with disadvantage"
    else:
        dis_adv = ""

    print(f'\nYou made {article} {roll_for} {roll_type}{dis_adv}.')


# --------------------------------------------------
def calc_total(rolls, pos_neg, mod):
    """ calculate the final total and print formatted results """
    if len(rolls) == 3:
        print(f'\nYour total is {rolls[0] + mod}.')
        print(f'You rolled a {rolls[1]} and a {rolls[2]} on the d20 \
with a {pos_neg}{mod} modifier.\n')
    elif len(rolls) == 1:
        print(f'\nYour total is {rolls[0] + mod}.')
        print(f'You rolled a {rolls[0]} on the d20 with a \
{pos_neg}{mod} modifier.\n')


# --------------------------------------------------
if __name__ == '__main__':
    main()
