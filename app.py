import sys
from PyQt5.QtWidgets import QApplication
from windows import MainW, SplashW

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    splash = SplashW()
    splash.show()    
        
    sys.exit(app.exec_())