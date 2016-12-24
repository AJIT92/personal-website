#!/usr/bin/env python2

import codecs
import json
import os
import subprocess

SRC_DIR = 'src'
CRUSHED_LIST_FILE = os.path.join('scripts', 'pngcrushed.json')


def main():
    # Read crushed file list
    with codecs.open(CRUSHED_LIST_FILE, 'r', 'utf8') as f:
        crushed = set(json.load(f))

    # Search for PNGs
    for root, _, fnames in os.walk(SRC_DIR):
        for fname in fnames:
            # Skip if not PNG
            if not fname.endswith('.png'):
                continue

            # Skip if already crushed
            fpath = os.path.join(root, fname)
            if fpath in crushed:
                continue

            # Crush PNG
            subprocess.call(['pngcrush', fpath, '_tmp.png'])
            subprocess.call(['mv', '-f', '_tmp.png', fpath])
            crushed.add(fpath)

    # Write crushed file list
    with codecs.open(CRUSHED_LIST_FILE, 'w', 'utf8') as f:
        json.dump(sorted(crushed), f, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    main()