import re

eq = '2 * 3 + 4 * 0 '.replace(' ','')


eq = re.split('([\*+])', eq)


print(eq)