from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
                               QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
                               QHeaderView, QLabel, QListView, QListWidget,
                               QListWidgetItem, QPushButton, QRadioButton, QSizePolicy,
                               QSlider, QTableWidget, QTableWidgetItem, QTextBrowser,
                               QWidget, QCheckBox)
from ui.details_ui import Ui_Details
import subprocess
from os import getcwd
import os


class DetailsDialog(QDialog):
    def __init__(self, cur, uid, item, pictures=False):
        super().__init__()
        #super(QDialogButtonBox, self).__init__()
        self.ui = Ui_Details()
        self.ui.setupUi(self)
        self.cur = cur
        self.uid = uid
        self.list_item = item

        self.target = 'picture' if pictures else 'film'

        if pictures:
            (name, self.path) = self.cur.execute(
                "SELECT name, path FROM pictures WHERE uid = ?", (uid,)).fetchone()
            self.ui.formLayout.removeRow(self.ui.formLayout.rowCount() - 2)
            dirpath = os.path.dirname(self.path)
            self.cwd_uids = self.cur.execute(
                "SELECT uid, path FROM pictures WHERE path LIKE ?", (dirpath+'\%',)).fetchall()
        else:
            (name, thumbfrac, self.path, self.duration) = self.cur.execute(
                "SELECT name, thumbfrac, path, duration FROM films WHERE uid = ?", (uid,)).fetchone()
            self.ui.thumbPosSlider.setValue(int(thumbfrac*100))
            self.ui.rethumbButton.clicked.connect(self.rethumb)
            self.ui.resetThumbSliderButton.clicked.connect(self.reset_thumb)
            dirpath = os.path.dirname(self.path)
            self.cwd_uids = self.cur.execute(
                "SELECT uid, path FROM films WHERE path LIKE ?", (dirpath+'\%',)).fetchall()

        no_subfolders = []
        for (uid, path) in self.cwd_uids:
            if os.path.dirname(path) == dirpath:
                no_subfolders.append(uid)
        self.cwd_uids = no_subfolders

        self.ui.titleBrowser.setText(name)
        self.ui.titleBrowser.setFixedHeight(
            self.ui.titleBrowser.size().height())
        self.ui.varTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.show()

        self.setup_tags()
        self.setup_vars()

    def setup_tags(self):
        self.all_tags = self.cur.execute(
            "SELECT tag, tagid FROM tags").fetchall()
        self.selected_tags = [tagid for (tagid,) in self.cur.execute(
            f"SELECT tags.tagid FROM tags INNER JOIN tagmap ON tags.tagid = tagmap.tagid AND {self.target}id=?", (self.uid,)).fetchall()]
        for (tag, tagid) in self.all_tags:
            box = QListWidgetItem(tag)
            box.setFlags(box.flags() | Qt.ItemIsUserCheckable)
            box.setData(Qt.UserRole, tagid)
            if tagid in self.selected_tags:
                box.setCheckState(Qt.Checked)
            else:
                box.setCheckState(Qt.Unchecked)
            self.ui.tagsList.addItem(box)

        self.ui.tagsList.itemChanged.connect(self.tag_changed)

    def setup_vars(self):
        self.all_vars = self.cur.execute(
            "SELECT variable, varid, min, max FROM variables").fetchall()
        self.selected_vars = dict(self.cur.execute(
            f"SELECT variables.varid, varmap.value FROM variables INNER JOIN varmap ON variables.varid = varmap.varid AND {self.target}id=?", (self.uid,)).fetchall())
        for (var, varid, min, max) in self.all_vars:
            var_item = QTableWidgetItem(var)
            var_item.setData(Qt.UserRole, varid)
            min_item = QTableWidgetItem(str(min))
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(min)
            slider.setMaximum(max)
            slider.setValue(
                self.selected_vars[varid] if varid in self.selected_vars else min)
            max_item = QTableWidgetItem(str(max))
            checkbox = QCheckBox()
            value_item = QTableWidgetItem(
                str(self.selected_vars[varid]) if varid in self.selected_vars else str(min))

            row = self.ui.varTable.rowCount()
            self.ui.varTable.insertRow(row)
            self.ui.varTable.setItem(row, 0, var_item)
            self.ui.varTable.setItem(row, 1, min_item)
            self.ui.varTable.setCellWidget(row, 2, slider)
            self.ui.varTable.setItem(row, 3, max_item)
            self.ui.varTable.setCellWidget(row, 4, checkbox)
            self.ui.varTable.setItem(row, 5, value_item)

            if varid in self.selected_vars:
                checkbox.setCheckState(Qt.Checked)
            else:
                checkbox.setCheckState(Qt.Unchecked)

            checkbox.stateChanged.connect(
                lambda state, varid=varid, row=row: self.var_changed(state, varid, row))
            slider.valueChanged.connect(
                lambda state, varid=varid, row=row: self.slider_changed(state, varid, row))

    def tag_changed(self, item):
        add_tag = item.checkState() == Qt.Checked
        tagid = item.data(Qt.UserRole)
        single = self.ui.folderNoRadioButton.isChecked()
        if add_tag:
            if single:
                self.cur.execute(
                    f"INSERT INTO tagmap (tagid, {self.target}id) VALUES (?, ?)", (tagid, self.uid))
            else:
                for uid in self.cwd_uids:
                    self.cur.execute(
                        f"INSERT INTO tagmap (tagid, {self.target}id) VALUES (?, ?)", (tagid, uid))
        else:
            if not self.ui.folderAllRadioButton.isChecked():
                self.cur.execute(
                    f"DELETE FROM tagmap WHERE tagid = ? AND {self.target}id = ?", (tagid, self.uid))
            else:
                for uid in self.cwd_uids:
                    self.cur.execute(
                        f"DELETE FROM tagmap WHERE tagid = ? AND {self.target}id = ?", (tagid, uid))

    def var_changed(self, state, varid, row):
        enable = state == 2
        if enable:
            value = int(self.ui.varTable.item(row, 5).text())
            if self.ui.folderNoRadioButton.isChecked():
                self.cur.execute(
                    f"INSERT INTO varmap (varid, {self.target}id, value) VALUES (?, ?, ?)", (varid, self.uid, value))
            else:
                for uid in self.cwd_uids:
                    self.cur.execute(
                        f"INSERT INTO varmap (varid, {self.target}id, value) VALUES (?, ?, ?)", (varid, uid, value))
        else:
            if not self.ui.folderAllRadioButton.isChecked():
                self.cur.execute(
                    f"DELETE FROM varmap WHERE varid = ? AND {self.target}id = ?", (varid, self.uid))
            else:
                for uid in self.cwd_uids:
                    self.cur.execute(
                        f"DELETE FROM varmap WHERE varid = ? AND {self.target}id = ?", (varid, uid))

    def slider_changed(self, state, varid, row):
        value_item = QTableWidgetItem(str(state))
        self.ui.varTable.setItem(row, 5, value_item)
        checkbox = self.ui.varTable.cellWidget(row, 4)
        if checkbox.checkState() == Qt.Checked:
            self.cur.execute(
                f"UPDATE varmap SET value = ? WHERE varid = ? AND {self.target}id = ?", (state, varid, self.uid))
        else:
            checkbox.setChecked(True)

    def rethumb(self):
        thumbfrac = self.ui.thumbPosSlider.value()/100
        pos = int(self.duration*thumbfrac)
        thumb_path = f"{getcwd()}\\thumbnails\\{self.uid}.jpg"
        subprocess.call(['ffmpeg', '-ss', str(pos), '-i', self.path,  '-vframes', '1', '-vf', 'scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:-1:-1', '-y', thumb_path],
                        stdout=subprocess.DEVNULL)
        new_icon = QIcon(thumb_path)
        self.list_item.setIcon(new_icon)
        self.cur.execute(
            "UPDATE films SET thumbfrac = ? WHERE uid = ?", (thumbfrac, self.uid))

    def reset_thumb(self):
        self.ui.thumbPosSlider.setValue(50)
