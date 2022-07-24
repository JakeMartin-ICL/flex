import sqlite3

films = """CREATE TABLE "films" (
	"uid"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL ,
	"path"	TEXT NOT NULL UNIQUE,
	"duration"	INTEGER NOT NULL,
	"thumbfrac"	REAL DEFAULT 0.5,
	PRIMARY KEY("uid" AUTOINCREMENT))"""

pictures = """CREATE TABLE "pictures" (
	"uid"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"path"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("uid" AUTOINCREMENT))"""

tags = """CREATE TABLE "tags" (
	"tagid"	INTEGER NOT NULL UNIQUE,
	"tag"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("tagid" AUTOINCREMENT))"""

variables = """CREATE TABLE "variables" (
	"varid"	INTEGER NOT NULL UNIQUE,
	"min"	INTEGER,
	"max"	INTEGER,
	"variable"	TEXT NOT NULL,
	PRIMARY KEY("varid" AUTOINCREMENT))"""

tagmap = """CREATE TABLE "tagmap" (
	"filmid"	INTEGER,
	"tagid"	INTEGER NOT NULL,
	"pictureid"	INTEGER,
	FOREIGN KEY("tagid") REFERENCES "tags"("tagid") ON DELETE CASCADE,
	FOREIGN KEY("filmid") REFERENCES "films"("uid") ON DELETE CASCADE,
	FOREIGN KEY("pictureid") REFERENCES "pictures"("uid") ON DELETE CASCADE)"""

varmap = """CREATE TABLE "varmap" (
	"varid"	INTEGERN OT NULL,
	"filmid"	INTEGER,
	"pictureid"	INTEGER,
	"value"	INTEGER,
	FOREIGN KEY("pictureid") REFERENCES "pictures"("uid") ON DELETE CASCADE,
	FOREIGN KEY("filmid") REFERENCES "films"("uid") ON DELETE CASCADE,
	FOREIGN KEY("varid") REFERENCES "varmap"("varid") ON DELETE CASCADE)"""


def setup_tables(cur):
    cur.execute(films)
    cur.execute(pictures)
    cur.execute(tags)
    cur.execute(variables)
    cur.execute(tagmap)
    cur.execute(varmap)
