import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow): #inherits from QMainWindow
    def __init__(self): 
        super().__init__() #calls QMainWindow constructor
        self.setWindowTitle("Timer Project") #sets window title
        self.resize(500,500) # TODO: center on screen 
        self.setWindowIcon(QIcon("cclock.png"))

def main():
    app = QApplication(sys.argv) #calls constructor for QApp, allows pyQt to process command line arguments (future proofing)
    window = MainWindow() #call mainwindow constructor
    window.show() #allows the window to actually appear
    sys.exit(app.exec()) # ensures clean exit when app execute method is called

if __name__ == "__main__": #Calls main function to start
    main()