import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QIcon
from mainwindow import Ui_MainWindow
from new_shelf import NewShelfDialog
from edit_shelf import EditShelfDialog
from settings import Ui_Settings
from detailswindow import Ui_Details
from tagmanager import Ui_TagManager
from variable_manager import VariableManagerDialog
from details import DetailsDialog
from shelf import Shelf
from name_bar import NameBar
import queries
from os import getcwd
import os
import json
import sqlite3
import subprocess
from pymediainfo import MediaInfo
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dbcon = sqlite3.connect('index.db')
        self.cur = self.dbcon.cursor()

        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionRe_index.triggered.connect(self.reindex)
        reload = self.ui.menubar.addAction("Reload")
        reload.triggered.connect(self.reload)

        self.ui.newShelfButton.clicked.connect(self.open_new_shelf_dialog)
        
        try:
            with open("config.json", 'r') as config_file:
                self.config = json.load(config_file)
        except:
            self.config = {"search_dir" : getcwd(), "shelves" : {}, "show_untagged" : True}
            with open("config.json", 'w') as new_config:
                json.dump(self.config, new_config)
        
        
        random10 = self.cur.execute("SELECT uid, name, path FROM films ORDER BY RANDOM() LIMIT 10").fetchall()
        for (uid, name, _) in random10:
            name = (name[:50] + '..') if len(name) > 75 else name
            list_item = QListWidgetItem(QtGui.QIcon(f"{getcwd()}/thumbnails/{uid}.jpg"), name)
            list_item.setData(QtCore.Qt.UserRole, uid)
            self.ui.listWidget.addItem(list_item)
        
        self.ui.listWidget.itemClicked.connect(self.video_clicked)
        self.ui.listWidget.customContextMenuRequested.connect(lambda loc, bar=self.ui.listWidget : self.open_details(loc, bar, False))

        self.shelves = {}
        self.load_shelves()

    def load_shelves(self):
        self.new_direct_query_shelf("Random Pictures", queries.random_pics, pictures=True)

        if self.config["show_untagged"]:
            self.new_direct_query_shelf("Untagged Files", queries.untagged)
        
        for shelf_name in self.config["order"]:
            self.new_shelf(shelf_name, self.config["shelves"][shelf_name]["pictures"])

    def new_direct_query_shelf(self, name, query, pictures=False):
        shelf_config = {"filter": query, "limit": 1000, "shuffle": False, "pictures" : pictures}
        shelf = Shelf(self.cur, name, shelf_config, direct_query=True)
        label = QLabel(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, label)
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, shelf)

        if pictures:
            shelf.itemClicked.connect(self.picture_clicked)
            shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar, True))
        else:
            shelf.itemClicked.connect(self.video_clicked)
            shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar, False))
        self.shelves[name] = (label, shelf)
    
    def new_shelf(self, name, picture=False):
        shelf_config = self.config["shelves"][name]
        shelf = Shelf(self.cur, name, shelf_config)
        name_bar = NameBar(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, name_bar)
        name_bar.shelfToolButton.clicked.connect(lambda test=True, name=name : self.open_edit_shelf_dialog(test, name))
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, shelf)

        if picture:
            shelf.itemClicked.connect(self.picture_clicked)
            shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar, True))
        else:
            shelf.itemClicked.connect(self.video_clicked)
            shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar, False))
        self.shelves[name] = (name_bar, shelf)


    def video_clicked(self, item):
        uid = item.data(QtCore.Qt.UserRole)
        (path, ) = self.cur.execute("SELECT path FROM films WHERE uid = ?", (uid,)).fetchone()
        subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", f"file:///{path}"])
    
    def picture_clicked(self, item):
        uid = item.data(QtCore.Qt.UserRole)
        (path, ) = self.cur.execute("SELECT path FROM pictures WHERE uid = ?", (uid,)).fetchone()
        if sys.platform.startswith('linux'):
            subprocess.call(['xdg-open', path])

        elif sys.platform.startswith('darwin'):
            subprocess.call(['open', path])

        elif sys.platform.startswith('win'):
            subprocess.call(['explorer', os.path.abspath(path)])

    def open_details(self, loc, bar, picture):
        item = bar.itemAt(loc)
        self.details = DetailsDialog(self.cur, item.data(QtCore.Qt.UserRole), item, picture)
        if self.details.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

    def open_new_shelf_dialog(self):
        self.new_shelf_dialog = NewShelfDialog(self.cur, self.config)
        if self.new_shelf_dialog.exec() == QDialog.Accepted:
            self.config = self.new_shelf_dialog.get_config()
            self.save_config()
            name = list(self.config["shelves"].keys())[-1]
            self.new_shelf(name, self.config["shelves"][name]["pictures"])
    
    def open_edit_shelf_dialog(self, test, name):
        print(f"T: {test}. n: {name}")
        self.edit_shelf_dialog = EditShelfDialog(self.cur, self.config, name)
        deleted = self.edit_shelf_dialog.exec() == QDialog.Rejected
        self.config = self.edit_shelf_dialog.config
        self.save_config()
        (name_bar, shelf) = self.shelves[name]
        if deleted:
            self.ui.scrollAreaLayout.removeWidget(name_bar)
            name_bar.deleteLater()
            self.ui.scrollAreaLayout.removeWidget(shelf)
            shelf.deleteLater()
            del self.shelves[name]
        else:
            self.shelves[name][1].reload(self.config["shelves"][name])
    
    def reload(self):
        for (name_bar, shelf) in self.shelves.values():
            self.ui.scrollAreaLayout.removeWidget(name_bar)
            name_bar.deleteLater()
            self.ui.scrollAreaLayout.removeWidget(shelf)
            shelf.deleteLater()
        self.shelves = {}
        self.load_shelves()

    def reindex(self):
        start = time.time()
        films = findFilms(self.config["search_dir"])
        dbpaths = [path for (path, ) in self.cur.execute("SELECT path from films").fetchall()]
        # Delete moved or removed films 
        for dbpath in dbpaths:
            if dbpath not in [path for (_, path) in films]:
                self.cur.execute("DELETE FROM films WHERE path = ?", (dbpath,))
                print(f"Removed: {dbpath}")

        for (name, path) in films:
            if path not in dbpaths:
                info = MediaInfo.parse(path)
                duration = int(float(info.video_tracks[0].duration)) // 1000
                id = self.cur.execute("INSERT into films (name, path, duration) VALUES (?, ?, ?) RETURNING uid", (name, path, duration)).fetchone()[0]
                thumb_path = f"{getcwd()}\\thumbnails\\{id}.jpg"
                subprocess.call(['ffmpeg', '-ss', str(duration//2), '-i', path,  '-vframes', '1', '-vf', 'scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:-1:-1', '-y', thumb_path],
                    stdout=subprocess.DEVNULL)
                print(f"Added: {path}")

        pictures = findPictures(self.config["search_dir"])
        dbpaths = [path for (path, ) in self.cur.execute("SELECT path FROM pictures").fetchall()]
        # Delete moved or removed films 
        for dbpath in dbpaths:
            if dbpath not in [path for (_, path) in pictures]:
                self.cur.execute("DELETE FROM pictures WHERE path = ?", (dbpath,))
                print(f"Removed: {dbpath}")

        for (name, path) in pictures:
            if path not in dbpaths:
                id = self.cur.execute("INSERT into pictures (name, path) VALUES (?, ?) RETURNING uid", (name, path)).fetchone()[0]
                print(f"Added: {path}")
     

        print(f"Database reindexed in {time.time() - start}")
        self.dbcon.commit()

    def show_settings(self):
        self.settings_w = SettingsDialog(self.cur, self.dbcon, self.config)
        self.settings_w.show()
        if self.settings_w.exec() == QDialog.Accepted:
            self.config = self.settings_w.get_config()
            self.save_config()

    
    def save_config(self):
        print(f"New config! {self.config}")
        with open("config.json", 'w') as config_file:
            json.dump(self.config, config_file)
    
    def closeEvent(self, event):
        print("Safely closing")
        self.dbcon.close()
        event.accept()


class SettingsDialog(QDialog):
    def __init__(self, cur, dbcon, config):
        super().__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cur = cur
        self.dbcon = dbcon
        self.ui.browseFiles.clicked.connect(self.browse_files)
        self.ui.tagEditorButton.clicked.connect(self.open_tag_manager)
        self.ui.variableManagerButton.clicked.connect(self.open_var_manager)
        self.ui.showUntaggedCheckBox.setChecked(config["show_untagged"])
        self.ui.showUntaggedCheckBox.stateChanged.connect(self.show_untagged)

        for name, shelf_config in config["shelves"].items():
            item = QListWidgetItem(name)
            self.ui.orderList.addItem(item)
        self.ui.orderList.model().rowsMoved.connect(self.update_order)

        self.config = config

    def browse_files(self):
        self.config["search_dir"] = QFileDialog.getExistingDirectory()
    
    def open_tag_manager(self):
        self.tag_manager = TagManager(self.cur)
        if self.tag_manager.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()
    
    def open_var_manager(self):
        self.tag_manager = VariableManagerDialog(self.cur)
        if self.tag_manager.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

    def show_untagged(self, state):
        show = state == 2
        self.config["show_untagged"] = show

    def update_order(self):
        new_order = []
        for i in range(self.ui.orderList.count()):
            name = self.ui.orderList.item(i).text()
            new_order.append(name)
        self.config["order"] = new_order

    def get_config(self):
        return self.config

class TagManager(QDialog):
    def __init__(self, cur):
        super().__init__()
        self.ui = Ui_TagManager()
        self.ui.setupUi(self)
        self.cur = cur

        self.load_tags()

        self.ui.addButton.clicked.connect(self.add_tag)
        self.ui.removeButton.clicked.connect(self.remove_tag)
        self.show()
    
    def load_tags(self):
        self.tags = [tag for (tag, ) in self.cur.execute("SELECT tag from tags").fetchall()]
        self.ui.listWidget.addItems(self.tags)

    def add_tag(self):
        new_tag = self.ui.lineEdit.text()
        self.cur.execute("INSERT INTO tags (tag) VALUES (?)", (new_tag,))
        self.ui.listWidget.addItem(new_tag)
        self.ui.lineEdit.clear()

    def remove_tag(self):
        tags = self.ui.listWidget.selectedItems()
        for tag in tags:
            self.cur.execute("DELETE FROM tags WHERE tag = ?", (tag.text(),))
        self.ui.listWidget.clear()
        self.load_tags()


def findFilms(folder):
    extensions = ('.avi', '.mkv', '.wmv', '.mp4', '.mpg', '.mpeg', '.mov', '.m4v')
    return findFilesWithExtension(folder, extensions)

def findPictures(folder):
    extensions = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')
    return findFilesWithExtension(folder, extensions)

def findFilesWithExtension(folder, extensions):
    return [(fn, os.path.abspath(os.path.join(r, fn)))
        for r, ds, fs in os.walk(folder) 
        for fn in fs if fn.lower().endswith(extensions)]

def get_length(path):
    result = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return int(float(result.stdout))

app = QtWidgets.QApplication(sys.argv)
#app.setStyleSheet("QLabel{font-size: 18pt;}")
file = QtCore.QFile("./stylesheet.qss")
file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
stream = QtCore.QTextStream(file)
app.setStyleSheet(stream.readAll())
window = MainWindow()
window.show()
app.exec()

