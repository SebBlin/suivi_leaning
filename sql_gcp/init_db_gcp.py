import os
import csv
import sqlalchemy
from sqlalchemy import insert, Table, inspect
from sqlalchemy import MetaData
import sqlparse
from manage_db import init_connection_engine

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

db = None
db = db or init_connection_engine()
engine = db
metadata = MetaData(engine)

with db.connect() as con:
    file = open("schema_gcp.sql")
    for req in sqlparse.split(file.read()):
        query = sqlalchemy.sql.text(req)
        con.execute(query, multi=True)

connection = db.connect()
cur = db.connect()

# chargement des UE
file_anme = '../list_ue.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    mytable = Table('ues', metadata, autoload=True, autoload_with=engine)
    for row in reader:
        ins = insert(mytable).values(ue_id=row["id"],ue_name=row["description"])
        connection.execute(ins)
#        cur.execute("INSERT INTO ues (ue_id, ue_name) VALUES (?, ?)", (row["id"], row["description"]))

# Chargement des Colleges 
file_anme = '../list_college.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader2 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    colleges = Table('colleges', metadata, autoload=True, autoload_with=engine)
    for row in reader2:
        ins = insert(colleges).values(college_id=row["id"],college_name=row["college"])
        connection.execute(ins)
        # cur.execute("INSERT INTO colleges (college_id, college_name) VALUES (?, ?)", (row["id"], row["college"]))

# Chargement des items
file_anme = '../items.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader3 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    items = Table('items', metadata, autoload=True, autoload_with=engine)
    for row in reader3:
        ins = insert(items).values(item_id=row["id"], ue_id=row["ue_id"], item_name=row['item'])
        connection.execute(ins)
        # cur.execute("INSERT INTO items (item_id, ue_id, item_name) VALUES (?, ?, ?)", (row["id"], row["ue_id"], row['item']))

# Chargement des liens items / colleges
file_anme = '../items-per-college.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader4 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    item_per_colleges = Table('item_per_colleges', metadata, autoload=True, autoload_with=engine)
    for row in reader4:
        ins = insert(item_per_colleges).values(item_id=row["item_id"], college_id=row["college_id"])
        connection.execute(ins)
        # cur.execute("INSERT INTO item_per_colleges (item_id, college_id) VALUES (?, ?)", (row["item_id"], row["college_id"]))

# import test LS
file_anme = '../ls.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader5 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    lss = Table('lss', metadata, autoload=True, autoload_with=engine)
    for row in reader5:
        ins = insert(lss).values(date=row["date"], college_id=row["college"], item_id=row["item"], serieux=row["serieux"], rang_a=row["rang_a"], rang_b=row["rang_b"])
        connection.execute(ins)
        # cur.execute("INSERT INTO lss (date, college_id, item_id, serieux, rang_a, rang_b) VALUES (?, ?, ?, ?, ?, ?)", (row["date"], row["college"], row["item"], row["serieux"], row["rang_a"], row["rang_b"] ))


connection.close()