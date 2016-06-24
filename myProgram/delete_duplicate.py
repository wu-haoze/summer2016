import sys

with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()

s = set([])

with open(sys.argv[2], 'w') as out_file:
    for line in content:
        new_line = line.split()
        if new_line[0] not in s:
            out_file.write(line)
            s.add(new_line[0])

