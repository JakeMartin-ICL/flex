untagged = "SELECT uid, name, path FROM films WHERE NOT EXISTS (SELECT filmid FROM tagmap WHERE tagmap.filmid = films.uid) AND NOT EXISTS (SELECT filmid FROM varmap WHERE varmap.filmid = films.uid) ORDER BY RANDOM() LIMIT 50"
random_vids = "SELECT uid, name, path FROM films ORDER BY RANDOM() LIMIT 50"
random_pics = "SELECT uid, name, path FROM pictures ORDER BY RANDOM() LIMIT 50"
