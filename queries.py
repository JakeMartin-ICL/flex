untagged = "SELECT uid, name FROM films WHERE uid NOT IN (SELECT filmid FROM tagmap) AND uid NOT IN (SELECT filmid FROM varmap)"