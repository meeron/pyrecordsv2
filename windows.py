from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QMainWindow, QAction
from PyQt5.QtGui import QIcon

class BaseW(QWidget):
    def __init__(self):
        super(BaseW, self).__init__()

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
        pass

#class SplashW(BaseW):
#    def __init__(self):
#        super(SplashW, self).__init__()
#        self._init("Welcome...", 300, 200)
#
#    def closeEvent(self, event):
#        answer = QMessageBox.question(self,"Exiting...", "Are you sure?",
#        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#
#        if answer == QMessageBox.No:
#            event.ignore()
    