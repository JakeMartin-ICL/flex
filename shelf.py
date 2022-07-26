from os import getcwd
import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QListView, QListWidget, QListWidgetItem,
                               QSizePolicy)

from query_parser import SQLify


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
        picture_size = QSize(320, 180) if "picture_size" not in shelf_config else height_to_qsize(
            shelf_config["picture_size"])
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
        self.SQL = SQLify(self.filter, self.limit, self.shuffle,
                          self.pictures) if not self.direct_query else self.filter
        print(self.SQL)

        results = self.cur.execute(self.SQL).fetchall()
        self.len = len(results)
        for (uid, name, path) in results:
            name = (name[:50] + '..') if len(name) > 75 else name
            icon_path = path if self.pictures else os.path.join(getcwd(), 'thumbnails', f'{uid}.jpg')#f"{getcwd()}/thumbnails/{uid}.jpg"
            list_item = QListWidgetItem(QIcon(icon_path), name)
            list_item.setData(Qt.UserRole, uid)
            self.addItem(list_item)


def height_to_qsize(height):
    return QSize(int(16*(height/9)), height)
