#!/usr/bin/python3
#-*-coding: utf-8-*-#
from bs4 import BeautifulSoup
import re
import cymysql
import urllib.request
import time
from getmoviecomments import GetMovieComments
import getmoviecomments
ratingStrings = getmoviecomments.ratingStrings
get = 0
#后会无期: 25805741
#小时代: 24847340
#老男孩: 25755645
#变形金刚: 7054604
#布达佩斯大饭店: 11525673
#辩护人: 21937445
currentId = 21937445
if (get == 0):
    g = GetMovieComments(currentId)
    g.setDatabase('foolchi', '1', 'movie')
    #g.getnComments()
    g.getComments(g.url, True)
    #g.getComments('http://movie.douban.com/subject/25805741/comments')
    #print(g.nextPage)
    while (g.nextPage is not None):
        g.getComments(g.nextPage)
    #print(g.nextPage)
    #g.getComments(g.nextPage)
    #g.getComments(g.nextPage)
    g.finish()

if (get == 2):
    conn = cymysql.connect(user = 'foolchi', passwd = '1', db = 'movie')
    cur = conn.cursor()
    cur.execute('SELECT * FROM m' + str(currentId))
    fetchall = cur.fetchall()
    size = len(fetchall)
    average = 0
    if (size <= 0):
        print("Empty")
    else:
        for info in fetchall:
            #userId = info[0]
            average += int(info[1])
            #comment = info[2]
            #print("userId: %s, rating: %d, comment: %s" % (userId, rating, comment))
        print("Total: %d, size: %d, average: %f" % (average, size, average / size))
    cur.close()
    conn.close()

if (get == 3):
    f = open('collections_empty.html')
    soup = BeautifulSoup(f)
    tables = soup.find_all('table')
    userPattern = re.compile(r'/people/((\d|\D)+)/$')
    ratings = len(ratingStrings)

    for table in tables:
        try:
            userId = userPattern.search(table.a.get('href')).group(1)
        except AttributeError:
            continue
        print(userId)
        rating = 0
        if (table.p != None):
            spans = table.p.find_all('span')
            #print(table)
            for span in spans:
                #print(span)
                classes = span['class']
                #print(classes)
                for i in range (ratings):
                    if ratingStrings[i] in classes:
                        rating = i + 1
                        break
                #print('--------------')
                if (rating != 0):
                    print("userId: %s, rating: %d" % (userId, rating))
                    print('==============')
                    break
    nextPages = soup.find_all(class_ = 'next')
    nextPage = nextPages[0].a['href']
    if len(soup.find_all(class_ = 'prev')) == 0:
        print('Empty')
    print(nextPage)




#compare()
'''


f = open('collections.html')
soup = BeautifulSoup(f)
#print(soup.prettify())
comment = soup.find_all(class_ = "comment-item")
count = 0
for c in comment:
    #print(c)
    count += 1

    userPattern = re.compile(r'/people/((\d|\D)+)/$')

    #print(c.a.get('href'))
    print(userPattern.search(c.a.get('href')).group(1))
    rating = 0
    spans = c.find_all('span')
    for span in spans:
        classes = span['class']
        for i in range(5):
            if ratingStrings[i] in classes:
                rating = i + 1
                break
        if (rating != 0):
            break
    print("Rating:" + str(rating))
    #if (c.p.a != None):
        #del c.p['a']
    print(c.p.contents[0])
    #print(c.p.string)
    #print(c.p)
    print("=============")
pages = soup.find_all(id = 'paginator')
pageLink = pages[-1].find_all('a')[-1]['href']
print(pageLink)

print("Total: %d" % count)
'''