# python -c 'from solutions import *; day1()'

import copy
import string

from collections import OrderedDict

def day1():
    infile = open("./input-1-1.txt", "r")
    lines = infile.readlines()

    elf = 1
    items = 0
    calories = 0

    elves = []

    for l in lines:
        l = l.strip()
        if l != '':
            items += 1
            calories += int(l)
        else:
            elves.append((elf, items, calories))
            items = 0
            calories = 0
            elf += 1
    
    # part 1: calories of elf with most total calories
    e, i, c = zip(*elves)
    print(max(c))

    # part 2: total calories of top 3 elves with most total calories
    c = sorted(c, reverse=True)
    print(sum(c[0:3]))


def day2():
    def _win(against):
        if against == 'A':
            return 'B', 2
        elif against == 'B':
            return 'C', 3
        else:
            return 'A', 1

    def _tie(against):
        if against == 'A':
            return 'A', 1
        elif against == 'B':
            return 'B', 2
        else:
            return 'C', 3

    def _lose(against):
        if against == 'A':
            return 'C', 3
        elif against == 'B':
            return 'A', 1
        else:
            return 'B', 2
    
    f = open("./input-2.txt", "r")
    lines = []
    lines_original = []
    values = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    for l in f:
        lines.append([values.get(l[0]), values.get(l[2])])
        lines_original.append([l[0], l[2]])

    total_score = 0
    for l in lines:
        score = 0
        if l[0] == l[1]: # tie
            score = l[1] + 3
        else:
            if (l[0] == 1 and l[1] == 2) or (l[0] == 2 and l[1] == 3) or (l[0] == 3 and l[1] == 1): # winning conditions
                score = l[1] + 6
            else: # you lose
                score = l[1]
        total_score += score

    # part 1: total score if you follow the script
    print(total_score)

    # part 2: do the thing i originally did for part 1 and deleted - Z == win, Y == draw, X == lose
    total_score = 0
    for l in lines_original:
        score = 0
        if l[1] == 'Z': 
            _, score = _win(l[0])
            score += 6
        elif l[1] == 'Y':
            _, score = _tie(l[0])
            score += 3
        else:
            _, score = _lose(l[0])

        total_score += score

    print(total_score)


