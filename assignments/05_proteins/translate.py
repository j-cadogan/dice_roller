#!/usr/bin/env python3
"""
Author : Jaclyn Cadogan <jcadogan@localhost>
Date   : 2021-10-05
Purpose: Translates a given DNA or RNA sequence into amino acids
         and write the output to a new file.
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Translate DNA/RNA to proteins',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('sequence',
                        metavar='str',
                        help='DNA/RNA sequence')

    parser.add_argument('-c',
                        '--codons',
                        help='A file with codon translations',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=None,
                        required=True)

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='out.txt')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    codon_table = {}
    for line in args.codons:
        codon_table.update({line[:3].lstrip(): line[4:].rstrip()})

    k = 3
    seq = args.sequence
    protein_seq = ''
    for codon in [seq[i:i + k] for i in range(0, len(seq), k)]:
        value = codon_table.get(codon.upper(), '-')
        protein_seq += value

    args.outfile.write(protein_seq)
    print('Output written to "{}".'.format(args.outfile.name))


# --------------------------------------------------
if __name__ == '__main__':
    main()
