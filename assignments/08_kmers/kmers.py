#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-10-26
Purpose: Find common k-mers between two files, with customizable
         k-mer length.
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Find common kmers',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file1',
                        metavar='FILE1',
                        help='Input file 1',
                        type=argparse.FileType('rt'))

    parser.add_argument('file2',
                        metavar='FILE2',
                        help='Input file 2',
                        type=argparse.FileType('rt'))

    parser.add_argument('-k',
                        '--kmer',
                        help='K-mer size',
                        metavar='int',
                        type=int,
                        default=3)

    args = parser.parse_args()

    if args.kmer < 1:
        parser.error(f'--kmer "{args.kmer}" must be > 0')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    text1 = args.file1.read().split()
    text2 = args.file2.read().split()

    kmers1 = kmers_dict(text1, args.kmer)
    kmers2 = kmers_dict(text2, args.kmer)

    common = sorted(list(set(kmers1) & set(kmers2)))
    for i in common:
        print(f'{i:10} {kmers1[i]:5} {kmers2[i]:5}')


# --------------------------------------------------
def find_kmers(seq, k):
    """Find k-mers in string"""
    n = len(seq) - k + 1
    return [] if n < 1 else [seq[i:i + k] for i in range(n)]


# --------------------------------------------------
def kmers_dict(text, k):
    """Add k-mers and their frequency to dictionary."""
    kmers = {}
    for seq in text:
        for kmer in find_kmers(seq, k):
            if kmer not in kmers:
                kmers.update({kmer: 1})
            else:
                kmers[kmer] += 1
    return kmers


# --------------------------------------------------
if __name__ == '__main__':
    main()
