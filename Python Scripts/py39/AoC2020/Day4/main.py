import re

def str2int(i):
    try:
        int(i)
        return True
    except:
        return False


with open('Python Scripts\py39\AoC2020\Day4\input.txt') as f:
    lines = [line.replace('\n', ' ').strip().split(' ') for line in f.read().split('\n\n')]
    passports = [{each.split(':')[0]:each.split(':')[1] for each in doc} for doc in lines]
    print(passports)

checks = {
'byr' : lambda x : len(x) == 4 and 1920 <= int(x) <= 2002,
'iyr' : lambda x : len(x) == 4 and 2010 <= int(x) <= 2020,
'eyr' : lambda x : len(x) == 4 and 2020 <= int(x) <= 2030,
'hgt' : lambda x : 150 <= int(x[:-2]) <= 193  if x[-1] == 'm' else 59 <= int(x[:-2]) <= 76,
'hcl' : lambda x : True if re.search('^#[a-fA-F0-9]{6}$',x) else False,
'ecl' : lambda x : x in set("amb blu brn gry grn hzl oth".split(' ')),
'pid' : lambda x : str2int(x) and len(x) == 9 ,
'cid' : lambda x : True
}

checks.pop('cid', None)

valid = 0
for each in passports:
    for key in checks.keys():
        try:
            if not checks[key](each[key]):
                break
        except:
            break
    else:
        valid += 1

# != 103

print(valid)

print('byr', True  ==  checks['byr']('2002'))
print('byr', False == checks['byr']('2003'))
print('hgt', True  ==  checks['hgt']('60in'))
print('hgt', True  ==  checks['hgt']('190cm'))
print('hgt', False == checks['hgt']('190in'))
print('hgt', False == checks['hgt']('190'))
print('hcl', True  ==  checks['hcl']('#123abc'))
print('hcl', False == checks['hcl']('#123abz'))
print('hcl', False == checks['hcl']('123abc'))
print('ecl', True  ==  checks['ecl']('brn'))
print('ecl', False == checks['ecl']('wat'))
print('pid', True  ==  checks['pid']('000000001'))
print('pid', False == checks['pid']('0123456789'))

"""
byr valid:   2002
byr invalid: 2003
hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190
hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc
ecl valid:   brn
ecl invalid: wat
pid valid:   000000001
pid invalid: 0123456789
"""