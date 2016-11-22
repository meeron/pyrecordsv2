from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QMessageBox, QMainWindow, QAction, QDialog,
    QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox,
    QMessageBox)
from PyQt5.QtGui import QIcon
from time import sleep
from models import Storage, OpenDbStaus

class BaseW(QDialog):
    def __init__(self, parent=None):
        super(BaseW, self).__init__(parent)

    def _init(self, title, w, h, posX=0, posY=0):
        self.resize(w,h)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("resources/app-icon.png")) 
        
        if posX == 0 and posY == 0:
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        else:
            self.move(posX, posY)


class MainW(QMainWindow):
    def __init__(self, app):
        super(MainW, self).__init__()  
        self._init(app, "PyRecords", 800, 500)
        self._wasShown = False
        #self._storage = Storage()

    def _init(self, app, title, w, h, posX=0, posY=0):        
        self._app = app
        self._buildMenu(self._createMenu())

        self.resize(w,h)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("resources/app-icon.png")) 
        
        if posX == 0 and posY == 0:
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        else:
            self.move(posX, posY)

    def _createMenu(self):
        return {
            "&File": [
                self._createMenuAction("&Open Db...", "Ctrl+O", "Open Db file...", self._openDbFile),
                self._createMenuAction("&Exit", "Ctrl+Q", "Exit application", self._app.quit)
            ]
        }

    def _buildMenu(self, menuDef):
        menubar = self.menuBar()

        for key in menuDef.keys():
            menu = menubar.addMenu(key)
            for a in menuDef[key]:
                menu.addAction(a)
        
        self.statusBar()

    def _createMenuAction(self, name, shortcut, statusTip, action):
        menuAction = QAction(QIcon(""), name, self)        
        menuAction.setShortcut(shortcut)
        menuAction.setStatusTip(statusTip)
        menuAction.triggered.connect(action)
        return menuAction

    def _openDbFile(self):
        opendbw = OpenDbW(self)
        r = opendbw.exec()
        if r == QDialog.Accepted:
            #TODO: read data from dialog
            print("Db OK")

    def showEvent(self, event):
        if not self._wasShown:
            self._wasShown = True
            self._openDbFile()


class OpenDbW(BaseW):
    def __init__(self, mainW):
        super(OpenDbW, self).__init__(mainW)
        self._init("Open db file...", 450, 0)
        self._createWidgets()
        self._createLayout()

    def _createWidgets(self):
        self._dbFileLnEd = QLineEdit()

        self._dbPass = QLineEdit()
        self._dbPass.setEchoMode(QLineEdit.Password) 
        
        self._openFileBtn = QPushButton("...")

        self._openBtn = QPushButton("Open")
        self._openBtn.clicked.connect(self._openBtn_click)
        self._cancelBtn = QPushButton("Cancel")
        self._cancelBtn.clicked.connect(self._cancelBtn_click)

    def _createLayout(self):
        gridLayout = QGridLayout()
        gridLayout.setSpacing(10)
        
        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        
        buttonsLayout = QHBoxLayout()       

        gridLayout.addWidget(QLabel("Database file"), 0, 0)
        gridLayout.addWidget(self._dbFileLnEd, 0, 1)
        gridLayout.addWidget(self._openFileBtn, 0, 2)
        gridLayout.addWidget(QLabel("Password"), 1, 0)
        gridLayout.addWidget(self._dbPass, 1, 1)

        buttonsLayout.addWidget(self._cancelBtn)
        buttonsLayout.addWidget(self._openBtn)

        mainLayout.addLayout(gridLayout)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        
    def _cancelBtn_click(self):
        self.reject()

    def _openBtn_click(self):
        msg = None
        path = self._dbFileLnEd.text()
        pw = self._dbPass.text()
        if path and pw:
            storage = Storage(path, pw)
            status = storage.open()

            if status == OpenDbStaus.success:
                #TODO: save last successfuly opened file in users home directory
                self.accept()
            if status == OpenDbStaus.not_found:
                msg = "File '{0}' not found.".format(path)
            if status == OpenDbStaus.invalid_password:
                msg = "Password for '{0}' is invalid.".format(path)

            if msg:
                QMessageBox.warning(self, "Warning...", msg)