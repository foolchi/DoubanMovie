#!/usr/bin/python3
#-*-coding: utf-8-*-#
from bs4 import BeautifulSoup
import re
import cymysql
import urllib.request
import time

# Rating strings for movie.douban.com
ratingStrings = ['allstar10', 'allstar20', 'allstar30', 'allstar40', 'allstar50']

class GetMovieComments:
    def __init__(self, id):
        self.id = id
        self.url = 'http://movie.douban.com/subject/' + str(id) + '/comments'
        self.nRating = len(ratingStrings)
        self.userPattern = re.compile(r'/people/((\d|\D)+)/$') #Regular expression for users

    def setDatabase(self, user, passwd, db):
        '''
        :param user: user name for database
        :param passwd: password for database
        :param db: name of database to store the rating data
        :return: None
        '''
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = cymysql.connect(user = self.user, passwd = self.passwd, db = self.db)
        self.cur = self.conn.cursor()
        self.query = 'INSERT INTO m' + str(self.id) + '(id, rating) VALUES (%s, %s)'
        # Create the table, if exists, pass
        try:
            self.cur.execute('CREATE TABLE m' + str(self.id) + '(id TINYTEXT, rating INTEGER)')
            print("database created")
        except:
            print('database exists')
            pass

    def getnComments(self):
        ''' Get the number of comments '''
        print(self.url)
        req = urllib.request.Request(self.url, headers={'User-Agent' : "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"})
        con = urllib.request.urlopen(req)
        nSoup = BeautifulSoup(con.read())
        nComments = nSoup.find(class_ = 'fleft')
        numberPattern = re.compile(r'\d+')
        number = int(numberPattern.search(nComments.get_text()).group(0))
        number = number if number > 0 else 0
        self.nComments = number
        return number

    def getAllComments(self):
        self.getComments(self.url, True)
        while (self.nextPage is not None):
            self.getComments(self.nextPage)

    def getComments(self, url, start = False):
        print(url)
        req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"})
        conn = urllib.request.urlopen(req)
        try:
            content = conn.read()
        except:
            print("Sleep for %s" % url)
            time.sleep(3)
            self.getComments(url)
            return

        commentSoup = BeautifulSoup(content)
        pages = commentSoup.find_all(id = 'paginator')[-1].find_all('a')
        if (len(pages) == 1 and not start):
            self.nextPage = None
            return
        self.nextPage = self.url + pages[-1]['href']
        comments = commentSoup.find_all(class_ = 'comment-item')

        for comment in comments:
            try:
                userId = self.userPattern.search(comment.a['href']).group(1)
            except AttributeError:
                continue
            rating = 0
            spans = comment.find_all('span')
            for span in spans:
                classes = span['class']
                for i in range(self.nRating):
                    if ratingStrings[i] in classes:
                        rating = i + 1
                        break
                if (rating != 0):
                    #print("UserId %s, rating %s" % (userId, rating))
                    self.cur.execute(self.query, (str(userId), str(rating)))
                    break
        self.conn.commit()
        time.sleep(1)

    def finish(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()