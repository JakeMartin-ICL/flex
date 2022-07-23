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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(665, 378)
        self.formLayout = QFormLayout(Settings)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Settings)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.browseFiles = QPushButton(Settings)
        self.browseFiles.setObjectName(u"browseFiles")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.browseFiles)

        self.label_2 = QLabel(Settings)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.tagEditorButton = QPushButton(Settings)
        self.tagEditorButton.setObjectName(u"tagEditorButton")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.tagEditorButton)

        self.label_3 = QLabel(Settings)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.variableManagerButton = QPushButton(Settings)
        self.variableManagerButton.setObjectName(u"variableManagerButton")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.variableManagerButton)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.buttonBox)

        self.showUntaggedCheckBox = QCheckBox(Settings)
        self.showUntaggedCheckBox.setObjectName(u"showUntaggedCheckBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.showUntaggedCheckBox)

        self.label_4 = QLabel(Settings)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_4)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Search directory:", None))
        self.browseFiles.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"Manage tags:", None))
        self.tagEditorButton.setText(QCoreApplication.translate("Settings", u"Tag editor", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"Manage variables:", None))
        self.variableManagerButton.setText(QCoreApplication.translate("Settings", u"Variable manager", None))
        self.showUntaggedCheckBox.setText(QCoreApplication.translate("Settings", u"Show", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"Untagged shelf:", None))
    # retranslateUi

