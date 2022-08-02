from PySide6.QtWidgets import (QDialogButtonBox, QHeaderView, QLabel,
                               QTableWidgetItem, QTextBrowser, QDialog)

from query_parser import SQLify
from ui.new_shelf_ui import Ui_NewShelfDialog


class EditShelfDialog(QDialog):
    def __init__(self, cur, config, name):
        super().__init__()
        self.ui = Ui_NewShelfDialog()
        self.ui.setupUi(self)
        self.cur = cur
        self.config = config
        self.name = name

        shelf_config = config["shelves"][name]
        self.ui.nameEdit.setText(name)
        self.ui.filterEdit.setPlainText(shelf_config["filter"])
        self.ui.limitSpinBox.setValue(shelf_config["limit"])
        self.ui.shuffleCheckBox.setChecked(shelf_config["shuffle"])
        self.pictures = shelf_config["pictures"]
        self.ui.picturesCheckBox.setChecked(self.pictures)
        self.ui.sizeSpinBox.setValue(
            180 if "picture_size" not in shelf_config else shelf_config["picture_size"])
        #self.ui.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Discard | QDialogButtonBox.C)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Delete")

        self.load_tags()
        self.load_variables()
        self.ui.varTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.buttonBox.accepted.connect(self.edit_filter)
        self.ui.buttonBox.rejected.connect(self.delete_filter)
        self.ui.sizeSpinBox.valueChanged.connect(self.change_size)

        self.sql_label = QLabel("Generated SQL:")
        self.sql_browser = QTextBrowser()
        self.sql_browser.setPlainText(SQLify(self.ui.filterEdit.toPlainText(
        ), shelf_config["limit"], shelf_config["shuffle"]))
        self.ui.verticalLayout.insertWidget(
            self.ui.verticalLayout.count() - 1, self.sql_label)
        self.ui.verticalLayout.insertWidget(
            self.ui.verticalLayout.count() - 1, self.sql_browser)

        self.show()

    def load_tags(self):
        self.tags = [tag for (tag, ) in self.cur.execute(
            "SELECT tag from tags").fetchall()]
        self.ui.tagsList.addItems(self.tags)

    def load_variables(self):
        self.variables = self.cur.execute(
            "SELECT variable, min, max FROM variables").fetchall()
        for (var, min, max) in self.variables:
            self.append_to_table(var, min, max)

    def append_to_table(self, var, min, max):
        self.ui.varTable.insertRow(self.ui.varTable.rowCount())
        var_item = QTableWidgetItem(var)
        min_item = QTableWidgetItem(str(min))
        max_item = QTableWidgetItem(str(max))
        self.ui.varTable.setItem(self.ui.varTable.rowCount()-1, 0, var_item)
        self.ui.varTable.setItem(self.ui.varTable.rowCount()-1, 1, min_item)
        self.ui.varTable.setItem(self.ui.varTable.rowCount()-1, 2, max_item)

    def edit_filter(self):
        pictures = self.ui.picturesCheckBox.checkState() == 2
        self.config["shelves"][self.ui.nameEdit.text()] = {"filter": self.ui.filterEdit.toPlainText(), "limit": self.ui.limitSpinBox.value(
        ), "shuffle": self.ui.shuffleCheckBox.checkState() == 2, "pictures": pictures, "picture_size": self.ui.sizeSpinBox.value()}

    def change_size(self, value):
        pictures = self.ui.picturesCheckBox.checkState() == 2
        self.config["shelves"][self.ui.nameEdit.text()] = {"filter": self.ui.filterEdit.toPlainText(), "limit": self.ui.limitSpinBox.value(
        ), "shuffle": self.ui.shuffleCheckBox.checkState() == 2, "pictures": pictures, "picture_size": value}

    def delete_filter(self):
        del self.config["shelves"][self.name]
        self.config["order"].remove(self.name)

    def get_config(self):
        return self.config
