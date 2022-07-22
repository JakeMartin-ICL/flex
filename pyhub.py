import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from mainwindow import Ui_MainWindow
from settings import Ui_Settings
from os import getcwd
import os
import json
import sqlite3
import subprocess
import ffprobe

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
        


    def reindex(self):
        films = findFilms(self.config["search_dir"])
        dbfilms = self.cur.execute("SELECT * from films")
        # Delete moved or removed films 
        for (_, _, path) in dbfilms:
            if path not in [path for (_, path) in films]:
                self.cur.execute("DELETE FROM films WHERE path = ?", path)

        for (name, path) in films:
            if path not in [dbpath for (_, _, dbpath) in dbfilms]:
                duration = get_length(path)
                self.cur.execute("INSERT into films (name, path, duration) VALUES (?, ?, ?)", (name, path, duration))
                subprocess.call(['ffmpeg', '-i', path, ])
        

        print("Database reindexed")
        self.dbcon.commit()

    def show_settings(self):
        self.settings_w = SettingsDialog()
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


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        #super(QDialogButtonBox, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.ui.browseFiles.clicked.connect(self.browse_files)
        self.config = None

    def browse_files(self):
        self.config["search_dir"] = QFileDialog.getExistingDirectory()

    def set_settings(self, config):
        self.config = config
    
    def get_config(self):
        return self.config


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

