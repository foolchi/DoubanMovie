#!/usr/bin/python3
#-*-coding: utf-8-*-#
from bs4 import BeautifulSoup
import re
import cymysql
import urllib.request
import time


ratingStrings = ['allstar10', 'allstar20', 'allstar30', 'allstar40', 'allstar50']

class GetMovieComments:
    def __init__(self, id):
        self.id = id
        self.url = 'http://movie.douban.com/subject/' + str(id) + '/comments'
        self.nRating = len(ratingStrings)
        self.userPattern = re.compile(r'/people/((\d|\D)+)/$')

    def setDatabase(self, user, passwd, db):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = cymysql.connect(user = self.user, passwd = self.passwd, db = self.db
        )
        self.cur = self.conn.cursor()
        self.query = 'INSERT INTO m' + str(self.id) + '(id, rating, comment) VALUES (%s, %s, %s)'

        try:
            self.cur.execute('CREATE TABLE m' + str(self.id) + '(id TINYTEXT, rating INTEGER, comment MEDIUMTEXT)')

        except:
            pass
        self.cur.execute('INSERT INTO m' + str(self.id) + '(id, rating, comment) VALUES (%s, %s, %s)', ('foolchi', 3, "Test"))
        print("database created")

    def getnComments(self):
        print(self.url)
        req = urllib.request.Request(self.url, headers={'User-Agent' : "Chrome"})
        con = urllib.request.urlopen(req)
        nSoup = BeautifulSoup(con.read())
        #print(nSoup.prettify())
        nComments = nSoup.find(class_ = 'fleft')
        numberPattern = re.compile(r'\d+')
        number = int(numberPattern.search(nComments.get_text()).group(0))
        number = number if number > 0 else 0
        self.nComments = number
        pages = nSoup.find_all(id = 'paginator')[-1].find_all('a')
        self.nextPage = self.url + pages[-1]['href']
        comments = nSoup.find_all(class_ = 'comment-item')
        for comment in comments:
            userId = self.userPattern.search(comment.a['href']).group(1)
            rating = 0
            spans = comment.find_all('span')
            for span in spans:
                classes = span['class']
                for i in range(self.nRating):
                    if ratingStrings[i] in classes:
                        rating = i + 1
                        break
                if (rating != 0):
                    break
            commentString = str(comment.p.contents[0])
            print("UserId %s, rating %s, commentString %s" % (userId, rating, commentString))
            self.cur.execute(self.query, (str(userId), str(rating), str(commentString)))
        self.conn.commit()
        return number

    def getAllComments(self):
        self.getnComments()

        return

    def getComments(self, url):
        print(url)
        req = urllib.request.Request(url, headers={'User-Agent' : "Chrome"})
        conn = urllib.request.urlopen(req)
        content = None
        try:
            content = conn.read()
        except:
            print("Sleep for %s" % url)
            time.sleep(3)
            self.getComments(url)
            return
        commentSoup = BeautifulSoup(content)
        pages = commentSoup.find_all(id = 'paginator')[-1].find_all('a')
        if (len(pages) == 1):
            self.nextPage = None
            return
        self.nextPage = self.url + pages[-1]['href']
        comments = commentSoup.find_all(class_ = 'comment-item')
        for comment in comments:
            userId = self.userPattern.search(comment.a['href']).group(1)
            rating = 0
            spans = comment.find_all('span')
            for span in spans:
                classes = span['class']
                for i in range(self.nRating):
                    if ratingStrings[i] in classes:
                        rating = i + 1
                        break
                if (rating != 0):
                    break
            commentString = str(comment.p.contents[0])
            print("UserId %s, rating %s, commentString %s" % (userId, rating, commentString))
            self.cur.execute(self.query, (str(userId), str(rating), str(commentString)))
        self.conn.commit()


    def finish(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()



    def __end__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


get = 2

if (get == 0):
    g = GetMovieComments(25805741)
    g.setDatabase('foolchi', '1', 'movie')
    g.getnComments()
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
    cur.execute('SELECT * FROM m25805741')
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

'''
f = open('movie.html')
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
