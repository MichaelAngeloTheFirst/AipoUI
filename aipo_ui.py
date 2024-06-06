from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

app = QApplication([])
window = QWidget()

# layout
layout = QVBoxLayout()
layout.addWidget(QPushButton("Top"))
layout.addWidget(QPushButton("Bottom"))
######################################


window.setLayout(layout)
window.setWindowTitle("Aipo")
window.setMinimumSize(400, 300)


window.show()
app.exec()
