import sqlite3
import File_Utils as fu
from os import path

root = fu.absdir(__file__)
db_root = path.join(root, 'Data', 'db')


def search_link_in_blacklist(data):
    blacklist = sqlite3.connect(path.join(db_root, 'BlacklistDB.db'))
    conn = blacklist
    if '@' in data:  # Its an email address
        data = data.split('@')[-1]
        data1 = '@' + data
        data2 = '*@' + data
        Found = False
        cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data1,))
        if (len(cursor.fetchall()) == 0):
            cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data2,))
            if len(cursor.fetchall()) == 0:
                Found = False
            else:
                Found = True
                cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data2,))
                for row in cursor:
                    return row
        else:
            Found = True
            cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data1,))
            for row in cursor:
                return row

        if (Found == False):
            return None

    else:  # Its either URL or IP address
        cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data,))
        if len(cursor.fetchall()) == 0:
            return None
        else:
            cursor = conn.execute("SELECT DATA, TYPE from Blacklist where DATA=?", (data,))
            for row in cursor:
                return row
    conn.close()


def search_link_in_whitelist(data):
    print 'data ' + data
    whitelist = sqlite3.connect(path.join(db_root, 'WhitelistDB.db'))
    conn = whitelist

    cursor = conn.execute("SELECT DATA, TYPE from Whitelist where DATA=?", (data,))
    if len(cursor.fetchall()) == 0:
        return None
    else:
        cursor = conn.execute("SELECT DATA, TYPE from Whitelist where DATA=?", (data,))
        for row in cursor:
            conn.close()
            return row



if __name__ == '__main__':
    # print search_link_in_whitelist('google.com')
    # print search_link_in_whitelist('youtube.com')
    # print search_link_in_whitelist('Kishor_Kumar1@symantec.com')
    whitelist = sqlite3.connect(path.join(db_root, 'WhitelistDB.db'))
    conn = whitelist

    cursor = conn.execute("SELECT * from Whitelist")
    rows = cursor.fetchall()
    for row in rows:
        print row
