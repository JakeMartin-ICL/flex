# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(665, 378)
        self.formLayout = QFormLayout(Settings)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Settings)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(Settings)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.tagEditorButton = QPushButton(Settings)
        self.tagEditorButton.setObjectName(u"tagEditorButton")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.tagEditorButton)

        self.label_3 = QLabel(Settings)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.variableManagerButton = QPushButton(Settings)
        self.variableManagerButton.setObjectName(u"variableManagerButton")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.variableManagerButton)

        self.label_4 = QLabel(Settings)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.showUntaggedCheckBox = QCheckBox(Settings)
        self.showUntaggedCheckBox.setObjectName(u"showUntaggedCheckBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.showUntaggedCheckBox)

        self.label_5 = QLabel(Settings)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_5)

        self.orderList = QListWidget(Settings)
        self.orderList.setObjectName(u"orderList")
        self.orderList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.orderList.setDragEnabled(True)
        self.orderList.setDragDropMode(QAbstractItemView.InternalMove)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.orderList)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.buttonBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pathEdit = QLineEdit(Settings)
        self.pathEdit.setObjectName(u"pathEdit")

        self.horizontalLayout.addWidget(self.pathEdit)

        self.browseFiles = QPushButton(Settings)
        self.browseFiles.setObjectName(u"browseFiles")

        self.horizontalLayout.addWidget(self.browseFiles)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_6 = QLabel(Settings)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_6)

        self.vlcEdit = QLineEdit(Settings)
        self.vlcEdit.setObjectName(u"vlcEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.vlcEdit)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Search directory:", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"Manage tags:", None))
        self.tagEditorButton.setText(QCoreApplication.translate("Settings", u"Tag editor", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"Manage variables:", None))
        self.variableManagerButton.setText(QCoreApplication.translate("Settings", u"Variable manager", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"Untagged shelf:", None))
        self.showUntaggedCheckBox.setText(QCoreApplication.translate("Settings", u"Show", None))
        self.label_5.setText(QCoreApplication.translate("Settings", u"Reorder shelves:", None))
        self.browseFiles.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.label_6.setText(QCoreApplication.translate("Settings", u"Video player:", None))
    # retranslateUi

