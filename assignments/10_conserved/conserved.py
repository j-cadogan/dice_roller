#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-09
Purpose: Shows conserved bases in two or more aligned sequences.
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Find conserved bases',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    seq_list = []
    for sequence in args.file:
        seq_list += sequence.split()

    conserved = ''
    for i, seq in enumerate(seq_list):
        print(seq)
        for j, _ in enumerate(seq):
            tmp = "|"
            for k, _ in enumerate(seq_list):
                if seq_list[i][j] != seq_list[k][j]:
                    tmp = "X"
            conserved += tmp

    print(conserved[:len(seq_list[0])])


# --------------------------------------------------
if __name__ == '__main__':
    main()
