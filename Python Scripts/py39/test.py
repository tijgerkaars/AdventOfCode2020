import re


eq = "(((1+1)+(2+1))+(1*8+7))"
print(eq)
print(re.findall('\(([\w+*]+)\)', eq))







re.compile('(ab|aabb|aaabbb)')
tests = [ 'a'*i + 'b'*i for i in range(1,10) ]
for each in tests:
    print(re.match(f"({'|'.join([ 'a'*i + 'b'*i for i in range(1,10) ])})", each))










