import re


def get_numbered_duplicate(names, q):
    if q not in names:
        return q
    qregex = '^' + re.escape(q) + r'( \([1-9]\d*\))?$'  # the_attr, the_attr (1), the_attr (2) ...
    nums = []
    for name in names:
        if re.match(qregex, name) and name != q:
            num = int(name.split('(')[-1][:-1])
            nums.append(num)
    i = 1
    while True:
        if i not in nums:
            break
        i = i + 1
    return q + ' (%d)' % i
