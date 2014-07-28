#!/usr/bin/python3

import cymysql
import math
import numpy as np
import matplotlib.pyplot as plt
colors = [(1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1), (0.5,0,1)]
def compare(id1, id2):
    conn = cymysql.connect(user = 'foolchi', passwd = '1', db = 'movie')
    cur = conn.cursor()
    cur.execute('SELECT * FROM m' + str(id1))
    fetchall = cur.fetchall()
    size = len(fetchall)
    dic1 = dict()
    average = 0
    avg1 = 0
    if (size <= 0):
        print("Empty")
    else:
        for info in fetchall:
            userId = info[0]
            rating = int(info[1])
            average += rating
            dic1[userId] = rating
            #comment = info[2]
            #print("userId: %s, rating: %d, comment: %s" % (userId, rating, comment))
        print("Total: %d, size: %d, average: %f" % (average, size, average / size))
        avg1 = average / size

    cur.execute('SELECT * FROM m' + str(id2))
    fetchall = cur.fetchall()
    size = len(fetchall)
    dic2 = dict()
    average = 0
    avg2 = 0
    if (size <= 0):
        print("Empty")
    else:
        for info in fetchall:
            userId = info[0]
            rating = int(info[1])
            average += rating
            dic2[userId] = rating
            #comment = info[2]
            #print("userId: %s, rating: %d, comment: %s" % (userId, rating, comment))
        print("Total: %d, size: %d, average: %f" % (average, size, average / size))
        avg2 = average / size
    print("id1 std: %f"% np.std(list(dic1.values())))
    print("id2 std: %f"% np.std(list(dic2.values())))
    cur.close()
    conn.close()
    pairs = []
    for key, value in dic1.items():
        if (key in dic2):
            temp = []
            temp.append(dic1[key])
            temp.append(dic2[key])
            pairs.append(temp)
    tables = [[0] * 5 for i in range(5)]
    for pair in pairs:
        tables[pair[0]-1][pair[1]-1] += 1
    print(tables)
    print(len(pairs))
    diff = 0
    for i in range(5):
        for j in range(5):
            diff += tables[i][j] * math.fabs((i - avg1) - (j - avg2))
    print("Overlap: ", (100 * len(pairs) / (len(dic1)+len(dic2) - len(pairs))), r'%')
    print("Diff: %f, avgDiff: %f" % (diff, diff / len(pairs)))

def trend(id, seperates = 10):
    conn = cymysql.connect(user = 'foolchi', passwd = '1', db = 'movie')
    cur = conn.cursor()
    cur.execute('SELECT * FROM m' + str(id))
    fetchall = cur.fetchall()
    size = len(fetchall)
    #dic1 = dict()
    ratings = []
    if (size <= 0):
        print("Empty")
    else:
        for info in fetchall:
            userId = info[0]
            rating = int(info[1])
            ratings.append(rating)
            #dic1[userId] = rating
        nRating = len(ratings)
        trends = []
        step = nRating // seperates
        for i in range(seperates):
            trends.append(sum(ratings[i * step: (i+1)*step]) / step)
        #print(trends)
        trends.reverse()
        return trends


#后会无期: 25805741
#小时代: 24847340
#老男孩: 25755645
#变形金刚: 7054604
#布达佩斯大饭店: 11525673
#辩护人: 21937445
id1 = 25805741
id2 = 24847340
id3 = 25755645
id4 = 7054604
id5 = 11525673
id6 = 21937445
movieDict = {'后会无期': 25805741,'小时代3': 24847340,'老男孩': 25755645,'变形金刚': 7054604, '布达佩斯大饭店': 11525673, '辩护人': 21937445}
idList = [id1, id2, id3, id4, id5, id6]


sep = 5
i = 0
for id in idList:
    plt.plot(range(sep), trend(id, sep), color = colors[i])
    i += 1
plt.show()
'''
for key1, val1 in movieDict.items():
    for key2, val2 in movieDict.items():
        if (val1 != val2):
            print("======(%s, %s)=======" % (key1, key2))
            compare(val1, val2)
'''

'''
print("==============")
compare(id4, id1)
print("==============")
compare(id4, id2)
print("==============")
compare(id3, id4)
print("==============")
'''