def day3():
    infile = open("./input-3.txt", "r")
    lines = infile.readlines()

    rucksacks = []
    rucksacks_original = []
    for l in lines:
        l = l.strip()
        rucksacks.append([l[0:len(l)//2], l[len(l)//2:]])
        rucksacks_original.append(l)

    common = []
    for r in rucksacks:
        c = list(set(r[0]) & set(r[1]))
        for cc in c:
            common.append(cc)

    alphabet = list(string.ascii_letters)
    priority = {x: index for index, x in enumerate(alphabet, start=1)}
    
    #part 1: print the sum of the priority values for the common items in each rucksack
    print(sum(priority.get(c) for c in common))

    #part 2: every 3 rucksacks is a group. print the sum of the priority of the element common to each group
    common = []
    for i in range(0, len(rucksacks_original), 3):
        c = list(set(rucksacks_original[i]) & set(rucksacks_original[i+1]) & set(rucksacks_original[i+2]))
        for cc in c:
            common.append(cc)
    
    print(sum(priority.get(c) for c in common))


def day4():
    with open('./input-4.txt', 'r') as f:
        lines = [line.rstrip() for line in f]
    
    search_pairs = []

    for l in lines:
        pairs = l.split(',')
        pair = []
        for p in pairs:
            rng = p.split('-')
            pair.append(rng)
        
        search_pairs.append(pair)

    def _fully_overlaps(r1, r2):
        if int(r1[0]) >= int(r2[0]) and int(r1[1]) <= int(r2[1]):
            return True
        elif int(r2[0]) >= int(r1[0]) and int(r2[1]) <= int(r1[1]):
            return True
        else:
            return False
    
    fully_overlap = 0
    for p in search_pairs:
        if(_fully_overlaps(p[0], p[1])):
            fully_overlap += 1

    print(f"{fully_overlap=}")

    def _partially_overlaps(r1, r2):
        r1 = [int(r1[0]), int(r1[1])]
        r2 = [int(r2[0]), int(r2[1])]

        r1 = set(i for i in range(r1[0], r1[1]+1))
        r2 = set(i for i in range(r2[0], r2[1]+1))

        if len(set(r1 & r2)) > 0:
            return True
        else:
            return False

    partially_overlap = 0
    for p in search_pairs:
        if(_partially_overlaps(p[0], p[1])):
            partially_overlap += 1

    print(f"{partially_overlap=}")


def day5():
    # with open('./input-5.txt', 'r') as f:
    #     stacks = [line.rstrip() for line in f]
    
    with open('./input-5-moves.txt', 'r') as f:
        move_strings = [line.rstrip() for line in f]
    
    # recreate stacks - structure is list of lists, where the nested list is an individual stack; stack 1 -> list[0]
    # you know what, its actually faster to just type these
    stacks = []
    stacks.append("Hacky offset")
    stacks.append(list("RGHQSBTN"))
    stacks.append(list("HSFDPZJ"))
    stacks.append(list("ZHV"))
    stacks.append(list("MZJFGH"))
    stacks.append(list("TZCDLMSR"))
    stacks.append(list("MTWVHZJ"))
    stacks.append(list("TFPLZ"))
    stacks.append(list("QVWS"))
    stacks.append(list("WHLMTDNC"))

    # parse moves as tuple (quantity, from_stack, to_stack)
    moves = []
    for m in move_strings:
        moves.append(tuple(int(i) for i in m.split() if i.isdigit()))
    
    stacks_part1 = copy.deepcopy(stacks)
    # stacks_part2 = copy.deepcopy(stacks)

    for m in moves:
        accum = []
        for i in range(0,m[0]):
            accum += stacks_part1[m[1]].pop()
        stacks_part1[m[2]] += accum
    
    # part 1: item at top of each stack as a string
    top = ""
    for s in stacks_part1[1:]:
        top += s[-1]
    
    print(f"{top=}")

    # part 2: multiple crates move at once. don't pop, take an end slice and move it. or do the same thing as part 1 but reverse accum, whatever.
    for m in moves:
        # this looks like shit because i thought i had a bug, when it turns out i fatfingered an input
        accum = ""
        accum = copy.deepcopy(stacks[m[1]][-1 * m[0]:])
        stacks[m[2]] += accum
        for i in range(0,m[0]):
            stacks[m[1]].pop()
        # print(m, accum, accum[::-1])
        # stacks[m[2]] += list(accum[::-1])
        
        for s in stacks:
             print(s)

    top = ""
    for s in stacks[1:]:
        top += s.pop()
    
    print(f"{top=}")


def day6():
    with open('./input-6.txt', 'r') as f:
        signal = f.readline()
    
    def head_index_of_unique_window(signal, window):
        for i in range(4, len(signal)):
            if len(set(signal[i-window:i])) == window:
                return(i)
        
        return(-1)

    # part 1: yield the head character number of the signal when the first unique 4 character segment appears
    print(f"{head_index_of_unique_window(signal, 4)=}")
    
    # part 2: same thing, but 14 characters
    print(f"{head_index_of_unique_window(signal, 14)=}")


def day7():
    # got super hacky with this 
    
    def nested_get(dic, keys):    
        for key in keys:
            dic = dic[key]
        return dic

    def nested_set(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value


    with open("input-7.txt", "r") as f:
        commands = f.readlines()

    commands = [c.strip() for c in commands]

    tree = {"/": {}}
    current_path = ["/"]

    i = 0
    for c in commands:
        i += 1
        cmd = c.split()
        print(cmd)
        if cmd[0] == "$":
            match cmd[1]:
                case "cd":
                    if cmd[2] == "/":
                        current_path = ["/"]
                    elif cmd[2] == "..":
                        current_path.pop()
                    else:
                        print(f"{cmd[2]=}")
                        current_path += [cmd[2]]
                        nested_set(tree, current_path, {})
                case "ls":
                    continue
        elif cmd[0] == "dir":
            nested_set(tree, current_path + [cmd[1]], {})
        else: # treat the command as a file instead
            insert_into = current_path + [cmd[1]]
            print(f"{insert_into=}")
            nested_set(tree, insert_into, cmd[0])
        #if i > 100:
        #    break

    print(tree)

    global global_accum
    global_accum = []

    def size_of_dirtree(dirtree, threshold):
        global global_accum
        accum = 0
        for k, v in dirtree.items():
            if isinstance(v, dict):
                # print(f"Nested dict item {k=} {v=}")
                accum += size_of_dirtree(v, threshold)
            else:
                # print(f"File item {k=} {v=}")
                accum += int(v)
        
        # modify this for part 1 vs part 2
        if accum >= threshold:
            print(f"{dirtree=} {accum=}")
            global_accum.append(accum)
        
        return accum
    
    # part 1: print sum of directory sizes where the directory is <= 100000
    print(size_of_dirtree(tree, 100000))
    print(global_accum) 
    # turns out this debugging check was useful as an input to part 2

    # part 2: print smallest dir that deleting would free enough space to install 30 000 000 update (disk is 70 000 000, use part 1 checksum to determine used space)
    print(size_of_dirtree(tree, 1609574)) # 1609574 is the amount of space we need to free
    print(min(global_accum))
