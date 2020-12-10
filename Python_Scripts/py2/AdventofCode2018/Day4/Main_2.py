with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day4\sorted_input.csv") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines

import datetime

d1 = datetime.datetime.strptime('2011:10:01:10:30:00', '%Y:%m:%d:%H:%M:%S')

def getTime(string):
    trash, time = string.split("[")
    time, trash = time.split("]")
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
    return time

schedule = dict()
length = len(lines)

for i in range(length):
    if "Guard" in lines[i]:
        time,guard = lines[i].split("#")
        time = getTime(time)
        guard,trash = guard.split(" ",1)
        guard = int(guard)
        day = time.date()
        if guard not in schedule:
            schedule[guard] = dict()
        schedule[guard][day] = dict()
        if time.hour >= 0 and time.hour < 12:
            schedule[guard][day]["start"] = [time.hour, time.minute]
        elif time.hour == 23:
            schedule[guard][day]["start"] =[0, -1*(60-time.minute)]
        else:
            schedule[guard][day]["start"] =[-1*(24-time.hour), -1*(60-time.minute)]
        j = 1
        while "Guard" not in lines[i+j]:
            time2 = getTime(lines[i+j])
            dif = int((time2 - time).total_seconds()/60)
            time = time2
            if not "ritem" in schedule[guard][day]:
                schedule[guard][day]["ritem"] = ""
            if "up" in  lines[i+j]:
                for minute in range(dif):
                    schedule[guard][day]["ritem"] = schedule[guard][day]["ritem"] + "#"
                if "asleep" in schedule[guard]:
                    schedule[guard][day]["asleep"] += dif
                else:
                    schedule[guard][day]["asleep"] = dif
            elif "asleep" in lines[i+j]:
                for minute in range(dif):
                    schedule[guard][day]["ritem"] = schedule[guard][day]["ritem"] + "."
                if "awake" in schedule[guard]:
                    schedule[guard][day]["awake"] += dif
                else:
                    schedule[guard][day]["awake"] = dif
            j += 1
            if i+j >= length:
                break
        #break

for each in schedule:
    for day in schedule[each]:
        if "awake" not in schedule[each][day]:
            schedule[each][day][ "awake"] = 0
        if "asleep" not in schedule[each][day]:
            schedule[each][day]["asleep"] = 0
        if "ritem" not in schedule[each][day]:
            schedule[each][day][ "ritem"] = ""
# sleepyBoy is the guard that slept the most
# sleepyTimes is the ammount of sleep he got
sleepyBoy = -1
sleepyTimes = 0
# for each guard that is in the input
for guard in schedule:
    # counter for the minutes slept by a guard
    minutesAsleep = 0
    # for each day that the guard was on duty
    for day in schedule[guard]:
        # add the minutes slept that day to the total
        minutesAsleep += schedule[guard][day]["asleep"]
    # if that guard slept more than any other guard thus far
    if minutesAsleep > sleepyTimes:
        # set that amount of sleep as the new goal
        sleepyTimes = minutesAsleep
        # note down which guard slept that amount
        sleepyBoy = guard
print "sleepyBoy:", sleepyBoy, "sleepyTimes:", sleepyTimes

# to make the counting easier the ritem will be padded
# if the guard stated his shift earlier or later
earliestStartMinute = 0
earliestStartHour = 0
for guard in schedule:
    for day in schedule[guard]:
        if schedule[guard][day]["start"][1] < earliestStartMinute:
            earliestStartMinute = schedule[guard][day]["start"][1]
        if schedule[guard][day]["start"][0] < earliestStartHour:
            earliestStartMinute = schedule[guard][day]["start"][0][:]
print "earliestStartHour:", earliestStartHour, "earliestStartMinute:", earliestStartMinute

# now that we know how much before or after midnight the shift started
longestShift = 0
# pad Left
## for each day that this guard had a shift
for guard in schedule:
    for day in schedule[guard]:
        # if the guard started his shift later than the earliest start
        if schedule[guard][day]["start"][1] > earliestStartMinute:
            # by how much is it different
            dif = schedule[guard][day]["start"][1] - earliestStartMinute
            temp = ""
            # add i amount of minutes awake together
            for i in range(dif):
                temp = temp + "."
            # add these minutes awake before the shift
            schedule[guard][day]["ritem"] = temp + schedule[guard][day]["ritem"]
        # if this shift is now the longest shift
        if len(schedule[guard][day]["ritem"]) > longestShift:
            # mark down how long it was for the padding on the right
            longestShift = len(schedule[guard][day]["ritem"])
print "longestShift:", longestShift

# for each day in the guard schedule
for guard in schedule:
    for day in schedule[guard]:
        # if that shift was shorter than the longest shift
        if len(schedule[guard][day]["ritem"]) < longestShift:
            # add padding to the right
            for i in range(len(schedule[guard][day]["ritem"]),longestShift):
                schedule[guard][day]["ritem"] = schedule[guard][day]["ritem"] + "."

# the guard that slept the most on a specific minute
sleepyBoy = -1
# that minute
mostSleptMinute = 0
# for each guard
for guard in schedule:
    # the minute on which this guard slept the most
    mostSlept = 0
    # for each minute in their shifts
    for minutes in range(longestShift):
        # store this minute for all days
        minute = ""
        # for each of their shifts
        for day in schedule[guard]:
            # add the minute of this day to the string
            minute = minute + schedule[guard][day]["ritem"][minutes]
        # if this minute is the minute that this guard slept the most of his shifts
        if minute.count("#") > mostSlept:
            # his most slept minute is that minute
            mostSlept = minute.count("#")
        # if this minute is the minute in which any guard has slept the most
        if mostSleptMinute < mostSlept:
            # the guard that slept the most is that guard
            sleepyBoy = guard
            # and the minute that was most slept in by a guard is now the most slept in minute
            mostSleptMinute = minutes

# the non zero indexed most slept in minute relative to 00:00
mostSleptMinute = mostSleptMinute + 1 + earliestStartMinute

print  "sleepyBoy:", sleepyBoy, "mostSleptMinute:", mostSleptMinute, "mostSlept:", mostSlept
print "answer:", sleepyBoy, "*", mostSleptMinute, "=" , sleepyBoy * mostSleptMinute




end = True
