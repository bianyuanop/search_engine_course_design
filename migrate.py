import os
import sqlite3

os.makedirs('storage')
with open('./schema.sql', 'r') as f:
    sql = f.read()
    con = sqlite3.connect('data.db')
    con.executescript(sql)
    con.close()

    print("Done")
