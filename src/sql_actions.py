import sqlite3


def get_column_names():
    conn = sqlite3.connect('Matches.sqlite')
    cur = conn.cursor()

    cur.execute("SELECT * FROM matches")
    names = list(map(lambda x: x[0], cur.description))

    conn.commit()
    conn.close()

    return names


def get_all_data():
    conn = sqlite3.connect('Matches.sqlite')
    cur = conn.cursor()

    cur.execute("SELECT * FROM matches")

    data = cur.fetchall()

    conn.commit()
    conn.close()

    return data


def add_match_data(home, away, date, time, matched):
    conn = sqlite3.connect('Matches.sqlite')
    cur = conn.cursor()

    cur.execute("INSERT INTO matches (Home, Away, Date, Time, Matched) VALUES ('%s', '%s', '%s', '%s', %s)" % (home, away, date, time, matched))

    conn.commit()
    conn.close()

    return cur.lastrowid


def add_odds(match_id, odds, minute):
    conn = sqlite3.connect('Matches.sqlite')
    cur = conn.cursor()

    if cur.execute("SELECT * FROM matches WHERE Minute_%s IS NULL" % minute):
        cur.execute("UPDATE matches SET Minute_%s = %s WHERE Id = %s" % (minute, odds, match_id))

        conn.commit()
        conn.close()

        return True

    conn.commit()
    conn.close()

    return False



def create_new_table():
    conn = sqlite3.connect('Matches.sqlite')
    cur = conn.cursor()

    # cur.execute('DROP table matches;') # uncomment only if you're sure you want to delete the table
    cur.execute('CREATE TABLE matches ('
                'Id INTEGER PRIMARY KEY,'
                'Home TEXT,'
                'Away TEXT,'
                'Date TEXT,'
                'Time TEXT,'
                'Matched REAL'
                ')')

    for i in range(180, -1, -1):
        cur.execute("ALTER TABLE matches ADD COLUMN Minute_%d REAL" % i)

    conn.commit()
    conn.close()
