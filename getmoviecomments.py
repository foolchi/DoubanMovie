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
        self.query = 'INSERT INTO m' + str(self.id) + '(id, rating) VALUES (%s, %s)'

        try:
            self.cur.execute('CREATE TABLE m' + str(self.id) + '(id TINYTEXT, rating INTEGER)')

        except:
            pass
        #self.cur.execute('INSERT INTO m' + str(self.id) + '(id, rating) VALUES (%s, %s)', ('foolchi', 3))
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

    def getComments(self, url, start = False):
        print(url)
        req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"})
        conn = urllib.request.urlopen(req)
        #content = None
        try:
            content = conn.read()
        except:
            print("Sleep for %s" % url)
            time.sleep(3)
            self.getComments(url)
            return

        commentSoup = BeautifulSoup(content)

        '''
        nextPages = commentSoup.find_all(class_ = 'next')
        if (len(nextPages) == 0):
            self.nextPage = None
            return
        self.nextPage = nextPages[0].a['href']
        '''
        pages = commentSoup.find_all(id = 'paginator')[-1].find_all('a')
        if (len(pages) == 1 and not start):
            self.nextPage = None
            return
        self.nextPage = self.url + pages[-1]['href']
        comments = commentSoup.find_all(class_ = 'comment-item')
        #commentTables = commentSoup.find_all('table')
        #nOfUsers = 0
        #isEmpty = True
        for comment in comments:
            try:
                userId = self.userPattern.search(comment.a['href']).group(1)
            except AttributeError:
                continue
            #nOfUsers += 1
            rating = 0
            #if (comment.p is None):
            #    continue
            #spans = comment.p.find_all('span')
            spans = comment.find_all('span')
            for span in spans:
                classes = span['class']
                for i in range(self.nRating):
                    if ratingStrings[i] in classes:
                        rating = i + 1
                        break
                if (rating != 0):
                    print("UserId %s, rating %s" % (userId, rating))
                    self.cur.execute(self.query, (str(userId), str(rating)))
                    break
        #if (nOfUsers < 40):
        #    self.nextPage = None
        self.conn.commit()
        #time.sleep(1)

    def finish(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()