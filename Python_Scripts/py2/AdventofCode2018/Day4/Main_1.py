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
for day in schedule[sleepyBoy]:
    if schedule[sleepyBoy][day]["start"][1] < earliestStartMinute:
        earliestStartMinute = schedule[sleepyBoy][day]["start"][1]
    if schedule[sleepyBoy][day]["start"][0] < earliestStartHour:
        earliestStartMinute = schedule[sleepyBoy][day]["start"][0][:]

# now that we know how much before or after midnight the shift started
longestShift = 0
# pad Left
## for each day that this guard had a shift
for day in schedule[sleepyBoy]:
    # if the guard started his shift later than the earliest start
    if schedule[sleepyBoy][day]["start"][1] > earliestStartMinute:
        # by how much is it different
        dif = schedule[sleepyBoy][day]["start"][1] - earliestStartMinute
        temp = ""
        # add i amount of minutes awake together
        for i in range(dif):
            temp = temp + "."
        # add these minutes awake before the shift
        schedule[sleepyBoy][day]["ritem"] = temp + schedule[sleepyBoy][day]["ritem"]
    # if this shift is now the longest shift
    if len(schedule[sleepyBoy][day]["ritem"]) > longestShift:
        # mark down how long it was for the padding on the right
        longestShift = len(schedule[sleepyBoy][day]["ritem"])

test = []
# for each day in the guard schedule
for day in schedule[sleepyBoy]:
    # if that shift was shorter than the longest shift
    if len(schedule[sleepyBoy][day]["ritem"]) < longestShift:
        # add padding to the right
        for i in range(len(schedule[sleepyBoy][day]["ritem"]),longestShift):
            schedule[sleepyBoy][day]["ritem"] = schedule[sleepyBoy][day]["ritem"] + "."
    test.append(schedule[sleepyBoy][day]["ritem"])

# any just to get the length
for any in schedule[sleepyBoy]:
    # var to store the minutes
    overview = []
    # for each minute each shift
    for minute in range(len(schedule[sleepyBoy][any]["ritem"])):
        # store the minutes slept in a string
        minutes = ""
        # for each day the guard had a shift
        for day in schedule[sleepyBoy]:
            # add the minute of each day into 1 string
            minutes = minutes + schedule[sleepyBoy][day]["ritem"][minute]
        overview.append(minutes)
    temp = 0
    minute = 0
    # for each minute in a shift
    for i in range(len(overview)):
        # if there are more minutes slept in this minute than in those before it
        if overview[i].count("#") > temp:
            temp = overview[i].count("#")
            minute = i +1
    print "minute:", minute, "sleepyBoy:", sleepyBoy, "earliestStartMinute:", earliestStartMinute
    print "answer:", (minute) * sleepyBoy
    break
