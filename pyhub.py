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
        self.ui.listWidget.customContextMenuRequested.connect(lambda loc, bar=self.ui.listWidget : self.open_details(loc, bar))

        self.shelves = {}
        self.load_shelves()

    def load_shelves(self):
        if self.config["show_untagged"]:
            self.new_direct_query_shelf("Untagged Files", queries.untagged)
        
        for shelf_name in self.config["order"]:
            self.new_shelf(shelf_name)

    def new_direct_query_shelf(self, name, query):
        shelf_config = {"filter": query, "limit": 1000, "shuffle": False}
        shelf = Shelf(self.cur, name, shelf_config, direct_query=True)
        label = QLabel(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, label)
        
        
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, shelf)
        shelf.itemClicked.connect(self.video_clicked)
        shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar))
        self.shelves[name] = (label, shelf)
    
    def new_shelf(self, name):
        shelf_config = self.config["shelves"][name]
        shelf = Shelf(self.cur, name, shelf_config)
        name_bar = NameBar(f"{name} - {len(shelf)}")
        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, name_bar)
        name_bar.shelfToolButton.clicked.connect(lambda test=True, name=name : self.open_edit_shelf_dialog(test, name))

        self.ui.scrollAreaLayout.insertWidget(self.ui.scrollAreaLayout.count() - 2, shelf)
        shelf.itemClicked.connect(self.video_clicked)
        shelf.customContextMenuRequested.connect(lambda loc, bar=shelf : self.open_details(loc, bar))
        self.shelves[name] = (name_bar, shelf)


    def video_clicked(self, item):
        uid = item.data(QtCore.Qt.UserRole)
        (path, ) = self.cur.execute("SELECT path FROM films WHERE uid = ?", (uid,)).fetchone()
        subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", f"file:///{path}"])

    def open_details(self, loc, bar):
        item = bar.itemAt(loc)
        self.details = DetailsDialog(self.cur, item.data(QtCore.Qt.UserRole), item)
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

class DetailsDialog(QDialog):
    def __init__(self, cur, uid, item):
        super().__init__()
        #super(QDialogButtonBox, self).__init__()
        self.ui = Ui_Details()
        self.ui.setupUi(self)
        self.cur = cur
        self.uid = uid
        self.list_item = item

        (name, thumbfrac, self.path, self.duration) = self.cur.execute("SELECT name, thumbfrac, path, duration FROM films WHERE uid = ?", (uid,)).fetchone()
        self.ui.titleBrowser.setText(name)
        self.ui.titleBrowser.setFixedHeight(self.ui.titleBrowser.size().height())
        self.ui.varTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.show()

        self.setup_tags()
        self.setup_vars()

        self.ui.thumbPosSlider.setValue(int(thumbfrac*100))
        self.ui.rethumbButton.clicked.connect(self.rethumb)
        self.ui.resetThumbSliderButton.clicked.connect(self.reset_thumb)

    
    def setup_tags(self):
        self.all_tags = self.cur.execute("SELECT tag, tagid FROM tags").fetchall()
        self.selected_tags = [tagid for (tagid,) in self.cur.execute("SELECT tags.tagid FROM tags INNER JOIN tagmap ON tags.tagid = tagmap.tagid AND filmid=?", (self.uid,)).fetchall()]
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
    
    def setup_vars(self):
        self.all_vars = self.cur.execute("SELECT variable, varid, min, max FROM variables").fetchall()
        self.selected_vars = dict(self.cur.execute("SELECT variables.varid, varmap.value FROM variables INNER JOIN varmap ON variables.varid = varmap.varid AND filmid=?", (self.uid,)).fetchall())
        for (var, varid, min, max) in self.all_vars:
            var_item = QTableWidgetItem(var)
            var_item.setData(QtCore.Qt.UserRole, varid)
            min_item = QTableWidgetItem(str(min))
            slider = QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(min)
            slider.setMaximum(max)
            slider.setValue(self.selected_vars[varid] if varid in self.selected_vars else min)
            max_item = QTableWidgetItem(str(max))
            checkbox = QCheckBox()
            value_item = QTableWidgetItem(str(self.selected_vars[varid]) if varid in self.selected_vars else str(min))

            row = self.ui.varTable.rowCount()
            self.ui.varTable.insertRow(row)
            self.ui.varTable.setItem(row, 0, var_item)
            self.ui.varTable.setItem(row, 1, min_item)
            self.ui.varTable.setCellWidget(row, 2, slider)
            self.ui.varTable.setItem(row, 3, max_item)
            self.ui.varTable.setCellWidget(row, 4, checkbox)
            self.ui.varTable.setItem(row, 5, value_item)
            
            if varid in self.selected_vars:
                checkbox.setCheckState(QtCore.Qt.Checked)
            else:
                checkbox.setCheckState(QtCore.Qt.Unchecked)
            
            checkbox.stateChanged.connect(lambda state, varid=varid, row=row: self.var_changed(state, varid, row))
            slider.valueChanged.connect(lambda state, varid=varid, row=row: self.slider_changed(state, varid, row))

    
    def tag_changed(self, item):
        add_tag = item.checkState() == QtCore.Qt.Checked
        tagid = item.data(QtCore.Qt.UserRole)
        if add_tag:
            self.cur.execute("INSERT INTO tagmap (tagid, filmid) VALUES (?, ?)", (tagid, self.uid))
        else:
            self.cur.execute("DELETE FROM tagmap WHERE tagid = ? AND filmid = ?", (tagid, self.uid))

    def var_changed(self, state, varid, row):
        enable = state == 2
        if enable:
            value = int(self.ui.varTable.item(row, 5).text())
            self.cur.execute("INSERT INTO varmap (varid, filmid, value) VALUES (?, ?, ?)", (varid, self.uid, value))
        else:
            self.cur.execute("DELETE FROM varmap WHERE varid = ? AND filmid = ?", (varid, self.uid))

    def slider_changed(self, state, varid, row):
        value_item = QTableWidgetItem(str(state))
        self.ui.varTable.setItem(row, 5, value_item)
        checkbox = self.ui.varTable.cellWidget(row, 4)
        if checkbox.checkState() == QtCore.Qt.Checked:
            self.cur.execute("UPDATE varmap SET value = ? WHERE varid = ? AND filmid = ?", (state, varid, self.uid))
        else:
            checkbox.setChecked(True)
    
    def rethumb(self):
        thumbfrac = self.ui.thumbPosSlider.value()/100
        pos = int(self.duration*thumbfrac)
        thumb_path = f"{getcwd()}\\thumbnails\\{self.uid}.jpg"
        #os.remove(thumb_path)
        subprocess.call(['ffmpeg', '-ss', str(pos), '-i', self.path,  '-vframes', '1', '-vf', 'scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:-1:-1', '-y', thumb_path],
            stdout=subprocess.DEVNULL)
        new_icon = QIcon(thumb_path)
        self.list_item.setIcon(new_icon)
        self.cur.execute("UPDATE films SET thumbfrac = ? WHERE uid = ?", (thumbfrac, self.uid))
    
    def reset_thumb(self):
        self.ui.thumbPosSlider.setValue(50)


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
#app.setStyleSheet("QLabel{font-size: 18pt;}")
file = QtCore.QFile("./stylesheet.qss")
file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
stream = QtCore.QTextStream(file)
app.setStyleSheet(stream.readAll())
window = MainWindow()
window.show()
app.exec()

