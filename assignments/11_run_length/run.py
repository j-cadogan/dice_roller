#!/usr/bin/env python3
'''
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-16
Purpose: Rock the Casbah
'''

import argparse
import os


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Run-length encoding/data compresssion',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text',
                        metavar='str',
                        type=str,
                        help='DNA text or file')

    args = parser.parse_args()
    if os.path.isfile(args.text):
        args.text = open(args.text, encoding='utf-8').read().rstrip()

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    for seq in args.text.splitlines():
        rle(seq)


# --------------------------------------------------
def rle(seq: str) -> str:
    """Compress sequences"""
    compressed = ''
    prev = None
    count = 1
    for base in seq:
        if base == prev:
            count += 1
        elif prev is None:
            prev = base
        else:
            compressed += prev
            if count > 1:
                compressed += str(count)
            count = 1
            prev = base
    compressed += prev
    if count > 1:
        compressed += str(count)
    print(compressed)


# --------------------------------------------------
if __name__ == '__main__':
    main()
