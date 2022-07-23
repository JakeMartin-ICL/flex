from new_shelf_ui import Ui_NewShelfDialog
from PySide6.QtWidgets import *

class NewShelfDialog(QDialog):
    def __init__(self, cur, config):
        super().__init__()
        self.ui = Ui_NewShelfDialog()
        self.ui.setupUi(self)
        self.cur = cur
        self.config = config

        self.ui.verticalLayout.removeItem(self.ui.horizontalLayout_3)
        self.show()

        self.load_tags()
        self.load_variables()
        self.ui.varTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.buttonBox.accepted.connect(self.add_filter)

        self.show()
    
    def load_tags(self):
        self.tags = [tag for (tag, ) in self.cur.execute("SELECT tag from tags").fetchall()]
        self.ui.tagsList.addItems(self.tags)

    def load_variables(self):
        self.variables = self.cur.execute("SELECT variable, min, max FROM variables").fetchall()
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
    
    def add_filter(self):
        name = self.ui.nameEdit.text()
        name = name if len(name) > 0 else f'New Shelf {len(self.config["order"])}'
        pictures = self.ui.picturesCheckBox.checkState() == 2
        self.config["shelves"][name] = {"filter": self.ui.filterEdit.toPlainText(), "limit": self.ui.limitSpinBox.value(), "shuffle": self.ui.shuffleCheckBox.checkState() == 2, "pictures" : pictures}
        self.config["order"].append(name)
    
    def get_config(self):
        return self.config