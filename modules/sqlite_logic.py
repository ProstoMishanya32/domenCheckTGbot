import sqlite3 as sq

def start():
    global base, cur
    base = sq.connect("databases/db.db", check_same_thread=False)
    cur = base.cursor()

    if base:
        print(f"База данных подключена\n{'*' * 50}")
    base.execute("""
    CREATE TABLE IF NOT EXISTS
    url(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    status INT,
    steam INT,
    google INT)""")
    base.commit()

def add_url(url):
    result = cur.execute("SELECT id FROM url WHERE url = ?", (url,)).fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO url(url) VALUES (?)", (url,) )
        base.commit()

def update_steam(url, result):
    cur.execute("UPDATE url  SET steam = ? WHERE url = ?", (result, url))
    base.commit()

def update_google(url, result):
    cur.execute("UPDATE url  SET google = ? WHERE url = ?", (result, url))
    base.commit()

def update_notactive(url):
    result = cur.execute("SELECT id FROM url WHERE url = ?", (url,)).fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO url(url, status) VALUES (?, ?)", (url, 1) )
        base.commit()
    else:
        cur.execute("UPDATE url  SET (status) = ? WHERE url = ?", (1, url))
        base.commit()

def get_data(url):
    status = cur.execute("SELECT status FROM url WHERE url = ?", (url,)).fetchall()
    steam  = cur.execute("SELECT steam FROM url WHERE url = ?", (url,)).fetchall()
    google = cur.execute("SELECT google FROM url WHERE url = ?", (url,)).fetchall()
    return status[0], steam[0], google[0]

def get_domens():
    status = cur.execute("SELECT id, url FROM url").fetchall()
    return status

def get_url():
    url = cur.execute("SELECT url FROM url").fetchall()
    return url

def delete_domen(id):
    result = cur.execute("SELECT url FROM url WHERE id = ?", (id,)).fetchall()
    if len(result) == 0:
        return False
    else:
        cur.execute("DELETE FROM url WHERE id = ?", (id,))
        base.commit()
        return True
