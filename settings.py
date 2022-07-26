from PySide6.QtWidgets import QDialog, QFileDialog, QListWidgetItem

from tag_manager import TagManager
from ui.settings_ui import Ui_Settings
from variable_manager import VariableManager


class SettingsDialog(QDialog):
    def __init__(self, cur, dbcon, config):
        super().__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cur = cur
        self.dbcon = dbcon
        self.ui.pathEdit.setText(config["search_dir"])
        self.ui.pathEdit.textChanged.connect(self.edit_search_path)
        self.ui.vlcEdit.setText(config["vlc"])
        self.ui.vlcEdit.textChanged.connect(self.edit_vlc_path)
        self.ui.browseFiles.clicked.connect(self.browse_files)
        self.ui.tagEditorButton.clicked.connect(self.open_tag_manager)
        self.ui.variableManagerButton.clicked.connect(self.open_var_manager)
        self.ui.showUntaggedCheckBox.setChecked(config["show_untagged"])
        self.ui.showUntaggedCheckBox.stateChanged.connect(self.show_untagged)

        for name, shelf_config in config["shelves"].items():
            item = QListWidgetItem(name)
            self.ui.orderList.addItem(item)
        self.ui.orderList.model().rowsMoved.connect(self.update_order)

        self.config = config

    def edit_search_path(self, text):
        self.config["search_dir"] = text
    
    def edit_vlc_path(self, text):
        self.config["vlc"] = text

    def browse_files(self):
        path = QFileDialog.getExistingDirectory()
        self.config["search_dir"] = path
        self.ui.pathEdit.setText(path)

    def open_tag_manager(self):
        self.tag_manager = TagManager(self.cur)
        if self.tag_manager.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

    def open_var_manager(self):
        self.tag_manager = VariableManager(self.cur)
        if self.tag_manager.exec() == QDialog.Accepted:
            self.dbcon.commit()
        else:
            self.dbcon.rollback()

    def show_untagged(self, state):
        show = state == 2
        self.config["show_untagged"] = show

    def update_order(self):
        new_order = []
        for i in range(self.ui.orderList.count()):
            name = self.ui.orderList.item(i).text()
            new_order.append(name)
        self.config["order"] = new_order

    def get_config(self):
        return self.config
