from skip_list import *

a = SkipList()
# for _ in range(32):
#     i = randint(1, 10000)
#     a.append(i)
#     print(i)
a.from_iterable((randint(1, 10000) for _ in range(32)), tree_like=True)
print([*a])
print([*a._iterate(True)])
a.print()
