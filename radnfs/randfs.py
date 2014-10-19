#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string
import shutil


class RandFS:
    def __init__(self, hash_str=None):
        self._rand_set = string.ascii_uppercase + \
                         string.digits + \
                         string.ascii_lowercase


        self._top = len(os.getcwd().split(os.sep))
        self._max_dirs = 5
        self._max_depth = 3
        self._max_files = 4
        self._max_size = 10
        self._hash = hash_str
        if self._hash is None:
            self._hash = random.getrandbits(128)
        random.seed(self._hash)

    def _get_random_name(self):
        return ''.join(
            random.choice(self._rand_set) for _ in range(10))

    def get_hash(self):
        return self._hash

    def create_fs(self, path=None):
        if path is None:
            if os.path.isdir('test'):
                shutil.rmtree('test')
            os.mkdir('test')
            os.chdir(os.path.join(os.getcwd(), 'test'))
        else:
            os.chdir(path)

        path = os.getcwd()
        number_files = random.randrange(self._max_files)
        for _ in xrange(number_files):
            file_name = self._get_random_name()
            file_size = random.randrange(self._max_size)
            with open(file_name, 'wb') as f:
                f.write(os.urandom(file_size))

        depth = len(os.getcwd().split(os.sep))

        if (depth - self._top) > self._max_depth:
            return
        dir_list = []
        num_dirs = random.randrange(self._max_dirs)
        for _ in xrange(num_dirs):
            folder_name = self._get_random_name()
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
                dir_list.append(os.path.join(path, folder_name))

        for folder in dir_list:
            self.create_fs(folder)
        return self

if __name__ == '__main__':
    fs = RandFS(hash_str='278923569719323934022449651675688586450')
    print fs.create_fs().get_hash()
