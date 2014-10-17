#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string


class RandFS:
    def __init__(self, hash=None):
        self._deep_tree = (0, 0)
        self._num_folders = (0, 0)
        self._num_files = (0, 0)
        self._files_size = (0, 0)
        self._hash = hash

    def create_folders(self, num_folders=(0, 0)):
        self._num_folders = num_folders
        return self

    def create_files(self, num_files=(0, 0)):
        self._num_files = num_files
        return self

    def with_file_size(self, files_size=(0, 0)):
        self._files_size = files_size
        return self

    @staticmethod
    def _get_random_name():
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))

    def create(self):
        if self._hash is None:
            self._hash = random.getrandbits(128)
        random.seed(self._hash)

        os.mkdir(self._get_random_name())
        return self._hash


if __name__ == '__main__':
    fs = RandFS(hash='278923569719323934022449651675688586450')
    result = fs.create_folders(10).create_files(4).with_file_size(10000).create()
    print(result)