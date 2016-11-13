from PyQt5.QtWidgets import QWidget, QDesktopWidget
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


class MainW(BaseW):
    def __init__(self):
        super(MainW, self).__init__()
        self._init("Main", 800, 500)
    
class SplashW(BaseW):
    def __init__(self):
        super(SplashW, self).__init__()
        self._init("Welcome...", 300, 200)
    