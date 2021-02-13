import sqlite3
import csv

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# chargement des UE
file_anme = 'list_ue.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        cur.execute("INSERT INTO ues (ue_id, ue_name) VALUES (?, ?)", (row["id"], row["description"]))

# Chargement des Colleges 
file_anme = 'list_college.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader2 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader2:
        cur.execute("INSERT INTO colleges (college_id, college_name) VALUES (?, ?)", (row["id"], row["college"]))

# Chargement des items
file_anme = 'items.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader3 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader3:
        cur.execute("INSERT INTO items (item_id, ue_id, item_name) VALUES (?, ?, ?)", (row["id"], row["ue_id"], row['item']))

# Chargement des liens items / colleges
file_anme = 'items-per-college.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader4 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader4:
        cur.execute("INSERT INTO item_per_colleges (item_id, college_id) VALUES (?, ?)", (row["item_id"], row["college_id"]))

# import test LS
file_anme = 'ls.csv'
with open(file_anme, newline='', encoding="utf-8-sig") as csvfile:
    reader4 = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader4:
        cur.execute("INSERT INTO lss (date, college_id, item_id, serieux, rang_a, rang_b) VALUES (?, ?, ?, ?, ?, ?)", (row["date"], row["college"], row["item"], row["serieux"], row["rang_a"], row["rang_b"] ))


connection.commit()
connection.close()