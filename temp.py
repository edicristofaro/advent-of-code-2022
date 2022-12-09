from collections import defaultdict

with open("input-7-test.txt", "r") as f:
        commands = f.readlines()

commands = [c.strip() for c in commands]

def change_directory(s: str, cd: list[str]) -> None:
    match s:
        case '/':
            cd = ['root']
        case '..':
            cd.pop()
        case _:
            cd.append(s)

    return cd


def get_dict_path(d: dict, path: list) -> dict:
    if len(path) == 1:
        return d[path[0]]
    else:
        return get_dict_path(d[path[0]], path[1:])


def directory_size(d: dict) -> int:
    return sum(directory_size(v) if isinstance(v, dict) else v for v in d.values())


def traverse_dict(d: dict, res=None) -> None:
    if not res:
        res = []

    for k, v in d.items():
        if not isinstance(v, dict):
            continue
        res.append(directory_size(v))
        traverse_dict(v, res)

    return res


def p1(instructions: list[str]) -> None:

    files = {'root': {}}
    cd = ['root']

    for line in instructions:
        if '$ cd' in line:
            cd = change_directory(line.split()[-1], cd=cd)
        elif '$ ls' in line:
            continue
        else:
            marker, name = line.split()
            if marker.isnumeric():
                get_dict_path(files, cd)[name] = int(marker)
            else:
                get_dict_path(files, cd)[name] = {}

    print(sum(n for n in traverse_dict(files) if n <= 100_000))
    return files

p1(commands)