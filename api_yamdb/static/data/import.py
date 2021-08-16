import csv, sqlite3

con = sqlite3.connect("/Users/work/Documents/Learn Python/api_yamdb/api_yamdb/db.sqlite3")
cur = con.cursor()

with open("users.csv","r") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i["id"], i["username"],i["password"],i["is_superuser"],i["email"],i["role"],i["bio"],i["first_name"],i["last_name"]) for i in dr]

cur.executemany("INSERT INTO users_user (id,username,password,is_superuser,email,role,bio,first_name,last_name) VALUES (?,?,?,?,?,?,?,?,?);", to_db)
con.commit()
con.close()