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
from ui.tag_manager_ui import Ui_TagManager

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