list2 = [1,2,3,4,5]
list1 = [1,2,3,4,5,6]

print "modulo", 9%9

result =  all(elem in list1  for elem in list2)

if result:
    print("Yes, list1 contains all elements in list2")
else :
    print("No, list1 does not contains all elements in list2")

if str(list2[-1]) != str(4):
    print "test"

def stringToList(string):
    spliced = []
    spliced = string.split("]")
    splicedIntRaster = []
    for each in spliced:
        splicedInt = []
        for characters in each:
            if characters.isdigit():
                splicedInt.append(int(characters))
        if splicedInt:
            splicedIntRaster.append(splicedInt)
    raster = []
    for y in range(9):
        temp = []
        for x in range(9):
            temp.append(splicedIntRaster[y*9+x])
        raster.append(temp)
    return raster



a = [[[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[6], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [7], [3]], [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9]], [[1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [2], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8]], [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[8], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]]
print len(a)
a = str(a)
stringToList(a)
