#Simple Crawler for movie rating in Douban movie
This is a simple crawler for movie rating in [Douban Movie](http://movie.douban.com), you can get all the users and ratings for a given movie Id.

##Install
You need to install:
* Python3
* [CyMySql](https://github.com/nakagami/CyMySQL), python mysql client library for python2.6+
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/), Beautiful Soup provides a few simple methods and Pythonic idioms for navigating, searching, and modifying a parse tree

##How to use
It's simple:
```python
g = GetMovieComments(movieId)
g.setDatabase(user, passwd, database name)
g.getAllComments()
```