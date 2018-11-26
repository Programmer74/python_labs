import untangle

from flask import Flask
from flask import render_template
from flask import request
import requests
import sqlite3
import urllib
import re
from datetime import datetime

app = Flask(__name__, static_url_path='/static')


def fetch_rss_xml(url):
    return requests.get(url).text


@app.route("/feed/update/<id>")
def update_feed(id=-1):
    if id == -1:
        return "error: plz specify id"
    print("Issued update on", id)
    sql = "SELECT * FROM feeds WHERE id = ?"
    conn = sqlite3.connect("rss.db")
    c = conn.cursor()
    c.execute(sql, (id,))
    rows = c.fetchall()
    if len(rows) == 0:
        return "error: no such id"
    url = rows[0][4]
    xml = fetch_rss_xml(url)
    doc = untangle.parse(xml)
    # print(doc)
    title = doc.rss.channel.title.cdata
    # print(title)
    for item in doc.rss.channel.item:
        # print(item.title.cdata)
        # print(item.link.cdata)
        # print(item.description.cdata)
        c = conn.cursor()
        sql = "SELECT * FROM feed_contents WHERE feed_id = ? AND url = ?"
        c.execute(sql, (id, item.link.cdata))
        rows = c.fetchall()
        if len(rows) == 0:
            c = conn.cursor()
            sql = \
                "INSERT or REPLACE INTO feed_contents (url, title, content, feed_id, pub_at) " \
                "VALUES (?,?,?,?,?)"
            convdate = 0
            try:
                convdate = datetime.strptime(item.pubDate.cdata, "%a, %d %b %Y %H:%M:%S GMT")
            except ValueError:
                convdate = datetime.strptime(item.pubDate.cdata, "%a, %d %b %Y %H:%M:%S %z")

            c.execute(sql, (item.link.cdata, item.title.cdata, item.description.cdata, id,
                            convdate))
            conn.commit()
            print("Inserted " + item.link.cdata + " " + item.pubDate.cdata)
        else:
            print("Already exists " + item.link.cdata)
    return "ok"


@app.route("/feed/view/<id>")
def view_feed(id=-1):
    if id == -1:
        return "error: plz specify id"

    page = request.args.get('page')
    if page is None:
        page = 1
    page = int(page) - 1

    offset = page * 10
    limit = 10

    sql = "SELECT * FROM feeds WHERE id = ?"
    conn = sqlite3.connect("rss.db")
    c = conn.cursor()
    c.execute(sql, (id,))
    rows = c.fetchall()
    if len(rows) == 0:
        return "error: no such id"

    title = rows[0][1]

    c = conn.cursor()
    sql = "SELECT COUNT(*) FROM feed_contents WHERE feed_id = ?"
    c.execute(sql, (id,))
    rows = c.fetchall()
    totalcount = rows[0][0]

    c = conn.cursor()
    sql = "SELECT * FROM feed_contents WHERE feed_id = ? ORDER BY pub_at DESC " \
          "LIMIT ? OFFSET ? "
    c.execute(sql, (id, limit, offset))
    rows = c.fetchall()

    entries = []
    for row in rows:
        entry = []
        entry.append(row[0])  # id
        entry.append(row[1])  # url
        entry.append(row[2])  # title

        content = row[3]
        content = re.sub(r'<br>', '!br!', str(content))
        content = re.sub(r'<.+?>', '', str(content))
        content = re.sub(r'!br!', '<br>', str(content))
        # print(content)

        entry.append(content)  # content
        entry.append(row[4])  # parent_id
        entry.append(row[5])  # date
        entries.append(entry)

    pagescount = totalcount // limit + 1
    # print(offset, limit, totalcount, pagescount)

    pages = range(1, pagescount + 1)

    return render_template('feed.html', title=title,
                           entries=entries, feed_id=id, pages=pages, currentpage=(page + 1))


# http://127.0.0.1:5000/feed/add/https%253A%252F%252Fhabr.com%252Frss%252Finteresting%252F
# http://127.0.0.1:5000/feed/add/http%253A%252F%252Frss.nytimes.com%252Fservices%252Fxml%252Frss%252Fnyt%252FTechnology.xml
@app.route("/feed/add/<url>")
def add_feed(url=""):
    print(url)
    if url == "":
        return render_template('error.html')
    url = urllib.parse.unquote(url)
    print(url)
    xml = fetch_rss_xml(url)
    doc = untangle.parse(xml)
    title = doc.rss.channel.title.cdata
    description = doc.rss.channel.description.cdata
    link = doc.rss.channel.link.cdata
    print(link)
    sql = "SELECT * FROM feeds WHERE link = ?"
    conn = sqlite3.connect("rss.db")
    c = conn.cursor()
    c.execute(sql, (url,))
    rows = c.fetchall()
    if len(rows) != 0:
        return "error: already exists"

    sql = \
        "INSERT or REPLACE INTO feeds (name, description, link, url) " \
        "VALUES (?,?,?,?)"
    print(sql)
    conn = sqlite3.connect("rss.db")
    c = conn.cursor()
    c.execute(sql, (title, description, link, url))
    conn.commit()

    return "ok"


@app.route("/")
def list_feeds():
    conn = sqlite3.connect("rss.db")
    c = conn.cursor()
    c.execute("""Select * from feeds""")
    rows = c.fetchall()
    return render_template('feeds.html', entries=rows)


if __name__ == "__main__":
    connection = sqlite3.connect("rss.db")

    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS feeds
                      (id integer primary key autoincrement,
                      name text, description text, link text, url text)
                   """)

    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS feed_contents
                          (id integer primary key autoincrement,
                          url text, title text, content text, feed_id number, pub_at timestamp)
                       """)

    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM feeds""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    app.run(debug=True)