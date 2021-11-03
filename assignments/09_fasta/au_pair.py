#!/usr/bin/env python3
"""
Author : jcadogan <jcadogan@localhost>
Date   : 2021-11-02
Purpose: Splits interleaved fasta sequence files into separate
         files for forward and reverse reads.
"""

import argparse
import os


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Split the interleaved/paired reads',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input file(s)',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='split')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    for fh in args.file:
        basename = os.path.basename(fh.name)
        root, ext = os.path.splitext(basename)
        line_count = 0
        for line in fh:
            if line_count % 2 == 0:
                if line_count % 4 == 0:
                    out_name = os.path.join(args.outdir, root + '_1' + ext)
                    with open(out_name, 'a', encoding='utf-8') as out:
                        out.write(line.strip() + '\n')
                else:
                    out_name = os.path.join(args.outdir, root + '_2' + ext)
                    with open(out_name, 'a', encoding='utf-8') as out:
                        out.write(line.strip() + '\n')
            else:
                with open(out_name, 'a', encoding='utf-8') as out:
                    out.write(line.strip() + '\n')
            line_count += 1
    print(f'Done, see output in "{args.outdir}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
