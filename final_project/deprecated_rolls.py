#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-25
Purpose: Rock the Casbah
"""

import argparse
import random
import mock
import builtins
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Calculate dice rolls in D&D 5e',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('character',
                        metavar='char',
                        help='.txt with character info and stats',
                        type=argparse.FileType('rt'))

    parser.add_argument('--seed',
                        '-s',
                        metavar='seed',
                        help='Optional seed value for testing',
                        type=int)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    # create all dicts
    for i, line in enumerate(args.character):
        if i == 0:
            char = read_dict(line)
        elif i == 1:
            scores = read_dict(line)
        elif i == 2:
            saves = read_dict(line)
        elif i == 3:
            skills = read_dict(line)
    
    # get user commands
    while True:
        print("\n----------------------------------------------\n\n\
Options:\n\
        For ability check, enter ability or a\n\
        For skill check, enter skill or k\n\
        For saving throw, enter save or v\n\
        To exit program, type x or exit.\n")
        command = input("What would you like to roll for? ").split()

        if command[0] in ["x", "exit"]:
            break
        elif command[0] in ["ability", "a"]:
            ability = ability_check(command)
            pos_neg, mod = mod_calc(scores, ability, 0)
            calc_roll(command, pos_neg, mod)
        elif command[0] in ["skill", "k"]:
            skill = get_skill(command)
            prof, ability = skill_check(skill, char, skills)
            pos_neg, mod = mod_calc(scores, ability, prof)
            calc_roll(command, pos_neg, mod)
        elif command[0] in ["save", "v"]:
            ability = get_save(command)
            prof = saving_throw(ability, char, saves)
            pos_neg, mod = mod_calc(scores, ability, prof)
            calc_roll(command, pos_neg, mod)
        else:
            print("Please enter a valid command.")


# --------------------------------------------------
def read_dict(line):
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
        except:
            pass
        dictionary[pair[0]] = pair[1]
    return dictionary


# --------------------------------------------------
def mod_calc(scores, ability, prof):
    """
    Calculate modifider. If modifier is positive, add a + before it.
    scores: dictionary of ability scores.
    ability: ability used for roll.
    prof: 0, 1, or 2. 0 = no proficiency. 1 = proficiency. 2 = expertise.
    mod: modifier to be added to base d20 roll. Can be positive or negative.
    pos_neg: "+" if modifier is 0 or greater, empty string if less than 0,since 
            a "-" will automatically be used. Complies with typical 5e notation.
    """
    mod = int((scores[ability] - 10) / 2 + (prof))

    if mod >= 0:
        pos_neg = "+"
    else:
        pos_neg = ""
    
    return pos_neg, mod


# --------------------------------------------------
def calc_roll(command, pos_neg, mod):
    """
    Roll the d20 (twice, if the user indicated (dis)advantage), then add the
    modifier.
    """

    # if advantge/disadvantage, roll twice and take the higher/lower number
    if 'adv' in command or 'advantage' in command \
    or 'disadv' in command or 'disadvantage' in command:
        roll1 = random.randint(1,20)
        roll2 = random.randint(1,20)
        if 'disadv' in command or 'disadvantage' in command:
            roll = min(roll1, roll2)
        else:
            roll = max(roll1, roll2)
        print(f'\nYour total is {roll + mod}.')
        print(f'You rolled a {roll1} and a {roll2} on the d20 with a {pos_neg}{mod} modifier.')
    else:
        roll = random.randint(1,20)
        print(f'\nYour total is {roll + mod}.')
        print(f'You rolled a {roll} on the d20 with a {pos_neg}{mod} modifier.')


# --------------------------------------------------
def ability_check(command):
    """Make an ability check"""
    
    # show user options if not already specified
    if len(command) > 1:
        ability = command[1]
    elif len(command) == 1:
        print("\n\n----------------------------------------------\n\n\
Options:\n\
            For strength check, type str\n\
            For dexterity check, type dex\n\
            For constitution check, type con\n\
            For intelligence check, type int\n\
            For wisdom check, type wis\n\
            For charisma check, type cha\n")
        
        # validate input
        valid_input = ["strength", "str", "dexterity", "dex", "constitution",
        "con", "intelligence", "int", "wisdom", "wis", "charisma", "cha"]
        ability = input("What ability would you like to roll a check for? ")
        while ability not in valid_input:
            print("\nPlease enter a valid ability.")
            ability = input("What ability would you like to roll a check for? ").lower()
    
    return ability


# --------------------------------------------------
def get_save(command):
    """
    Determine what save is being used.
    """
    if len(command) > 1:
        ability = command[1]
        return ability
    elif len(command) == 1:
        ability = get_save_input()
        return ability
#         print("\n\n----------------------------------------------\n\n\
# Options:\n\
#             For strength save, type str\n\
#             For dexterity save, type dex\n\
#             For constitution save, type con\n\
#             For intelligence save, type int\n\
#             For wisdom save, type wis\n\
#             For charisma save, type cha\n")
#         valid_input = ["strength", "str", "dexterity", "dex", "constitition",
#         "con", "intelligence", "int", "wisdom", "wis", "charisma", "cha"]
        
#         ability = input("What ability would you like to roll a saving throw for? ").lower()
#         while ability not in valid_input:
#             print("\nPlease enter a valid ability.")
#             ability = input("What ability would you like to roll a saving throw for? ").lower()

    #return ability


def get_save_input():
    print("\n\n----------------------------------------------\n\n\
Options:\n\
        For strength save, type str\n\
        For dexterity save, type dex\n\
        For constitution save, type con\n\
        For intelligence save, type int\n\
        For wisdom save, type wis\n\
        For charisma save, type cha\n")
    valid_input = ["strength", "str", "dexterity", "dex", "constitition",
    "con", "intelligence", "int", "wisdom", "wis", "charisma", "cha"]
        
    ability = input("What ability would you like to roll a saving throw for? ").lower()
    while ability not in valid_input:
        print("\nPlease enter a valid ability.")
        ability = input("What ability would you like to roll a saving throw for? ").lower()

    return ability

# --------------------------------------------------
def test_get_save():
    assert get_save(["save", "strength"]) == "strength"
    assert get_save(["v", "dex"]) == "dex"


# --------------------------------------------------
def test_get_save_input():
    with mock.patch.object(builtins, 'input', lambda _: "dexterity"):
        assert get_save_input() == "dexterity"
    with mock.patch.object(builtins, 'input', lambda _: "cha"):
        assert get_save_input() == "cha"
    with mock.patch.object(builtins, 'input', lambda _: "foo"):
        assert "\nPlease enter a valid ability." in sys.stdout
        # else:
        #     with mock.patch.object(builtins, 'input', lambda _: "int"):
        #         assert get_save_input() == "intelligence"


# --------------------------------------------------
def saving_throw(ability, char, saves):
    # check if proficient
    if ability in saves.keys():
        prof = saves[ability] * char['prof_bonus']
    else:
        prof = 0
    
    return prof


# --------------------------------------------------
def get_skill(command):
    """
    Determine what skill is being used.
    """
    # get skill to make a check for, if not already specified
    if len(command) > 1:
        skill = command[1]
    elif len(command) == 1:
        print("\n----------------------------------------------\n\n\
Choose a skill to roll for:\n\
        Acrobatics (acr)\n\
        Animal handling (anh)\n\
        Arcana (arc)\n\
        Athletics (ath)\n\
        Deception (dec)\n\
        Insight (ins)\n\
        Intimidation (int)\n\
        Investigation (inv)\n\
        Medicine (med)\n\
        Nature (nat)\n\
        Perception (perc)\n\
        Performance (perf)\n\
        Persuasion (pers)\n\
        Religion (rel)\n\
        Sleight of hand (soh)\n\
        Stealth (ste)\n\
        Survival (sur)\n")
        
        valid_input = ["acrobatics", "acr", "animal handling", "anh",
        "arcana", "arc", "athletics", "ath", "deception", "dec", "insight",
        "ins", "intimidation", "int", "investigation", "inv", "medicine",
        "med", "nature", "nat", "perception", "perc", "performance", "perf",
        "persuasion", "pers", "religion", "rel", "sleight of hand", "soh",
        "stealth", "ste", "survival", "sur"]

        skill = input("What skill would you like to roll a check for? ").lower()
        while skill not in valid_input:
            print("\nPlease enter a valid skill.")
            skill = input("What skill would you like to roll a check for? ").lower()
    
    return skill

# --------------------------------------------------
def skill_check(skill, char, skills):
    """
    Make a skill check
    skill: what skill is being used
    char: dict of key character stats
    skills: dict of what skills character is proficient/expert in
    prof: 0, 1, or 2.
    """
    skill_type = {
    'str':['athletics', 'ath'],
    'dex':['acrobatics', 'acr', 'sleight of hand', 'soh', 'stealth', 'ste'],
    'int':['arcana', 'arc', 'history', 'his', 'hist',
        'investigation', 'inv', 'nature', 'nat', 'religion', 'rel'],
    'wis':['animal handling', 'animal', 'anh', 'insight', 'ins',
        'medicine', 'med', 'perception', 'perc', 'survival', 'sur', 'surv'],
    'cha':['intimidation', 'int', 'intim', 'deception', 'dec', 'performance', 'perf', 'persuasion', 'pers']
    }

    # calculate proficiency
    if skill in skills.keys():
        prof = skills[skill] * char['prof_bonus']
    else:
        prof = 0
    
    # figure out which ability is used by the skill
    for key, value in skill_type.items():
        if skill in value:
            ability = key
    
    return prof, ability


# --------------------------------------------------
if __name__ == '__main__':
    main()
