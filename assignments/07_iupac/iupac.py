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


# --------------------------------------------------
if __name__ == '__main__':
    main()
