# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'variablemanager.ui'
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
    QDialogButtonBox, QFormLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_VariableManager(object):
    def setupUi(self, VariableManager):
        if not VariableManager.objectName():
            VariableManager.setObjectName(u"VariableManager")
        VariableManager.resize(455, 518)
        self.verticalLayout = QVBoxLayout(VariableManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(VariableManager)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.tableWidget)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(VariableManager)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(VariableManager)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaxLength(30)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(VariableManager)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.minSpinBox = QSpinBox(VariableManager)
        self.minSpinBox.setObjectName(u"minSpinBox")
        self.minSpinBox.setMaximum(100000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.minSpinBox)

        self.label_3 = QLabel(VariableManager)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.maxSpinBox = QSpinBox(VariableManager)
        self.maxSpinBox.setObjectName(u"maxSpinBox")
        self.maxSpinBox.setMaximum(100000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.maxSpinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(VariableManager)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)

        self.removeButton = QPushButton(VariableManager)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout.addWidget(self.removeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(VariableManager)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(VariableManager)
        self.buttonBox.accepted.connect(VariableManager.accept)
        self.buttonBox.rejected.connect(VariableManager.reject)

        QMetaObject.connectSlotsByName(VariableManager)
    # setupUi

    def retranslateUi(self, VariableManager):
        VariableManager.setWindowTitle(QCoreApplication.translate("VariableManager", u"Variable Manager", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VariableManager", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VariableManager", u"Minimum", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("VariableManager", u"Maximum", None));
        self.label.setText(QCoreApplication.translate("VariableManager", u"Name:", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("VariableManager", u"New variable", None))
        self.label_2.setText(QCoreApplication.translate("VariableManager", u"Minimum:", None))
        self.label_3.setText(QCoreApplication.translate("VariableManager", u"Maximum:", None))
        self.addButton.setText(QCoreApplication.translate("VariableManager", u"Add", None))
#if QT_CONFIG(shortcut)
        self.addButton.setShortcut(QCoreApplication.translate("VariableManager", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.removeButton.setText(QCoreApplication.translate("VariableManager", u"Remove", None))
#if QT_CONFIG(shortcut)
        self.removeButton.setShortcut(QCoreApplication.translate("VariableManager", u"Del", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

