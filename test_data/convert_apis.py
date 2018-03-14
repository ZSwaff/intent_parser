#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This file converts exported APIs to this API."""

import os
import zipfile
import shutil

ROOT_DIR_PATH = './raw_apis/'


def main():
    for fname in os.listdir(ROOT_DIR_PATH):
        fname = ROOT_DIR_PATH + fname
        if not fname.endswith('.zip'):
            continue

        dname = fname[:-4]
        with zipfile.ZipFile(fname, 'r') as fin:
            fin.extractall(dname)



        shutil.rmtree(dname)


if __name__ == '__main__':
    main()
