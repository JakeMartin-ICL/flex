import sqlite3

def setup_tables(cur):
    cur.execute("""CREATE TABLE "films" (
	"uid"	INTEGER UNIQUE,
	"name"	TEXT,
	"path"	TEXT UNIQUE,
	"duration"	INTEGER,
	"thumbfrac"	REAL DEFAULT 0.5,
	PRIMARY KEY("uid" AUTOINCREMENT)))""")
    cur.execute("""CREATE TABLE "pictures" (
	"uid"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"path"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("uid" AUTOINCREMENT))""")
    cur.execute("""CREATE TABLE "tags" (
	"tagid"	INTEGER UNIQUE,
	"tag"	TEXT UNIQUE,
	PRIMARY KEY("tagid" AUTOINCREMENT))""")
    cur.execute("""CREATE TABLE "variables" (
	"varid"	INTEGER UNIQUE,
	"min"	INTEGER,
	"max"	INTEGER,
	"variable"	TEXT,
	PRIMARY KEY("varid" AUTOINCREMENT))""")
    cur.execute("""CREATE TABLE "tagmap" (
	"filmid"	INTEGER,
	"tagid"	INTEGER,
	"pictureid"	INTEGER,
	FOREIGN KEY("tagid") REFERENCES "tags"("tagid") ON DELETE CASCADE,
	FOREIGN KEY("filmid") REFERENCES "films"("uid") ON DELETE CASCADE,
	FOREIGN KEY("pictureid") REFERENCES "pictures"("uid") ON DELETE CASCADE)""")
    cur.execute("""CREATE TABLE "varmap" (
	"varid"	INTEGER,
	"filmid"	INTEGER,
	"pictureid"	INTEGER,
	"value"	INTEGER,
	FOREIGN KEY("pictureid") REFERENCES "pictures"("uid") ON DELETE CASCADE,
	FOREIGN KEY("filmid") REFERENCES "films"("uid") ON DELETE CASCADE,
	FOREIGN KEY("varid") REFERENCES "varmap"("varid") ON DELETE CASCADE)""")
