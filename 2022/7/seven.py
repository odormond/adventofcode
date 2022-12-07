#! /usr/bin/env python

import advent_of_code as adv

test_data = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def to_fs_tree(data):
    root = {}
    cd = []
    cwd = root
    for line in data.splitlines():
        match line.split():
            case ['$', 'cd', '/']:
                cwd = root
            case ['$', 'cd', '..']:
                cd.pop()
                cwd = root
                for d in cd:
                    cwd = cwd[d]
            case ['$', 'cd', directory]:
                cd.append(directory)
                cwd = cwd.setdefault(directory, {})
            case ['$', 'ls']:
                pass
            case ["dir", directory]:
                cwd[directory] = {}
            case [size, filename]:
                cwd[filename] = int(size)
            case _:
                raise ValueError(_)

    return root


def dir_sizes(tree):
    sizes = {}
    for name, entry in tree.items():
        if isinstance(entry, int):
            sizes[''] = sizes.get('', 0) + entry
        else:
            for sub_path, size in dir_sizes(entry).items():
                sizes[f'/{name}{sub_path}'] = size
    sizes[''] = sum(size for path, size in sizes.items() if path.count('/') <= 1)
    return sizes


test_tree = to_fs_tree(test_data)
test_sizes = dir_sizes(test_tree)
assert test_sizes['/a/e'] == 584
assert test_sizes['/a'] == 94853
assert test_sizes['/d'] == 24933642
assert test_sizes[''] == 48381165

assert sum(size for size in test_sizes.values() if size <= 100000) == 95437

sizes = dir_sizes(adv.input(to_fs_tree))
print("Part 1:", sum(size for size in sizes.values() if size <= 100000))

DISK_SIZE = 70000000
REQ_SIZE = 30000000

def free(sizes, req, total):
    available = total - sizes['']
    for size in sorted(sizes.values()):
        if available + size >= req:
            return size
    raise ValueError("No directory big enough")

assert free(test_sizes, REQ_SIZE, DISK_SIZE) == 24933642

print("Part 2:", free(sizes, REQ_SIZE, DISK_SIZE))
