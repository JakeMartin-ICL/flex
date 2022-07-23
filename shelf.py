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
        elif char == '[':
            tag = ''
            curr += 1
            while True:
                char = filter[curr]
                if char == ']':
                    break
                tag += char
                curr += 1
            query += f'tag {"!=" if negate else "="} "{tag}"'
            negate = False
        elif char == '{':
            var = ''
            curr += 1
            while True:
                char = filter[curr]
                if char == "=" or char == "<" or char == "=" or char == "=" or char == "!" or char == " ":
                    break
                var += char
                curr += 1
            query += f'(variable = "{var}" AND value'
            while True:
                char = filter[curr]
                if char == '}':
                    break
                query += char
                curr += 1
            query += ')'
        elif char == '|':
            path = ''
            curr += 1
            while True:
                char = filter[curr]
                if char == '|':
                    break
                path += char
                curr += 1
            query += f'path {"NOT " if negate else ""} LIKE "%{path}%"'
            negate = False
        else:
            query += char
        curr += 1
    return query + f'){" ORDER BY RANDOM()" if shuffle else ""} LIMIT {limit} '
