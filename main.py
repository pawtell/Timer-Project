import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QTimer, QElapsedTimer

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
        #self.timer_label.setFont(QFont("Arial", 36))

        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Minutes and seconds inputs
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 99)
        self.minutes_input.setValue(5)
        self.minutes_input.setPrefix("Minutes: ")
        QTimer.singleShot(0, lambda: self.minutes_input.lineEdit().setCursorPosition(
            len(self.minutes_input.lineEdit().text())
        ))

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

        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.reset_button.clicked.connect(self.reset)
        # While idle, time label previews input time
        self.minutes_input.valueChanged.connect(self.refresh_ui)
        self.seconds_input.valueChanged.connect(self.refresh_ui)

        # Timer state, tried to keep the logic somewhat portable for future projects
        self.state = "idle"     # "idle" | "running" | "paused" | "finished"
        self.total_ms = 0       # total duration, captured on a fresh start
        self.time_elapsed = 0   # needed for pause and resume logic - each pause adds to this

        # Main timer - starts from 0, only records how much time elapsed since last start()
        self.clock = QElapsedTimer()

        # Interval timer to update displayed time every 100 ms; doesn't measure time itself
        self.tick = QTimer(self)
        self.tick.setInterval(100)
        self.tick.timeout.connect(self.update_display)
        

        self.refresh_ui()

        self.setStyleSheet("""
            QPushButton{
                font-size: 50px;
                font-family: "Roboto";
            }
            QPushButton:hover {
                background-color: #30422b;
            }
            QPushButton:pressed {
                background-color: #1A202C;
            }
            QLabel{
                font-size: 100px;
                font-family: "Roboto";
            }
            QSpinBox {
                font-family: "Roboto";
                font-size: 15px;
                font-weight: 5000;
                border: 1px solid #555;
                border-radius: 6px;
                background-color: #222;
                color: white;
                min-width: 100px
            }
            QSpinBox:hover {
                background-color: #30422b;
            }
            QSpinBox:Focus{
                border: 1px solid #63B3ED;
            }
            QSpinBox::up-button {
                width: 25px;
            }
            QSpinBox::down-button {
                width: 25px;
            }
        """)

    def start(self):
        # Fresh start: grab the inputs and clear old time passed value
        if self.state == "idle":
            self.total_ms = self.input_ms()
            self.time_elapsed = 0

            # Catches edge case where total input time is 0
            if self.total_ms == 0:
                return

            self.clock.start()      # start elapsed timer - starts from 0
            self.tick.start()       # start 100ms interval timer
            self.state = "running"
            self.refresh_ui()       # update right away instead of waiting 100 ms

        # Resume: keep total_ms and time_elapsed, start a new stretch
        elif self.state == "paused":
            self.clock.start()      # clock now measures only this new stretch
            self.tick.start()
            self.state = "running"
            self.refresh_ui()

    def pause(self):
        # Error catch - verifies timer running
        if self.state != "running":
            return

        # Note the time from this stretch
        stretch = self.clock.elapsed()                  # ms since the last start/resume
        self.time_elapsed = self.time_elapsed + stretch # adds, not overwrites to account for multiple pauses if user decides to

        # Pause the display
        self.tick.stop()
        self.state = "paused"
        self.refresh_ui()

    def reset(self):
        # Stop interval timer, stops updating display too
        self.tick.stop()

        # Clears values held
        self.total_ms = 0
        self.time_elapsed = 0

        # State -> idle, timer display resets, unlocks inputs
        self.state = "idle"
        self.refresh_ui()

    # Helper function, turns ms into readable MM:SS
    # Rounds partial seconds up
    def format_time(self, ms):
        total_seconds = (ms + 999) // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_display(self):
        time_left = self.remaining_ms()

        if time_left == 0:
            self.tick.stop()
            self.state = "finished"

        self.refresh_ui()

    def input_ms(self):
        return (self.minutes_input.value() * 60 + self.seconds_input.value()) * 1000

    # Helper, total ms - time counted during stretch in ms, if timer is running
    def remaining_ms(self):
        if self.state == "idle":
            return self.input_ms()
        if self.state == "finished":
            return 0
        used = self.time_elapsed
        if self.state == "running":
            used += self.clock.elapsed()    # add the current running stretch
        return max(0, self.total_ms - used) # failsafe, never returns negative 


    def refresh_ui(self):
        # 1. Update the time display
        time_left = self.remaining_ms()
        time_text = self.format_time(time_left)
        self.timer_label.setText(time_text)

        # 2. Start with everything OFF
        start_on = False
        pause_on = False
        reset_on = False
        inputs_on = False

        # each state turns ON only what it allows
        if self.state == "idle":
            start_on = True
            inputs_on = True
        elif self.state == "running":
            pause_on = True
            reset_on = True
        elif self.state == "paused":
            start_on = True      # Start acts as Resume here
            reset_on = True
        elif self.state == "finished":
            reset_on = True      # only way out is Reset

        # 3. Lock the widgets to prevent errors from happening
        self.start_button.setEnabled(start_on)
        self.pause_button.setEnabled(pause_on)
        self.reset_button.setEnabled(reset_on)
        self.minutes_input.setEnabled(inputs_on)
        self.seconds_input.setEnabled(inputs_on)



def main():
    app = QApplication(sys.argv) #calls constructor for QApp, allows pyQt to process command line arguments (future proofing)
    window = MainWindow() #call mainwindow constructor
    window.show() #allows the window to actually appear
    sys.exit(app.exec()) # ensures clean exit when app execute method is called

if __name__ == "__main__": #Calls main function to start
    main()