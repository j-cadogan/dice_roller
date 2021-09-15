#!/usr/bin/env python3
"""
Author : Jaclyn Cadogan (j-cadogan)
Date   : 2021-09-14
Purpose: Sum a list of numbers.
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('integers',
                        metavar='INT',
                        help='Numbers to add',
                        type = int,
                        nargs = '+')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    int_list = args.integers

    print('{} = {}'.format(' + '.join(map(str, args.integers)), sum(args.integers)))


# --------------------------------------------------
if __name__ == '__main__':
    main()
