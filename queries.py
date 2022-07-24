untagged = "SELECT uid, name, path FROM films WHERE NOT EXISTS (SELECT filmid FROM tagmap WHERE tagmap.filmid = films.uid) AND NOT EXISTS (SELECT filmid FROM varmap WHERE varmap.filmid = films.uid)"
random_pics = "SELECT uid, name, path FROM pictures"
