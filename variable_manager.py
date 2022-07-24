from ui.variable_manager_ui import Ui_VariableManager
from PySide6.QtWidgets import *


class VariableManager(QDialog):
    def __init__(self, cur):
        super().__init__()
        self.ui = Ui_VariableManager()
        self.ui.setupUi(self)
        self.cur = cur

        self.load_variables()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.addButton.clicked.connect(self.add_variable)
        self.ui.removeButton.clicked.connect(self.remove_variable)
        self.show()

    def load_variables(self):
        self.variables = self.cur.execute(
            "SELECT variable, min, max FROM variables").fetchall()
        for (var, min, max) in self.variables:
            self.append_to_table(var, min, max)

    def append_to_table(self, var, min, max):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        var_item = QTableWidgetItem(var)
        min_item = QTableWidgetItem(str(min))
        max_item = QTableWidgetItem(str(max))
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount()-1, 0, var_item)
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount()-1, 1, min_item)
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount()-1, 2, max_item)

    def add_variable(self):
        new_variable = self.ui.lineEdit.text()
        min = self.ui.minSpinBox.value()
        max = self.ui.maxSpinBox.value()
        self.cur.execute(
            "INSERT INTO variables (variable, min, max) VALUES (?, ?, ?)", (new_variable, min, max))
        self.append_to_table(new_variable, min, max)
        self.ui.lineEdit.clear()
        self.ui.minSpinBox.setValue(0)
        self.ui.maxSpinBox.setValue(0)

    def remove_variable(self):
        variables = self.ui.tableWidget.selectionModel().selectedRows()
        for variable in variables:
            self.cur.execute(
                "DELETE FROM variables WHERE variable = ?", (variable.data(),))
            self.ui.tableWidget.removeRow(variable.row())
        self.ui.tableWidget.clear()
        self.load_variables()
