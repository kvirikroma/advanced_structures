from skip_list import *

a = SkipList()
for _ in range(16):
    i = randint(1, 10000)
    a.append(i)
    print(i)
print([*a])
print([*a._iterate(True)])
