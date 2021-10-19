#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-10-19
Purpose: Rock the Casbah
"""

import argparse
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('SEQ',
                        metavar='SEQ',
                        help='Input sequence(s)',
                        nargs='+')

    parser.add_argument('-o',
                        '--outfile',
                        help='A readable file',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default=sys.stdout)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    code_input = args.SEQ

    '''
    code_base = {'A':'A', 'C':'C', 'G':'G', 'T':'T', 'U':'U', 'R':'AG',
                 'Y':'CT', 'S':'GC', 'W':'AT', 'K':'GT', 'M':'AC',
                 'B':'CGT', 'D':'AGT', 'H':'ACT', 'V':'ACG', 'N':'ACGT'}
    '''
    code_base = {'A':'A', 'C':'C', 'G':'G', 'T':'T', 'U':'U', 'R':'[AG]',
                 'Y':'[CT]', 'S':'[GC]', 'W':'[AT]', 'K':'[GT]', 'M':'[AC]',
                 'B':'[CGT]', 'D':'[AGT]', 'H':'[ACT]', 'V':'[ACG]', 'N':'[ACGT]'}
    '''
    for sequence in code_input:
        base_str = ''
        #print(sequence)
        for letter in sequence:
            print(letter, code_base[letter])
            if len(code_base[letter]) > 1:
                base_str += base_str.join('[' + code_base[letter] + ']')
                print('[' + code_base[letter] + ']')
            else:
                base_str += base_str.join(code_base[letter])
            print(base_str)
        print(sequence, base_str)
    
    for sequence in code_input:
        base_str = ''
        for letter in sequence:
            tmp = []
            if len(code_base[letter]) > 1:
                tmp += ['[', code_base[letter], ']']
                print(tmp.join())
    '''
    for sequence in code_input:
        translation = sequence.maketrans(code_base)
        print(sequence, sequence.translate(translation))

# --------------------------------------------------
if __name__ == '__main__':
    main()
