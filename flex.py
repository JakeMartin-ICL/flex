import json
import os
import sqlite3
import subprocess
import sys
import time
from os import getcwd

from pymediainfo import MediaInfo
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *

import queries
from create_db import setup_tables
from edit_shelf import EditShelfDialog
from name_bar import NameBar
from new_shelf import NewShelfDialog
from settings import SettingsDialog
from shelf import Shelf
from ui.main_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dbcon = sqlite3.connect('index.db')
        self.cur = self.dbcon.cursor()
        table = self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='films'").fetchall()
        if len(table) == 0:
            setup_tables(self.cur)

        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionRe_index.triggered.connect(self.reindex)
        reload = self.ui.menubar.addAction("Reload")
        reload.triggered.connect(self.reload)

        self.ui.newShelfButton.clicked.connect(self.open_new_shelf_dialog)

        try:
            with open("config.json", 'r') as config_file:
                self.config = json.load(config_file)
        except:
            self.config = {"search_dir": getcwd(), "vlc": "vlc", "shelves": {}, "order": [],
                           "show_untagged": True}
            with open("config.json", 'w') as new_config:
                json.dump(self.config, new_config)

        self.shelves = {}
        self.load_shelves()

    def load_shelves(self):
        self.new_direct_query_shelf(
            "Random Videos", queries.random_vids, pictures=False)
        self.new_direct_query_shelf(
            "Random Pictures", queries.random_pics, pictures=True)

        if self.config["show_untagged"]:
            self.new_direct_query_shelf("Untagged Files", queries.untagged)

        for shelf_name in self.config["order"]:
            self.new_shelf(shelf_name)

    def new_direct_query_shelf(self, name, query, pictures=False):
        shelf_config = {"filter": query, "limit": 30,
                        "shuffle": False, "pictures": pictures}
        shelf = Shelf(self.cur, self.dbcon, name, shelf_config,
                      self.config["vlc"], direct_query=True)
        label = QLabel(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(
            self.ui.scrollAreaLayout.count() - 2, label)
        self.ui.scrollAreaLayout.insertWidget(
            self.ui.scrollAreaLayout.count() - 2, shelf)
        self.shelves[name] = (label, shelf)

    def new_shelf(self, name):
        shelf_config = self.config["shelves"][name]
        shelf = Shelf(self.cur, self.dbcon, name,
                      shelf_config, self.config["vlc"])
        name_bar = NameBar(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(
            self.ui.scrollAreaLayout.count() - 2, name_bar)
        name_bar.shelfToolButton.clicked.connect(
            lambda test=True, name=name: self.open_edit_shelf_dialog(test, name))
        self.ui.scrollAreaLayout.insertWidget(
            self.ui.scrollAreaLayout.count() - 2, shelf)
        self.shelves[name] = (name_bar, shelf)

    def open_new_shelf_dialog(self):
        self.new_shelf_dialog = NewShelfDialog(self.cur, self.config)
        if self.new_shelf_dialog.exec() == QDialog.Accepted:
            self.config = self.new_shelf_dialog.get_config()
            self.save_config()
            name = list(self.config["shelves"].keys())[-1]
            self.new_shelf(name)

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
        local_paths = [path for (_, path) in films]
        dbpaths = [path for (path, ) in self.cur.execute(
            "SELECT path from films").fetchall()]
        # Delete moved or removed films
        for dbpath in dbpaths:
            if dbpath not in local_paths:
                self.cur.execute("DELETE FROM films WHERE path = ?", (dbpath,))
                print(f"Removed: {dbpath}")

        for (name, path) in films:
            if path not in dbpaths:
                info = MediaInfo.parse(path)
                try:
                    duration = int(float(info.video_tracks[0].duration)) // 1000
                except:
                    print(f"File {name} appears to have no video track - skipping.")
                added = int(time.time())
                accessed = int(os.path.getatime(path))
                size = os.path.getsize(path)
                self.cur.execute("INSERT into films (name, path, duration, added, accessed, size) VALUES (?, ?, ?, ?, ?, ?)", (
                    name, path, duration, added, accessed, size))
                id = self.cur.lastrowid
                thumb_path = os.path.join(getcwd(), 'thumbnails', f"{id}.jpg")
                subprocess.call(['ffmpeg', '-ss', str(duration//2), '-i', path,  '-vframes', '1', '-vf', 'scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:-1:-1', '-y', thumb_path],
                                stdout=subprocess.DEVNULL)
                print(f"Added: {path}")

        pictures = findPictures(self.config["search_dir"])
        local_paths = [path for (_, path) in pictures]
        dbpaths = [path for (path, ) in self.cur.execute(
            "SELECT path FROM pictures").fetchall()]
        # Delete moved or removed films
        for dbpath in dbpaths:
            if dbpath not in local_paths:
                self.cur.execute(
                    "DELETE FROM pictures WHERE path = ?", (dbpath,))
                print(f"Removed: {dbpath}")

        for (name, path) in pictures:
            if path not in dbpaths:
                added = int(time.time())
                accessed = int(os.path.getatime(path))
                size = os.path.getsize(path)
                self.cur.execute("INSERT into pictures (name, path, added, accessed, size) VALUES (?, ?, ?, ?, ?)", (
                    name, path, added, accessed, size))
                id - self.cur.lastrowid
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


def findFilms(folder):
    extensions = ('.avi', '.mkv', '.wmv', '.mp4',
                  '.mpg', '.mpeg', '.mov', '.m4v')
    return findFilesWithExtension(folder, extensions)


def findPictures(folder):
    extensions = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief',
                  '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')
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
file = QtCore.QFile("./ui/stylesheets/stylesheet.qss")
file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
stream = QtCore.QTextStream(file)
app.setStyleSheet(stream.readAll())
window = MainWindow()
window.show()
app.exec()
