# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'details.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_Details(object):
    def setupUi(self, Details):
        if not Details.objectName():
            Details.setObjectName(u"Details")
        Details.resize(400, 300)
        self.formLayout = QFormLayout(Details)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Details)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.buttonBox = QDialogButtonBox(Details)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.buttonBox)

        self.titleBrowser = QTextBrowser(Details)
        self.titleBrowser.setObjectName(u"titleBrowser")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.titleBrowser)

        self.label_2 = QLabel(Details)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.tagsList = QListWidget(Details)
        self.tagsList.setObjectName(u"tagsList")
        self.tagsList.setSortingEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.tagsList)


        self.retranslateUi(Details)
        self.buttonBox.accepted.connect(Details.accept)
        self.buttonBox.rejected.connect(Details.reject)

        QMetaObject.connectSlotsByName(Details)
    # setupUi

    def retranslateUi(self, Details):
        Details.setWindowTitle(QCoreApplication.translate("Details", u"Details", None))
        self.label.setText(QCoreApplication.translate("Details", u"Title:", None))
        self.label_2.setText(QCoreApplication.translate("Details", u"Tags:", None))
    # retranslateUi

