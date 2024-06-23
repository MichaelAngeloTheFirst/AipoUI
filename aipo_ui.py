import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "AiPO"
        self.left = 10
        self.top = 10
        self.width = 420
        self.height = 380
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.label = QLabel('No image selected')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        buttonLayout = QHBoxLayout()

        self.selectButton = QPushButton('Select image')
        self.selectButton.clicked.connect(self.openFileNameDialog)
        self.selectButton.setStyleSheet("background-color: lightblue;")
        buttonLayout.addWidget(self.selectButton)

        self.uploadButton = QPushButton('Check personal information')
        self.uploadButton.clicked.connect(self.upload_image)
        self.uploadButton.setStyleSheet("background-color: lightgreen;")
        buttonLayout.addWidget(self.uploadButton)

        layout.addLayout(buttonLayout)

        self.resultLabel = QLabel('Your personal information')
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setMaximumSize(800,1200)
        
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            self.label.setPixmap(QPixmap(fileName).scaled(400, 400, Qt.KeepAspectRatio))
            self.fileName = fileName

    def format_personal_data(self, data):
        formatted_text = (
            f"First Name: {str(data['first_name']).replace('{', '').replace('}', '')}\n"
            f"Last Name: {str(data['last_name']).replace('{', '').replace('}', '')}\n"
            f"PESEL: {str(data['pesel']).replace('{', '').replace('}', '')}\n"
            f"Place of Birth: {str(data['place_of_birth']).replace('{', '').replace('}', '')}\n"
            f"Date of Birth: {str(data['date_of_birth']).replace('{', '').replace('}', '')}\n"
            f"Nationality: {str(data['nationality']).replace('{', '').replace('}', '')}\n"
            f"Sex: {str(data['sex']).replace('{', '').replace('}', '')}\n"
            f"Signature: {str(data['signature']).replace('{', '').replace('}', '')}\n"
            f"Passport data: [{str(data['passport']).replace('{', '').replace('}', '')}]\n"
            f"Identity Card data: [{str(data['identitycard']).replace('{', '').replace('}', '')}]"
        )
        return formatted_text


    def upload_image(self):
        if hasattr(self, 'fileName'):
            url = 'http://127.0.0.1:8000/photo_data' 
            files = {'file': open(self.fileName, 'rb')}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                self.resultLabel.setText(self.format_personal_data( response.json()))
            else:
                self.resultLabel.setText('Error uploading image')
        else:
            self.resultLabel.setText('No Image Selected')

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
