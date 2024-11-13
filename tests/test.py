import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit

app = QApplication(sys.argv)
win = QWidget()
win.resize(300, 300)
win.move(200, 200)
win.setWindowTitle('Medium Article')
# Create Buttons
btn = QPushButton('Quit', win)

# Message Box
QMessageBox.question(win, 'Message', "Are you sure to quit?")
# Label Text
lbl = QLabel('Hello World', win)
# Button Clicked
btn.clicked.connect(lambda: QMessageBox.question(win, 'Message', "Are you sure to quit?"))
# Entry Box
entry = QLineEdit(win)
win.show()
sys.exit(app.exec())

