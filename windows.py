from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QMessageBox, QMainWindow, QAction, QDialog,
    QGridLayout, QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QIcon
from time import sleep

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
        print(r)

    def showEvent(self, event):
        if not self._wasShown:
            self._wasShown = True
            self._openDbFile()


class OpenDbW(BaseW):
    def __init__(self, mainW):
        super(OpenDbW, self).__init__(mainW)
        self._init("Open db file...", 450, 200)
        self._createWidgets()
        self._createLayout()

    def _createWidgets(self):
        self._dbFile = QLineEdit()

        self._dbPass = QLineEdit()
        self._dbPass.setEchoMode(QLineEdit.Password) 
        
        self._openFileBtn = QPushButton("...")

        #TODO: add buttons to dialog within QHBoxLayoyt within QVBoxLayout
        #self._okBtn = QPushButton("OK")
        #self._cancelBtn = QPushButton("Cancel")

    def _createLayout(self):
        #TODO: add grid within QVBoxLayout
        grid = QGridLayout()
        #grid.setSpacing(10)

        grid.addWidget(QLabel("Database file"), 0, 0)
        grid.addWidget(self._dbFile, 0, 1)
        grid.addWidget(self._openFileBtn, 0, 2)

        grid.addWidget(QLabel("Password"), 1, 0)
        grid.addWidget(self._dbPass, 1, 1)        

        self.setLayout(grid)
        