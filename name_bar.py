from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListView,
                               QListWidget, QListWidgetItem, QMainWindow, QMenu,
                               QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
                               QStatusBar, QToolButton, QVBoxLayout, QWidget)


class NameBar(QWidget):
    def __init__(self, name):
        super().__init__()

        self.setObjectName(u"nameBar")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.shelfName = QLabel(self)
        self.shelfName.setObjectName(u"shelfName")
        self.shelfName.setText(name)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shelfName.sizePolicy().hasHeightForWidth())
        self.shelfName.setSizePolicy(sizePolicy)
        self.shelfName.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.shelfName)

        self.shelfToolButton = QToolButton(self)
        self.shelfToolButton.setObjectName(u"shelfToolButton")

        self.horizontalLayout.addWidget(self.shelfToolButton)
