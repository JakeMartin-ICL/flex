import os
import subprocess
import sys
from os import getcwd

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QListView, QListWidget,
                               QListWidgetItem, QSizePolicy)

from details import DetailsDialog
from query_parser import SQLify


class Shelf(QListWidget):
    def __init__(self, cur, con, name, shelf_config, vlc, direct_query=False):
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
        self.con = con
        self.name = name
        self.vlc = vlc
        self.direct_query = direct_query
        self.middle_clicked = False
        self.reload(shelf_config)
        picture_size = QSize(320, 180) if "picture_size" not in shelf_config else height_to_qsize(
            shelf_config["picture_size"])
        if "picture_size" in shelf_config:
            self.setMinimumHeight(shelf_config["picture_size"] + 50)
        self.setIconSize(picture_size)

        self.itemPressed.connect(self.item_clicked)

    def __len__(self):
        return self.len

    def mousePressEvent(self, event):
        self.click_type = event.button()
        return QListWidget.mousePressEvent(self, event)

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
            disp_name = os.path.join(
                os.path.basename(os.path.dirname(path)), name)
            disp_name = ('..' + disp_name[-48:]
                         ) if len(disp_name) > 50 else disp_name
            icon_path = path if self.pictures else os.path.join(
                getcwd(), 'thumbnails', f'{uid}.jpg')  # f"{getcwd()}/thumbnails/{uid}.jpg"
            list_item = QListWidgetItem(QIcon(icon_path), disp_name)
            list_item.setData(Qt.UserRole, uid)
            self.addItem(list_item)

    def item_clicked(self, item):
        uid = item.data(Qt.UserRole)
        target = 'pictures' if self.pictures else 'films'
        (path, ) = self.cur.execute(
            f"SELECT path FROM {target} WHERE uid = ?", (uid,)).fetchone()
        if self.click_type == Qt.MiddleButton:
            open_location(path)
        elif self.click_type == Qt.RightButton:
            self.open_details(item)
        else:
            if self.pictures:
                open_picture(path)
            else:
                open_video(path, self.vlc)

    def open_details(self, item):
        self.details = DetailsDialog(self.cur, item, self.pictures)
        if self.details.exec() == QDialog.Accepted:
            self.con.commit()
        else:
            self.con.rollback()


def open_picture(path):
    if sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', path])

    elif sys.platform.startswith('darwin'):
        subprocess.call(['open', path])

    elif sys.platform.startswith('win'):
        subprocess.call(['explorer', os.path.abspath(path)])


def open_video(path, vlc):
    subprocess.Popen([vlc, f"file:///{path}"])


def open_location(path):
    path = os.path.dirname(path)
    if sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', path])

    elif sys.platform.startswith('darwin'):
        subprocess.call(['open', path])

    elif sys.platform.startswith('win'):
        subprocess.call(['explorer', os.path.abspath(path)])


def height_to_qsize(height):
    return QSize(int(16*(height/9)), height)
