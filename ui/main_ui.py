# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1697, 842)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionRe_index = QAction(MainWindow)
        self.actionRe_index.setObjectName(u"actionRe_index")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1679, 783))
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.nameBar = QWidget(self.scrollAreaWidgetContents_2)
        self.nameBar.setObjectName(u"nameBar")
        self.horizontalLayout = QHBoxLayout(self.nameBar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.shelfName = QLabel(self.nameBar)
        self.shelfName.setObjectName(u"shelfName")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shelfName.sizePolicy().hasHeightForWidth())
        self.shelfName.setSizePolicy(sizePolicy)
        self.shelfName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.shelfName)

        self.shelfToolButton = QToolButton(self.nameBar)
        self.shelfToolButton.setObjectName(u"shelfToolButton")

        self.horizontalLayout.addWidget(self.shelfToolButton)


        self.scrollAreaLayout.addWidget(self.nameBar)

        self.listWidget = QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.listWidget.setMinimumSize(QSize(0, 230))
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.setIconSize(QSize(320, 180))
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QListView.Adjust)
        self.listWidget.setViewMode(QListView.IconMode)

        self.scrollAreaLayout.addWidget(self.listWidget)

        self.newShelfButton = QPushButton(self.scrollAreaWidgetContents_2)
        self.newShelfButton.setObjectName(u"newShelfButton")

        self.scrollAreaLayout.addWidget(self.newShelfButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scrollAreaLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1697, 21))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionRe_index)
        self.menuMenu.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionRe_index.setText(QCoreApplication.translate("MainWindow", u"Re-index", None))
        self.shelfName.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.shelfToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.newShelfButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi
