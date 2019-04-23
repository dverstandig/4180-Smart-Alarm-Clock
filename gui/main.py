import sys
import os
import time

# Qt Packages
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# UI mainwindow conversion
import mainwindow_auto
# JSON Packages
import json
# HTTP Image Request
from PIL import Image
import requests
from io import BytesIO
from PIL.ImageQt import ImageQt

weather_json = 1



# Single Window GUI (MainWindow)
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # Init all widgits in MainWindow
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # self.setStyleSheet("background-color: #a7adb7;")
        self.json = None
        self.comm_json = None
        self.alarm = None
        self.alarm_time = None
        self.dev_path = "Resource/"
        self.pi_path = "home/pi/build/SampleApp/src/"
        # print(self.comm_json)

        # Check For Data
        self.checkFile()
        # self.updateWeather()

        file_timer = QTimer(self)
        file_timer.timeout.connect(self.loadWeather)
        file_timer.start(2000)
        self.updateWeather()

        file_timer = QTimer(self)
        file_timer.timeout.connect(self.loadAlarm)
        file_timer.start(2500)

        self.updateCommute()
        file_timer = QTimer(self)
        file_timer.timeout.connect(self.loadCommute)
        file_timer.start(3000)

        # file_timer = QTimer(self)
        # file_timer.timeout.connect(self.setupForecast)
        # file_timer.start(4700)

        # print("updating weather")

        # Time Label
        self.time_label.setAlignment(Qt.AlignCenter)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start()

        # Weather Label
        self.weather_label.setAlignment(Qt.AlignRight)
        w_timer = QTimer(self)
        w_timer.start(5600)
        w_timer.timeout.connect(self.updateWeather)
        self.location_label.setAlignment(Qt.AlignRight)
        self.greetLabel()

        # Date Label
        self.date_label.setAlignment(Qt.AlignCenter)
        date_timer = QTimer(self)
        date_timer.timeout.connect(self.updateDate)
        date_timer.start(2000)

        # Alarm Button
        self.alarm_button.setCheckable(True)
        self.alarm_button.toggle()
        self.alarm_button.clicked.connect(self.updateAlarm)
        timer.timeout.connect(self.updateAlarm)

        # Commute Label
        comm_timer = QTimer(self)
        comm_timer.timeout.connect(self.updateCommute)
        comm_timer.start(6000)


    # Check File Connect Function
    def checkFile(self):
        self.loadWeather()
        self.loadAlarm()
        self.loadCommute()
        self.setupForecast()


    # Date Label Connect Function
    def showTime(self):
        time = QTime.currentTime()
        time_text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            time_text = time_text[:2] + ' ' + time_text[3:]
            time_text = time_text[:5] + ' ' + time_text[6:]
        self.time_label.setText(time_text)


    # Weather Label Connect Function
    def updateWeather(self):
        if self.json is not None:
            URL = self.json["currentWeatherIcon"]["sources"][0]["url"]
            response = requests.get(URL)
            # print(response)
            img = Image.open(BytesIO(response.content))
            # print("got image")
            qimage = ImageQt(img)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.weather_label.setPixmap(pixmap)
            location = self.json["title"]["mainTitle"]
            self.location_label.setText(location)
            temp = self.json["currentWeather"]
            self.temp_label.setText(temp)
            self.setupForecast()

    # Date Label Connect Function
    def updateDate(self):
        date = QDate.currentDate()
        text = "Today is " + date.toString(Qt.DefaultLocaleLongDate)
        self.date_label.setText(text)

    # Alarm Update Connect Function
    def updateAlarm(self):
        if self.alarm == 0:
            self.alarm_button.setText("No Alarm! Sleep In!")
        elif self.alarm == 1:
            self.alarm_button.setText("Alarm at " + self.alarm_time.toString())
        if self.alarm_button.isChecked():
            if self.alarm is not None and self.alarm == 1:
                self.alarm_button.setText("Alarm at " + self.alarm_time.toString())
        else:
            self.alarm_button.setText("No Alarm! Sleep In!")
            self.alarm = 0

    # Forecast Labels Connect Function
    def setupForecast(self):
        if self.json is not None:
            icon_list = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
            day_list = [self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12]
            i = 0
            for icon_label in icon_list:
                URL = self.json["weatherForecast"][i]["image"]["sources"][0]["url"]
                response = requests.get(URL)
                img = Image.open(BytesIO(response.content))
                qimage = ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(qimage)
                icon_label.setPixmap(pixmap)
                i += 1
            i = 0
            for day_label in day_list:
                day = self.json["weatherForecast"][i]["day"]
                day_label.setText(day)
                i += 1

    # Set Greeting Connect Function
    def greetLabel(self):
        time = QTime.currentTime().hour()
        # print(time)
        if time < 12:
            greet = "Good Morning!"
        elif time < 17:
            greet = "Good Afternoon!"
        else:
            greet = "Good Evening!"
        self.greeting_label.setText(greet)

    # Set Daily Commute Connect Function
    def updateCommute(self):
        if self.comm_json is not None:
            qimage = ImageQt(self.dev_path+ "/car_small.png")
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.comm_icon.setPixmap(pixmap)
            text = self.comm_json["textField"]
            self.comm_label.setText(text)
        else:
            self.comm_label.setText("")
            self.comm_icon.setText("")

    # Load Weather Text File from Alexa Output
    def loadWeather(self):
        path = self.dev_path + "example.txt"
        # print(path)
        file = open(path, "r")
        if os.stat(path).st_size == 0:
            print("empty")
            self.json = None
        else:
            # print(file)
            self.json = json.load(file)
        file.flush()
        file.close()

    # Load Commute Text File from Alexa Output
    def loadCommute(self):
        path = self.dev_path + "CommuteFile.txt"
        commute_file = open(path)
        if os.stat(path).st_size == 0:
            print("empty")
            self.comm_json = None
        else:
            # print(commute_file)
            self.comm_json = json.load(commute_file)
        commute_file.flush()
        commute_file.close()

    # Load Alarm Text File from Alexa Output
    def loadAlarm(self):
        path = self.dev_path + "AlarmFile.txt"
        alarm_file = open(path)
        if os.stat(path).st_size == 0:
            print("empty")
            self.alarm = None
        else:
            line1 = alarm_file.readline()
            line2 = alarm_file.readline()
            # print(int(line1))
            self.alarm = int(line1)
            if self.alarm != 0:
                # print(int(line2[0:2]))
                alarm_hour = int(line2[0:2])
                alarm_minute = int(line2[3:5])
                # print(alarm_minute)
                self.alarm_time = QTime(alarm_hour, alarm_minute)
        alarm_file.flush()
        alarm_file.close()


# Run as script Python3
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

# Script
if __name__ == "__main__":
    main()