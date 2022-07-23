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

    
    def __len__(self):
        return self.len

    def reload(self, shelf_config):
        self.clear()
        self.filter = shelf_config["filter"]
        self.limit = shelf_config["limit"]
        self.shuffle = shelf_config["shuffle"]
        self.SQL = SQLify(self.filter, self.limit, self.shuffle) if not self.direct_query else self.filter
        print(self.SQL)


        results = self.cur.execute(self.SQL).fetchall()
        self.len = len(results)
        for (uid, name) in results:
            name = (name[:50] + '..') if len(name) > 75 else name
            list_item = QListWidgetItem(
                QIcon(f"{getcwd()}/thumbnails/{uid}.jpg"), name)
            list_item.setData(Qt.UserRole, uid)
            self.addItem(list_item)



def SQLify(filter, limit, shuffle):
    curr = 0
    negate = False
    query = 'SELECT DISTINCT uid, name FROM films LEFT JOIN tagmap ON films.uid = tagmap.filmid LEFT JOIN tags ON tags.tagid = tagmap.tagid LEFT JOIN varmap ON films.uid = varmap.filmid LEFT JOIN variables ON varmap.varid = variables.varid WHERE ('
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
        else:
            query += char
        curr += 1
    return query + f'){" ORDER BY RANDOM()" if shuffle else ""} LIMIT {limit} '
