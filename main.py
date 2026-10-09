"""File deduplication utility.
Finds duplicate files in a directory tree and prints groups.
"""

import os, sys, hashlib

def file_hash(path, block=65536):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block), b''):
            h.update(chunk)
    return h.hexdigest()

def find_dups(root):
    size_map = {}
    for dirpath, _, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            try:
                sz = os.path.getsize(path)
            except OSError:
                continue
            size_map.setdefault(sz, []).append(path)
    hash_map = {}
    for sz, paths in size_map.items():
        if len(paths) < 2:
            continue
        for p in paths:
            try:
                h = file_hash(p)
            except OSError:
                continue
            hash_map.setdefault(h, []).append(p)
    return [paths for paths in hash_map.values() if len(paths) > 1]

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    dups = find_dups(root)
    if not dups:
        print('No duplicates found.')
    else:
        for group in dups:
            print('Duplicate group:')
            for p in group:
                print('  ' + p)
            print()

if __name__ == '__main__':
    main()