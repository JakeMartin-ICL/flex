from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, QToolButton,
                               QWidget)


class NameBar(QWidget):
    def __init__(self, name):
        super().__init__()

        self.setObjectName(u"nameBar")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.shelfName = QLabel(self)
        self.shelfName.setObjectName(u"shelfName")
        self.shelfName.setText(name)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shelfName.sizePolicy().hasHeightForWidth())
        self.shelfName.setSizePolicy(sizePolicy)
        self.shelfName.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.shelfName)

        self.shelfToolButton = QToolButton(self)
        self.shelfToolButton.setObjectName(u"shelfToolButton")

        self.horizontalLayout.addWidget(self.shelfToolButton)
