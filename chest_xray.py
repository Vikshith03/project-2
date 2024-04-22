from PyQt5.QtGui import QMovie

import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog  #PyQt5 is cross-platform GUI toolkit
from PyQt5.QtGui import QPixmap
from win32com.client import Dispatch 

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

class PneumoniaDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNEUMONIA Detection App")
        self.setGeometry(100, 100, 900, 700)  
        self.centralwidget = QLabel(self)
        self.centralwidget.setGeometry(0, 0, 901, 701)  
        self.centralwidget.setStyleSheet("background-color: #035874;")

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(80, -60, 541, 561)
        self.gif=QMovie("picture.gif")
        self.label.setMovie(self.gif)
        self.gif.start()
        # No QMovie for simplicity

        self.label_result = QLabel(self.centralwidget)
        self.label_result.setGeometry(80, 430, 591, 41)
        self.label_result.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.label_result.setText("PNEUMONIA Detection")

        self.btn_upload = QPushButton("Upload Image", self.centralwidget)
        self.btn_upload.setGeometry(30, 530, 201, 31)
        self.btn_upload.clicked.connect(self.upload_image)

        self.btn_predict = QPushButton("Prediction", self.centralwidget)
        self.btn_predict.setGeometry(450, 530, 201, 31)
        self.btn_predict.clicked.connect(self.predict_result)

        self.model = load_model('chest_xray.h5')

    def upload_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            img = image.load_img(filename, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            self.image_data = img_array
            pixmap = QPixmap(filename)
            self.label.setPixmap(pixmap.scaled(541, 561))  # Scale pixmap to fit QLabel

    def predict_result(self):
        if hasattr(self, 'image_data'):
            result = self.model.predict(self.image_data)
            print(result)
            if result[0][0] > 0.5:
                self.label_result.setText("Result is Normal")
                speak("Result is Normal")
            else:
                self.label_result.setText("Affected By PNEUMONIA")
                speak("Affected By PNEUMONIA")
        else:
            self.label_result.setText("No image uploaded yet.")
            print("No image uploaded yet.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = PneumoniaDetectorApp()
    MainWindow.show()
    sys.exit(app.exec_())