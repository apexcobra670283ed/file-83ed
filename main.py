#!/usr/bin/env python3
"""
File deduplication utility: identifies duplicate files in a directory and optionally deletes them.
"""
import os, argparse, hashlib

def file_hash(path, block=65536):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block), b''):
            h.update(chunk)
    return h.hexdigest()

def find_dups(root):
    size_map = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
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
            h = file_hash(p)
            hash_map.setdefault(h, []).append(p)
    return [paths for paths in hash_map.values() if len(paths) > 1]

def main():
    parser = argparse.ArgumentParser(description="Find and optionally delete duplicate files.")
    parser