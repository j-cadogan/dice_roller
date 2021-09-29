#!/usr/bin/env python3
"""
Author : Jaclyn Cadogan <jcadogan@localhost>
Date   : 2021-09-28
Purpose: Create a python version of the cat command that can print
         files line by line. Includes an optional flag that will
         number each line.
"""

import argparse
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Python cat',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file(s)',
                        nargs='+',
                        default=[sys.stdin])

    parser.add_argument('-n',
                        '--number',
                        help='Number the lines',
                        action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    for fh in args.file:
        num_lines = 0
        for line in fh:
            num_lines += 1
            if args.number:
                print(f'{num_lines:6}' + '\t' + line.rstrip())
            else:
                print(line.rstrip())


# --------------------------------------------------
if __name__ == '__main__':
    main()
