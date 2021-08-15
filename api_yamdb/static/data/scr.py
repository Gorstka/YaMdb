import csv, sqlite3

con = sqlite3.connect("../db.sqlite3")
cur = con.cursor()
cur.execute("CREATE TABLE users (id,username,email,role,bio,first_name,last_name);")

with open("users.csv","r") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i["id"], i["username"],i["email"], i["role"],i["bio"], i["first_name"],i["last_name"]) for i in dr]

cur.executemany("INSERT INTO users (id,username,email,role,bio,first_name,last_name) VALUES (?,?,?,?,?,?,?);", to_db)
con.commit()
con.close()