untagged = "SELECT uid, name, path FROM films WHERE NOT EXISTS (SELECT filmid FROM tagmap WHERE tagmap.filmid = films.uid) AND NOT EXISTS (SELECT filmid FROM varmap WHERE varmap.filmid = films.uid) LIMIT 50"
random_pics = "SELECT uid, name, path FROM pictures LIMIT 50 ORDER BY RANDOM()"
