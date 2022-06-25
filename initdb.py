import sqlite3

connection = sqlite3.connect("identifier.sqlite")

cur = connection.cursor()
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "pewpewpew"))

connection.commit()
connection.close()