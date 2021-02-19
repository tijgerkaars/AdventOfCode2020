#-*-coding:utf8;-*-
#qpy:3
#qpy:console

from collections import Counter
inp ="""73
114
100
122
10
141
89
70
134
2
116
30
123
81
104
42
142
26
15
92
56
60
3
151
11
129
167
76
18
78
32
110
8
119
164
143
87
4
9
107
130
19
52
84
55
69
71
83
165
72
156
41
40
1
61
158
27
31
155
25
93
166
59
108
98
149
124
65
77
88
46
14
64
39
140
95
113
54
66
137
101
22
82
21
131
109
45
150
94
36
20
33
49
146
157
99
7
53
161
115
127
152
128"""

inp1="""16
10
15
5
1
11
7
19
6
12
4"""

inp2="""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

def choices(n):
    if n >= 3:
        return 3*choices(n-1)
    elif n == 2:
        return 2
    else: 
        return 1

from collections import Counter
from math import factorial

inp = sorted(map(int, (i for i in inp.splitlines())))
inp = [0] + inp + [inp[-1]+3]
print(inp)
l = len(inp)
diff = [inp[i]-inp[i-1] for i in range(1,l)]
print(f" {diff}")
print(Counter(diff))

knots = [0]+[i+1 for i,each in enumerate(diff) if each == 3]
print(knots)
parts = list(map(len, [inp[knots[i-1]:knots[i]] for i in range(1,len(knots))]))
print(parts)
print(set(parts))

out = 1
for p in parts:
    if p == 3:
        out *= 2
    elif p == 4:
        out *= 4
    elif p == 5:
        out *= 7

print(out) # 31581162962944
"""

out = filter(lambda x : len(x)>1, ''.join(diff).split('3'))
out = list(out)
# out = map(len, out)
# out = list(out)
print(out)
# out = map(choices,(each for each in out))
# out = list(out)
# print(out)

"""


# diff = ''.join(diff)
# print(diff)
# out = map(factorial,(map(len,(each for each in diff.split('3') if each != ''))))

# print(list(out))
# summed = sum((each for each in out if each != 1))
# print(summed)

#