#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import cymysql
import urllib.request


class GetMovieComments:
    def __init__(self, id):
        self.id = id
        self.url = "http://movie.douban.com/subject/" + str(id)
        self.getnComments()
        print("Comments: %d" % self.nComments)

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
        #cur.execute('INSERT INTO m' + str(self.id) + '(id, rating) VALUES (%s, %s)', ('foolchi', 3))
        print("database created")

    def getnComments(self):
        print(self.url + '/comments')
        req = urllib.request.Request(self.url + '/comments', headers={'User-Agent' : "Chrome"})
        con = urllib.request.urlopen(req)
        nSoup = BeautifulSoup(con.read())
        print(nSoup.prettify())
        nComments = nSoup.find(class_ = 'fleft')
        numberPattern = re.compile(r'\d+')
        number = int(numberPattern.search(nComments.get_text()).group(0))
        number = number if number > 0 else 0
        self.nComments = number
        return number

    def __end__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

#g = GetMovieComments(25805741)
#g.setDatabase('foolchi', '1', 'movie')

f = open('movie.html')
soup = BeautifulSoup(f)
#print(soup.prettify())
comment = soup.find_all(class_ = "comment-item")
i = 0
for c in comment:
    #print(c)
    i += 1
    userPattern = re.compile(r'/people/((\d|\D)+)/$')

    print(c.a.get('href'))
    print(userPattern.search(c.a.get('href')).group(1))
    print("=============")
print("Total: %d" % i)
