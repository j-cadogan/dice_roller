#!/usr/bin/env python3
"""
Author : Jaclyn Cadogan <jcadogan@localhost>
Date   : 2021-10-12
Purpose: Finds the words in common between two text files, sorts
         the words, and prints the results to STDOUT and/or to
         another file.
"""

import argparse
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Find common words',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file1',
                        metavar='FILE1',
                        help='Input file 1',
                        type=argparse.FileType('rt'),
                        default=[sys.stdin])

    parser.add_argument('file2',
                        metavar='FILE2',
                        help='Input file 2',
                        type=argparse.FileType('rt'),
                        default=[sys.stdin])

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default=sys.stdout)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    f1_list, f2_list = [], []

    for fh in args.file1:
        f1_list += fh.rstrip().split()
    for fh in args.file2:
        f2_list += fh.rstrip().split()

    # Convert lists to sets, use intersection method, then convert
    # the resulting set back into a sorted list. Not exactly elegant.
    f1_set, f2_set = set(f1_list), set(f2_list)
    common = sorted(list(f1_set.intersection(f2_set)))

    # Pylint pouted about me using range(len(common)) in the
    # for loop instead of enumerate(common). Then it pouted
    # about me not using both loop variables from enumerate.
    # So now I have to create an otherwise useless 'length' variable,
    # and I'm so salty about it that I added 5 lines of comments.
    length = len(common)
    for i in range(length):
        print(common[i])


# --------------------------------------------------
if __name__ == '__main__':
    main()
