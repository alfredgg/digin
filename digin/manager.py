#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def import_file(path, delimiter=';'):
    rows = []
    cols = 0
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for rw in reader:
            cols = max(len(rw), cols)
            rows.append(rw)
    return {
        'size': len(rows),
        'rows': rows,
        'cols': cols
    }

def export_file(path):
    pass