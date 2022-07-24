from time import mktime, strptime

comparators = ('=', '<', '>', '!')
markers = ('|', '[', ']', '{', '}')
special_chars = comparators + markers
special_vars = ('added, accessed, size')
time_format = '%d/%m/%Y'
size_pow = {'kb': 1, 'mb': 2, 'gb': 3}


def SQLify(filter, limit, shuffle, pictures=False):
    curr = 0
    negate = False
    target = 'picture' if pictures else 'film'
    query = f'SELECT DISTINCT uid, name, path FROM {target}s LEFT JOIN tagmap ON {target}s.uid = tagmap.{target}id LEFT JOIN tags ON tags.tagid = tagmap.tagid LEFT JOIN varmap ON {target}s.uid = varmap.{target}id LEFT JOIN variables ON varmap.varid = variables.varid WHERE ('
    while curr < len(filter):
        char = filter[curr]
        if char == '!':
            negate = True
        elif char in markers:
            curr += 1
            if char == '[':
                tag, curr = get_token(filter, curr)
                query += f'tag {"!=" if negate else "="} "{tag}" '
                negate = False
            elif char == '{':
                var, curr = get_token(filter, curr)
                comparator, curr = get_comparator(filter, curr)
                value, curr = get_token(filter, curr)
                if var in special_vars:
                    value = handle_special_value(var, value)
                    query += f' {var} {comparator} {value}'
                else:
                    query += f'(variable = "{var}" AND value {comparator} {value}) '
            elif char == '|':
                path, curr = get_token(filter, curr)
                query += f'path {"NOT " if negate else ""} LIKE "%{path}%" '
                negate = False
        else:
            query += char
        curr += 1

    return query + f'){" ORDER BY RANDOM()" if shuffle else ""} LIMIT {limit} '


def get_comparator(filter, curr):
    comparator = ''
    while True:
        char = filter[curr]
        if char in comparators:
            comparator += filter[curr]
            curr += 1
        elif char.isspace():
            curr += 1
        else:
            return (comparator, curr)


def get_token(filter, curr):
    token = ''
    while True:
        char = filter[curr]
        if char not in special_chars:
            token += char
            curr += 1
        else:
            return (token.strip(), curr)


def handle_special_value(var, value):
    if var == 'added' or var == 'accessed':
        value = int(mktime(strptime(value, time_format)))
    elif var == 'size':
        size = int(value[:-2])
        unit = value[-2:].lower()
        value = size * 1024 ** size_pow[unit]
    return value
