import os
import csv


with open("C:\Users\Jobber\Documents\Python Scripts\WieBetaaltWat\New\Betalingen.csv") as file:
    payments = []
    for entry in file:
        payments.append(entry.rstrip().split(";"))
file.close()

with open("C:\Users\Jobber\Documents\Python Scripts\WieBetaaltWat\New\Families.csv") as file:
    families = dict()
    for entry in file:
        entry = entry.rstrip().split(";")
        families[entry[0]] = []
        for i in range(1,len(entry)):
            families[entry[0]].append(entry[i])
file.close()

par = []
debt = dict()
for familie in families:
    for member in families[familie]:
        par.append(member)
        debt[member] = dict()

par = tuple(par)

for each in debt:
    for p in par:
        if each != p:
            debt[each][p] = 0

euro_factor = 10

for payment in payments:
    for i in range(len(payment)):
        payment[i] = payment[i].replace(",", ".")

    payer = payment[0]
    if payment[2] == "k":
        amount = int(float(payment[1]))/euro_factor
    elif payment[2] == "e":
        amount = int(float(payment[1]))
    else:
        print "invalid entry:", payment
    recievers = []
    for i in range(3,len(payment)):
        if payment[i] != "":
            if payment[i] == "all":
                recievers = par
                break
            if payment[i] in families:
                for member in families[payment[i]]:
                    recievers.append(member)
            else:
                recievers.append(payment[i])
    relative_amount = float(amount) / float(len(recievers))
    for each in debt[payer]:
        if each in recievers:
            debt[payer][each] += relative_amount

for each in debt:
    remove = []
    for key in debt[each]:
        if debt[each][key] == 0:
            remove.append(key)
        else:
            debt[each][key] = round(debt[each][key],2)
    for key in remove:
        debt[each].pop(key)

remove = []
for each in debt:
    if len(debt[each]) == 0:
        remove.append(each)

for each in remove:
    debt.pop(each)



fam_debt = dict()
for each in families:
    fam_debt[each] = dict()
    for f in families:
        if f != each:
            fam_debt[each][f] = 0
print fam_debt


for debtor in debt:
    for fam in families:
        if debtor in families[fam]:
            # needed
            break
    for each in debt[debtor]:
        for member in families:
            if each in families[member]:
                # needed
                break
        if member != fam:
            fam_debt[fam][member] += debt[debtor][each]
print "test:", fam_debt

for each in fam_debt:
    remove = []
    for key in fam_debt[each]:
        if fam_debt[each][key] == 0:
            remove.append(key)
    for key in remove:
        if key in fam_debt[each]:
            fam_debt[each].pop(key)

print fam_debt


"""
for each in debt:
    print "test:", each, debt[each]
"""
os.remove("C:\\Users\\Jobber\\Documents\\Python Scripts\\WieBetaaltWat\\New\\total.csv")

with open("C:\\Users\\Jobber\\Documents\\Python Scripts\\WieBetaaltWat\\New\\Total.csv", 'wb') as new_file:
    for each in debt:
        line = []
        line.append(each)
        line.append(" ")
        for pers in debt[each]:
            line.append(pers)
            temp = str(debt[each][pers]).replace(".", ",")
            line.append(temp)
        wr = csv.writer(new_file, delimiter = ';')
        wr.writerow(line)
    for each in fam_debt:
        if len(fam_debt[each]) != 0:
            line = []
            line.append(each)
            line.append(" ")
            for fam in fam_debt[each]:
                line.append(fam)
                temp = str(fam_debt[each][fam]).replace(".",",")
                line.append(temp)
            wr = csv.writer(new_file, delimiter = ';')
            wr.writerow(line)
    wr.writerow('=SOM(D1*D2)')
