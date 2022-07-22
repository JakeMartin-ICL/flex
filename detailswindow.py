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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QDialog, QDialogButtonBox, QFormLayout, QHeaderView,
    QLabel, QListView, QListWidget, QListWidgetItem,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTextBrowser,
    QWidget)

class Ui_Details(object):
    def setupUi(self, Details):
        if not Details.objectName():
            Details.setObjectName(u"Details")
        Details.resize(806, 339)
        self.formLayout = QFormLayout(Details)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Details)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.titleBrowser = QTextBrowser(Details)
        self.titleBrowser.setObjectName(u"titleBrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleBrowser.sizePolicy().hasHeightForWidth())
        self.titleBrowser.setSizePolicy(sizePolicy)
        self.titleBrowser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.titleBrowser)

        self.label_2 = QLabel(Details)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.tagsList = QListWidget(Details)
        self.tagsList.setObjectName(u"tagsList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tagsList.sizePolicy().hasHeightForWidth())
        self.tagsList.setSizePolicy(sizePolicy1)
        self.tagsList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tagsList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tagsList.setFlow(QListView.LeftToRight)
        self.tagsList.setProperty("isWrapping", True)
        self.tagsList.setResizeMode(QListView.Adjust)
        self.tagsList.setLayoutMode(QListView.SinglePass)
        self.tagsList.setModelColumn(0)
        self.tagsList.setSortingEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.tagsList)

        self.buttonBox = QDialogButtonBox(Details)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.buttonBox)

        self.label_3 = QLabel(Details)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.varTable = QTableWidget(Details)
        if (self.varTable.columnCount() < 6):
            self.varTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.varTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.varTable.setObjectName(u"varTable")
        sizePolicy1.setHeightForWidth(self.varTable.sizePolicy().hasHeightForWidth())
        self.varTable.setSizePolicy(sizePolicy1)
        self.varTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.varTable.setSelectionMode(QAbstractItemView.SingleSelection)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.varTable)


        self.retranslateUi(Details)
        self.buttonBox.accepted.connect(Details.accept)
        self.buttonBox.rejected.connect(Details.reject)

        QMetaObject.connectSlotsByName(Details)
    # setupUi

    def retranslateUi(self, Details):
        Details.setWindowTitle(QCoreApplication.translate("Details", u"Details", None))
        self.label.setText(QCoreApplication.translate("Details", u"Title:", None))
        self.label_2.setText(QCoreApplication.translate("Details", u"Tags:", None))
        self.label_3.setText(QCoreApplication.translate("Details", u"Variables:", None))
        ___qtablewidgetitem = self.varTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Details", u"Variable", None));
        ___qtablewidgetitem1 = self.varTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Details", u"Min", None));
        ___qtablewidgetitem2 = self.varTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Details", u"-", None));
        ___qtablewidgetitem3 = self.varTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Details", u"Max", None));
        ___qtablewidgetitem4 = self.varTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Details", u"Enabled", None));
        ___qtablewidgetitem5 = self.varTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Details", u"Value", None));
    # retranslateUi

