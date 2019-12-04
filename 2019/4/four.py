#! /usr/bin/env python


candidates = []
for i in range(156218, 652528):
    password = str(i)
    for i in range(len(password) - 1):
        if password[i] == password[i+1]:
            break
    else:
        continue  # no two adjacent digits are the same
    for i in range(len(password) - 1):
        if password[i] > password[i+1]:
            break
    else:
        # only increasing digits
        candidates.append(password)

print("Part one:", len(candidates))


count = 0
for password in candidates:
    if any(password.count(digit) == 2 for digit in set(password)):
        count += 1

print("Part two:", count)
