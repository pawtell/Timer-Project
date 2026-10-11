import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow): #inherits from QMainWindow
    def __init__(self): 
        super().__init__() #calls QMainWindow constructor
        self.setWindowTitle("Timer Project") #sets window title
        self.resize(500,500) # TODO: center on screen 
        self.setWindowIcon(QIcon("cclock.png"))

         # Main widget and vertical layout
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Empty space above the timer
        layout.addStretch()

        # Timer display
        self.timer_label = QLabel("05:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 36))

        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Minutes and seconds inputs
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 99)
        self.minutes_input.setValue(5)
        self.minutes_input.setPrefix("Minutes: ")

        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setValue(0)
        self.seconds_input.setPrefix("Seconds: ")

        input_layout.addWidget(self.minutes_input)
        input_layout.addWidget(self.seconds_input)

        layout.addLayout(input_layout)

        # Start, Pause, and Reset buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        # Empty space below the buttons
        layout.addStretch()   




def main():
    app = QApplication(sys.argv) #calls constructor for QApp, allows pyQt to process command line arguments (future proofing)
    window = MainWindow() #call mainwindow constructor
    window.show() #allows the window to actually appear
    sys.exit(app.exec()) # ensures clean exit when app execute method is called

if __name__ == "__main__": #Calls main function to start
    main()