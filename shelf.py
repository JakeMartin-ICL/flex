from cgitb import handler
from time import strptime
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QListView, QListWidget,
                               QListWidgetItem, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
                               QVBoxLayout, QWidget)
from os import getcwd
from datetime import datetime

class Shelf(QListWidget):
    def __init__(self, cur, name, shelf_config, direct_query=False):
        super().__init__()
        self.setObjectName(u"listWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy1)
        self.setMinimumSize(QSize(0, 230))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setIconSize(QSize(320, 180))
        self.setProperty("isWrapping", False)
        self.setResizeMode(QListView.Adjust)
        self.setViewMode(QListView.IconMode)

        self.cur = cur
        self.name = name
        self.direct_query = direct_query
        self.reload(shelf_config)
        picture_size = QSize(320, 180) if "picture_size" not in shelf_config else height_to_qsize(shelf_config["picture_size"])
        if "picture_size" in shelf_config:
            self.setMinimumHeight(shelf_config["picture_size"] + 50)
        self.setIconSize(picture_size)

    
    def __len__(self):
        return self.len

    def reload(self, shelf_config):
        self.clear()
        self.filter = shelf_config["filter"]
        self.limit = shelf_config["limit"]
        self.shuffle = shelf_config["shuffle"]
        self.pictures = shelf_config["pictures"]
        self.SQL = SQLify(self.filter, self.limit, self.shuffle, self.pictures) if not self.direct_query else self.filter
        print(self.SQL)


        results = self.cur.execute(self.SQL).fetchall()
        self.len = len(results)
        for (uid, name, path) in results:
            name = (name[:50] + '..') if len(name) > 75 else name
            icon_path = path if self.pictures else f"{getcwd()}/thumbnails/{uid}.jpg"
            list_item = QListWidgetItem(QIcon(icon_path), name)
            list_item.setData(Qt.UserRole, uid)
            self.addItem(list_item)

def height_to_qsize(height):
    return QSize(int(16*(height/9)), height)

comparators = ('=', '<', '>', '!')
markers = ('|', '[', ']', '{', '}')
brackets = ('(', ')')
special_chars = comparators + markers
special_vars = ('added, accessed, size')
time_format = '%d/%m/%Y'
size_pow = {'kb' : 1, 'mb' : 2, 'gb' : 3}

def SQLify(filter, limit, shuffle, pictures=False):
    curr = 0
    negate = False
    target = 'picture' if pictures else 'film'
    query = f'SELECT DISTINCT uid, name, path FROM {target}s LEFT JOIN tagmap ON {target}s.uid = tagmap.{target}id LEFT JOIN tags ON tags.tagid = tagmap.tagid LEFT JOIN varmap ON {target}s.uid = varmap.{target}id LEFT JOIN variables ON varmap.varid = variables.varid WHERE ('
    end_tag_chars = [' ', '<', '>', '=']
    while curr < len(filter):
        char = filter[curr]

        if char == '!':
            negate = True
        elif char in markers:
            if char == '[':
                tag, curr = get_token(filter, curr)
                query += f' tag {"!=" if negate else "="} "{tag}"'
                negate = False
                curr += 1
            elif char == '{':
                var, curr = get_token(filter, curr)
                comparator, curr = get_comparator(filter, curr)
                value, curr = get_token(filter, curr)
                if var in special_vars:
                    value = handle_special_value(var, value)
                    query += f' {var} {comparator} {value}'
                else:
                    query += f' (variable = "{var}" AND value {comparator} {value})'
            elif char == '|':
                path, curr = get_token(filter, curr)
                query += f'path {"NOT " if negate else ""} LIKE "%{path}%"'
                negate = False
        elif char in brackets:
            query += char
        else:
            query += "### PARSE ERROR ###"
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
        value = strptime(value, time_format)
    elif var == 'size':
        size = value[:-2]
        unit = value[-2:].lower()
        value = size * 1024 ** size_pow[unit]
    return value