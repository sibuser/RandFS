#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string
import shutil
import argparse


class RandFS:
    def __init__(self, seed=None, max_dirs=1, max_depth=1, max_files=1,
                 max_size=1):
        self._rand_set = string.ascii_uppercase + \
                         string.digits + \
                         string.ascii_lowercase

        self._top = len(os.getcwd().split(os.sep))
        if not seed:
            self._max_dirs, self._max_depth, self._max_files, self._max_size = max_dirs, max_depth, max_files, max_size
            self.seed = '.'.join(map(str, [self._max_dirs, self._max_depth, self._max_files, self._max_size]))

        else:
            self._max_dirs, self._max_depth, self._max_files, self._max_size = tuple(map(int, seed.split('.')))
            self.seed = seed
        random.seed(self.seed)

    def _get_random_name(self):
        return ''.join(
            random.choice(self._rand_set) for _ in range(10))

    def _is_max_depth_reached(self):
        depth = len(os.getcwd().split(os.sep))
        return depth - self._top > self._max_depth

    def _generate_folders(self):
        path = os.getcwd()
        dir_list = []
        num_dirs = random.randrange(self._max_dirs)
        for _ in range(num_dirs):
            folder_name = self._get_random_name()
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
                dir_list.append(os.path.join(path, folder_name))
        return dir_list

    def _generate_files(self):
        number_files = random.randrange(self._max_files)
        for _ in range(number_files):
            file_name = self._get_random_name()
            file_size = random.randrange(self._max_size)
            with open(file_name, 'wb') as f:
                f.write(os.urandom(file_size))

    def create_fs(self, path=None):
        if path is None:
            if os.path.isdir('test'):
                shutil.rmtree('test')
            os.mkdir('test')
            os.chdir(os.path.join(os.getcwd(), 'test'))
        else:
            os.chdir(path)

        self._generate_files()

        if self._is_max_depth_reached():
            return

        for folder in self._generate_folders():
            self.create_fs(folder)
        return self


def main(args=None):
    """
    :param args:
    :return: 0 if everything is OK
             1 if something went wrong
             2 if invalid usage
    """
    parser = argparse.ArgumentParser(
        description='Generate pseudo random file tree.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--max-files', default=2, type=int, help='Max amount of files in each folder')
    parser.add_argument('--max-depth', default=3, type=int, help='Max depth of a tree')
    parser.add_argument('--max-size', default=2, type=int, help='Max size of a file')
    parser.add_argument('--max-dirs', default=5, type=int, help='Max amount of folders in each folder')

    parser.add_argument('--hash-str', default='', type=str, help='String will be used for reproducing a '
                                                                 'previously created file tree')

    opts = parser.parse_args(args)
    fs = RandFS(max_depth=opts.max_depth, max_files=opts.max_files, max_dirs=opts.max_dirs, max_size=opts.max_size,
                seed=opts.hash_str)
    print(fs.create_fs().seed)


if __name__ == '__main__':
    main()
