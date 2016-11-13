import sys
from PyQt5.QtWidgets import QApplication
from windows import MainW

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    main = MainW(app)
    main.show()    
        
    sys.exit(app.exec_())