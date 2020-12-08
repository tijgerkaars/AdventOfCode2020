import WieBetaaltWatDeelnemers
import WieBetaaltWatBetalingen
from xlutils.copy import copy
import xlwt
import xlrd

# parse the payments from excel
workbook = xlrd.open_workbook("C:\Users\Jobber\Documents\Python Scripts\WieBetaaltWat\Betalingen.xlsx")
sheet = workbook.sheet_by_index(0)
ResultSheet = copy(sheet)

# ______ Parse the Families to work with the base programe ______________________
column = []
for rowx in range(sheet.nrows):
    temp = []
    cols = sheet.row_values(rowx)
    for each in cols:
        if isinstance(each, unicode):
            each = str(each)
        temp.append(each)
    column.append(temp)

participants = []
FamilyRow = 0
ParticipantRow = 0



for i in range(len(column)):
    if "Groep" in column[i]:
        FamilyRow = i
    if "Naam" in column[i]:
        ParticipantRow = i

for i in range(len(column[FamilyRow])):
    column[FamilyRow][i] = column[FamilyRow][i].title()
    name = column[FamilyRow][i]
    if name != "Groep" and [name] not in participants:
        participants.append([name])

for j in range(len(column[ParticipantRow])):
    for each in participants:
        if each[0] == column[FamilyRow][j]:
            column[ParticipantRow][j] = column[ParticipantRow][j].title()
            each.append(column[ParticipantRow][j])

print "participants:", participants

# ______ Done parse the Families to work with the base programe ______________________

# ______ Parse the payments to work with the base programe ___________________________
payments = []

Kosten = []
Deelnemers = []
Betaald = []

column = []
for coly in range(sheet.ncols):
    temp = []
    cols = sheet.col_values(coly)
    for each in cols:
        if isinstance(each, unicode):
            each = str(each)
        temp.append(each)
    if "Kosten" in temp:
        start = 0
        for i in range(len(temp)):
            if temp[i] == "Kosten":
                start = i
                break
        for i in range(start+1, len(temp)):
            Kosten.append(temp[i])
    if "Betaald" in temp:
        start = 0
        for i in range(len(temp)):
            if temp[i] == "Betaald":
                start = i
                break
        for i in range(start+1, len(temp)):
            Betaald.append(temp[i])
    if "Deelnemers" in temp:
        start = 0
        for i in range(len(temp)):
            if temp[i] == "Deelnemers":
                start = i
                break
        for i in range(start+1, len(temp)):
            names = temp[i].split(", ")
            for j in range(len(names)):
                names[j] = names[j].title()
            Deelnemers.append(names)

print "Kosten:", Kosten
print "Deelnemers:", Deelnemers
print "Betaald:", Betaald

if len(Kosten) == len(Deelnemers) and len(Kosten) == len(Betaald):
    print "Good"
    for i in range(len(Betaald)):
        payments.append([])
        payments[i].append(Betaald[i])
        payments[i].append(Kosten[i])
        for each in Deelnemers[i]:
            payments[i].append(each)

else:
    print "Shit fucked up"

print payments

part = dict()

# >--> for every group in the participants
for family in participants:
    # for each member of the group(, fist place = group name)
    for i in range(1,len(family)):
        # >--> create a dict to keep the depts in
        debt = dict()
        # for each group
        for y in participants:
            # for each member
            for x in range(1,len(y)):
                # so the member can't owh themselfs
                if y[x] != family[i]:
                    # start it at 0
                    debt[y[x]] = 0
        # add the name as the dict key and the groupname and debts as  values
        part[family[i]] = [family[0], debt]

# from the imported payment
for payment in payments:
    # who payed
    payed = payment[0]
    # if the person who paid participated
    if payment.count(payed) == 2:
        cost = payment[1]/(len(payment)-2)
    # if they didn't
    elif payment.count(payed) == 1:
        cost = payment[1]/(len(payment)-2)
    # if something fucks up
    else:
        print "Shit's fucked up"
        cost = 0
    # add the cost to the dept dict value of the person who payed
    for i in range(2,len(payment)):
        if payment[i] != payed:
            part[payed][1][payment[i]] = cost

"""
# print the dict values
print "Intermediat debts:"
for i in part:
    print i, part[i]

print "\nEvening out\n"
"""

# even out debts
# part[each] is the dict of debts
for each in part:
    #part[each] is the dict of all others
    for others in part:
        if each != others:
            if part[others][1][each] > part[each][1][others]:
                part[others][1][each] -= part[each][1][others]
                part[each][1][others] = 0
            elif part[others][1][each] < part[each][1][others]:
                part[each][1][others] -= part[others][1][each]
                part[others][1][each] = 0
"""
print "Evening Done:"
for i in part:
    print i, part[i]
"""
import xlutils
