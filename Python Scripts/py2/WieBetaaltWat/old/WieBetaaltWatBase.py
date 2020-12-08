import WieBetaaltWatDeelnemers
import WieBetaaltWatBetalingen

participants = WieBetaaltWatDeelnemers.Families
payments = WieBetaaltWatBetalingen.Payments

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

# print the dict values
print "Intermediat debts:"
for i in part:
    print i, part[i]

print "\nEvening out\n"

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

print "Intermediat debts:"
for i in part:
    print i, part[i]
