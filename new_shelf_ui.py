# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newshelf.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QCheckBox, QDialog, QDialogButtonBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPlainTextEdit,
    QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_NewShelfDialog(object):
    def setupUi(self, NewShelfDialog):
        if not NewShelfDialog.objectName():
            NewShelfDialog.setObjectName(u"NewShelfDialog")
        NewShelfDialog.resize(823, 558)
        self.verticalLayout = QVBoxLayout(NewShelfDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(NewShelfDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tagsList = QListWidget(NewShelfDialog)
        self.tagsList.setObjectName(u"tagsList")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsList.sizePolicy().hasHeightForWidth())
        self.tagsList.setSizePolicy(sizePolicy)
        self.tagsList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tagsList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tagsList.setFlow(QListView.LeftToRight)
        self.tagsList.setProperty("isWrapping", True)
        self.tagsList.setResizeMode(QListView.Adjust)
        self.tagsList.setLayoutMode(QListView.SinglePass)
        self.tagsList.setModelColumn(0)
        self.tagsList.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.tagsList)

        self.label_2 = QLabel(NewShelfDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.varTable = QTableWidget(NewShelfDialog)
        if (self.varTable.columnCount() < 3):
            self.varTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.varTable.setObjectName(u"varTable")
        self.varTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.varTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.varTable)

        self.label_6 = QLabel(NewShelfDialog)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.line = QFrame(NewShelfDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_4 = QLabel(NewShelfDialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.nameEdit = QLineEdit(NewShelfDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.verticalLayout.addWidget(self.nameEdit)

        self.label_3 = QLabel(NewShelfDialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.filterEdit = QPlainTextEdit(NewShelfDialog)
        self.filterEdit.setObjectName(u"filterEdit")

        self.verticalLayout.addWidget(self.filterEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(NewShelfDialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.limitSpinBox = QSpinBox(NewShelfDialog)
        self.limitSpinBox.setObjectName(u"limitSpinBox")
        self.limitSpinBox.setMaximum(1000)
        self.limitSpinBox.setValue(100)

        self.horizontalLayout_2.addWidget(self.limitSpinBox)

        self.shuffleCheckBox = QCheckBox(NewShelfDialog)
        self.shuffleCheckBox.setObjectName(u"shuffleCheckBox")

        self.horizontalLayout_2.addWidget(self.shuffleCheckBox)

        self.picturesCheckBox = QCheckBox(NewShelfDialog)
        self.picturesCheckBox.setObjectName(u"picturesCheckBox")

        self.horizontalLayout_2.addWidget(self.picturesCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(NewShelfDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewShelfDialog)
        self.buttonBox.accepted.connect(NewShelfDialog.accept)
        self.buttonBox.rejected.connect(NewShelfDialog.reject)

        QMetaObject.connectSlotsByName(NewShelfDialog)
    # setupUi

    def retranslateUi(self, NewShelfDialog):
        NewShelfDialog.setWindowTitle(QCoreApplication.translate("NewShelfDialog", u"New Shelf", None))
        self.label.setText(QCoreApplication.translate("NewShelfDialog", u"Tag reference:", None))
        self.label_2.setText(QCoreApplication.translate("NewShelfDialog", u"Variable reference:", None))
        ___qtablewidgetitem = self.varTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("NewShelfDialog", u"Name", None));
        ___qtablewidgetitem1 = self.varTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("NewShelfDialog", u"Minimum", None));
        ___qtablewidgetitem2 = self.varTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("NewShelfDialog", u"Maximum", None));
        self.label_6.setText(QCoreApplication.translate("NewShelfDialog", u"Syntax reference:  [tag] |path| {variable = x} AND OR !", None))
        self.label_4.setText(QCoreApplication.translate("NewShelfDialog", u"Name:", None))
        self.nameEdit.setPlaceholderText(QCoreApplication.translate("NewShelfDialog", u"New shelf", None))
        self.label_3.setText(QCoreApplication.translate("NewShelfDialog", u"Filter:", None))
        self.filterEdit.setPlaceholderText(QCoreApplication.translate("NewShelfDialog", u"Eg. ([Action] AND [Horror]) OR ([Drama] AND {Year < 2010})", None))
        self.label_5.setText(QCoreApplication.translate("NewShelfDialog", u"Limit:", None))
        self.shuffleCheckBox.setText(QCoreApplication.translate("NewShelfDialog", u"Shuffle", None))
        self.picturesCheckBox.setText(QCoreApplication.translate("NewShelfDialog", u"Pictures", None))
    # retranslateUi

