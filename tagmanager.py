# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tagmanager.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_TagManager(object):
    def setupUi(self, TagManager):
        if not TagManager.objectName():
            TagManager.setObjectName(u"TagManager")
        TagManager.resize(400, 300)
        self.verticalLayout = QVBoxLayout(TagManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(TagManager)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.lineEdit = QLineEdit(TagManager)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaxLength(30)

        self.verticalLayout.addWidget(self.lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(TagManager)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)

        self.removeButton = QPushButton(TagManager)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout.addWidget(self.removeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(TagManager)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TagManager)
        self.buttonBox.accepted.connect(TagManager.accept)
        self.buttonBox.rejected.connect(TagManager.reject)

        QMetaObject.connectSlotsByName(TagManager)
    # setupUi

    def retranslateUi(self, TagManager):
        TagManager.setWindowTitle(QCoreApplication.translate("TagManager", u"Tag Manager", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("TagManager", u"New tag", None))
        self.addButton.setText(QCoreApplication.translate("TagManager", u"Add", None))
#if QT_CONFIG(shortcut)
        self.addButton.setShortcut(QCoreApplication.translate("TagManager", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.removeButton.setText(QCoreApplication.translate("TagManager", u"Remove", None))
#if QT_CONFIG(shortcut)
        self.removeButton.setShortcut(QCoreApplication.translate("TagManager", u"Del", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

