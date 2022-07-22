import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from mainwindow import Ui_MainWindow
from settings import Ui_Settings
from detailswindow import Ui_Details
from tagmanager import Ui_TagManager
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
        
        try:
            with open("config.json", 'r') as config_file:
                self.config = json.load(config_file)
        except:
            self.config = {"search_dir" : getcwd()}
            with open("config.json", 'w') as new_config:
                json.dump(self.config, new_config)
        
        
        random10 = self.cur.execute("SELECT uid, name, path FROM films ORDER BY RANDOM() LIMIT 10").fetchall()
        for (uid, name, _) in random10:
            name = (name[:50] + '..') if len(name) > 75 else name
            list_item = QListWidgetItem(QtGui.QIcon(f"{getcwd()}/thumbnails/{uid}.jpg"), name)
            list_item.setData(QtCore.Qt.UserRole, uid)
            self.ui.listWidget.addItem(list_item)
        
        self.ui.listWidget.itemClicked.connect(self.video_clicked)
        self.ui.listWidget.customContextMenuRequested.connect(lambda loc, bar=self.ui.listWidget : self.open_details(loc, bar))

    def video_clicked(self, item):
        uid = item.data(QtCore.Qt.UserRole)
        (path, ) = self.cur.execute("SELECT path FROM films WHERE uid = ?", (uid,)).fetchone()
        subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", f"file:///{path}"])

    def open_details(self, loc, bar):
        item = bar.itemAt(loc)
        self.details = DetailsDialog(self.cur, item.data(QtCore.Qt.UserRole))
        if self.details.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

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
     

        print(f"Database reindexed in {time.time() - start}")
        self.dbcon.commit()

    def show_settings(self):
        self.settings_w = SettingsDialog(self.cur, self.dbcon)
        self.settings_w.set_settings(self.config)
        self.settings_w.show()
        if self.settings_w.exec() == QDialog.Accepted:
            self.config = self.settings_w.get_config()
            print(f"New config! {self.config}")
            with open("config.json", 'w') as config_file:
                json.dump(self.config, config_file)
    
    def closeEvent(self, event):
        print("Safely closing")
        self.dbcon.close()
        event.accept()

class DetailsDialog(QDialog):
    def __init__(self, cur, uid):
        super().__init__()
        #super(QDialogButtonBox, self).__init__()
        self.ui = Ui_Details()
        self.ui.setupUi(self)
        self.cur = cur
        self.uid = uid

        (name,) = self.cur.execute("SELECT name FROM films WHERE uid = ?", (uid,)).fetchone()
        self.ui.titleBrowser.setText(name)

        self.all_tags = self.cur.execute("SELECT tag, tagid FROM tags").fetchall()
        self.selected_tags = [tagid for (tagid,) in self.cur.execute("SELECT tags.tagid FROM tags INNER JOIN tagmap ON tags.tagid = tagmap.tagid AND filmid=?", (uid,)).fetchall()]
        for (tag, tagid) in self.all_tags:
            box = QListWidgetItem(tag)
            box.setFlags(box.flags() | QtCore.Qt.ItemIsUserCheckable)
            box.setData(QtCore.Qt.UserRole, tagid)
            if tagid in self.selected_tags:
                box.setCheckState(QtCore.Qt.Checked)
            else:
                box.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tagsList.addItem(box)

        self.ui.tagsList.itemChanged.connect(self.tag_changed)

        self.show()
    
    def tag_changed(self, item):
        add_tag = item.checkState() == QtCore.Qt.Checked
        tagid = item.data(QtCore.Qt.UserRole)
        if add_tag:
            self.cur.execute("INSERT INTO tagmap (tagid, filmid) VALUES (?, ?)", (tagid, self.uid))
        else:
            self.cur.execute("DELETE FROM tagmap WHERE tagid = ? AND filmid = ?", (tagid, self.uid))




class SettingsDialog(QDialog):
    def __init__(self, cur, dbcon):
        super().__init__()
        #super(QDialogButtonBox, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cur = cur
        self.dbcon = dbcon
        self.ui.browseFiles.clicked.connect(self.browse_files)
        self.ui.tagEditorButton.clicked.connect(self.open_tag_manager)
        self.config = None

    def browse_files(self):
        self.config["search_dir"] = QFileDialog.getExistingDirectory()
    
    def open_tag_manager(self):
        self.tag_manager = TagManager(self.cur)
        if self.tag_manager.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

    def set_settings(self, config):
        self.config = config
    
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
    matches = []
    return [(fn, os.path.join(r, fn))
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
window = MainWindow()
window.show()
app.exec()

