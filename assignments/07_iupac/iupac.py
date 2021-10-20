#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-10-19
Purpose: Translate an IUPAC-encoded string of DNA into a regular
         expression that will match all the possible strings of DNA.
"""

import argparse
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Expand IUPAC codes',
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

    code_base = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'U': 'U',
                 'R': '[AG]', 'Y': '[CT]', 'S': '[GC]', 'W': '[AT]',
                 'K': '[GT]', 'M': '[AC]', 'B': '[CGT]', 'D': '[AGT]',
                 'H': '[ACT]', 'V': '[ACG]', 'N': '[ACGT]'}

    output = []
    for seq in args.SEQ:
        translation = seq.translate(seq.maketrans(code_base))
        if args.outfile.name == '<stdout>':
            print(seq, translation)
        seq_and_base = seq + ' ' + translation + '\n'
        output.append(seq_and_base)

    if args.outfile.name != '<stdout>':
        with open(args.outfile.name, 'w', encoding="utf-8") as f:
            for line in output:
                f.write(line)
            f.close()
            print(f'Done, see output in "{args.outfile.name}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
