#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-25
Purpose: Rock the Casbah
"""

import argparse
import random


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Calculate dice rolls in D&D 5e',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('weapons',
                        metavar='weapons',
                        help='.csv with 5e basic weapon info',
                        default='inputs/weapons.csv',
                        nargs='?',
                        type=argparse.FileType('rt'))

    parser.add_argument('character',
                        metavar='char',
                        help='.txt with character info and stats',
                        type=argparse.FileType('rt'))

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    # get all dicts and create inventory list
    for i, line in enumerate(args.character):
        if i == 0:
            char = read_dict(line)
        elif i == 1:
            scores = read_dict(line)
        elif i == 2:
            saves = read_dict(line)
        elif i == 3:
            skills = read_dict(line)
        elif i == 6:
            inventory = list(line.split(', '))
    

    while True:
        print("\nOptions:\n\
        For ability check, enter ability or a\n\
        For skill check, enter skill or k\n\
        For saving throw, enter save or v\n\
        For weapon attack, enter weapon or w\n\
        For tool check, enter tool or t\n\n\
        To exit program, type x or exit.\n")
        command = input("What would you like to roll for? ").split()
        if command[0] == ("x" or "exit"):
            break
        elif command[0] == "ability" or command[0] == "a":
            ability_check(scores, command)
        elif command[0] == "skill" or command[0] == "k":
            skill_check(scores, command, skills, char)
        elif command[0] in ["save", "v"]:
            saving_throw(scores, command, char, saves)
        elif command[0] in ['tool', 't']:
            tool_check(scores, command, char,)


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
    """Calculate modifider"""
    print(ability)
    mod = int((scores[ability] - 10) / 2 + (prof))

    if mod >= 0:
        pos_neg = "+"
    else:
        pos_neg = ""
    
    return pos_neg, mod


# --------------------------------------------------
def calc_roll(command, ability, prof, scores):
    pos_neg, mod = mod_calc(scores, ability, prof)

    # if advantge/disadvantage, roll twice and take the higher/lower number
    if 'adv' in command or 'advantage' in command \
    or 'disadv' in command or 'disadvantage' in command:
        roll1 = random.randint(1,20)
        roll2 = random.randint(1,20)
        if 'adv' or 'advantage' in command:
            roll = max(roll1, roll2)
        else:
            roll = min(roll1, roll2)
        print(f'Your total is {roll + mod}.')
        print(f'You rolled a {roll1} and a {roll2} on the d20 with a {pos_neg}{mod} modifier.')
    else:
        roll = random.randint(1,20)
        print(f'Your total is {roll + mod}.')
        print(f'You rolled a {roll} on the d20 with a {pos_neg}{mod} modifier.')


# --------------------------------------------------
def ability_check(scores, command):
    """Make an ability check"""
    # show user options if not already specified
    if len(command) == 1:
        print("\nOptions:\n\
            For strength check, type str\n\
            For dexterity check, type dex\n\
            For constitution check, type con\n\
            For intelligence check, type int\n\
            For wisdom check, type wis\n\
            For charisma check, type cha\n")
        ability = input("What ability would you like to roll a check for? ")
    elif len(command) > 1:
        ability = command[1]
    calc_roll(command, ability, 0, scores)


# --------------------------------------------------
def saving_throw(scores, command, char, saves):
    if len(command) == 1:
        print("\nOptions:\n\
            For strength save, type str\n\
            For dexterity save, type dex\n\
            For constitution save, type con\n\
            For intelligence save, type int\n\
            For wisdom save, type wis\n\
            For charisma save, type cha\n")
        ability = input("What ability would you like to roll a saving throw for? ")
    elif len(command) > 1:
        ability = command[1]
    
    if ability in saves.keys():
        prof = saves[ability] * char['prof_bonus']
    else:
        prof = 0
    
    calc_roll(command, ability, prof, scores)


# --------------------------------------------------
def skill_check(scores, command, skills, char):
    """
    Make a skill check
    scores: dict of ability scores (str, dex, con, etc.)
    command: entire command entered by user. list.
    skills: dict of skills the character is proficient or expert in (1 = proficient, 2 = expert)
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

    # get skill to make a check for
    if len(command) == 1:
        print("\nChoose a skill to roll for:\n\
            acrobatics (acr)\n\
            animal handling (anh)\n\
            arcana (arc)\n\
            athletics (ath)\n\
            deception (dec)\n\
            insight (ins)\n\
            intimidation (int)\n\
            investigation (inv)\n\
            medicine (med)\n\
            nature (nat)\n\
            perception (perc)\n\
            performance (perf)\n\
            persuasion (pers)\n\
            religion (rel)\n\
            sleight of hand (soh)\n\
            stealth (ste)\n\
            survival (sur)\n")
        skill = input("What skill would you like to roll a check for? ")
    elif len(command) > 1:
        skill = command[1]
    
    # calculate proficiency
    if skill in skills.keys():
        prof = skills[skill] * char['prof_bonus']
    else:
        prof = 0
    
    # figure out which ability is used by the skill
    for key, value in skill_type.items():
        if skill in value:
            ability = key

    calc_roll(command, ability, prof, scores)
    




# --------------------------------------------------
if __name__ == '__main__':
    main()
