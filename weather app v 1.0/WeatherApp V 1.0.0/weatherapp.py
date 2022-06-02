from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QTableWidgetItem
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from psycopg2 import connect
import sys
import requests
import time
from PyQt5.QtCore import pyqtSlot
# database baglanti

connection  = psycopg2.connect(host='localhost', user='postgres', password=#enterpass, dbname=#enterdabasename)
cur     = conn.cursor()

# hava durumu sitesi api key
apiKey  = '#enterapikey'

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("weather.ui", self)
        self.city = ""
        self.land = ""
        self.exitButton.clicked.connect(qApp.quit)
        self.weatherButton.clicked.connect(self.info_check)
        self.nthbuttton.clicked.connect(self.netherland_city)
        self.usabutton.clicked.connect(self.usa_city)
        self.trbutton.clicked.connect(self.tr_city)
        self.tableWidget.doubleClicked.connect(self.on_click)   

    def showTabel(self):
        # tablolari yazdirmak icin
        cur.execute(""" SELECT row_number () OVER (ORDER BY population DESC), city, province, population
                        FROM city_info where land=%s """, (self.land,))
        citytable = cur.fetchall()
        self.tableWidget.setRowCount(len(citytable))

        for i in range(len(citytable)):
            city_name   = citytable[i][1]  # city name
            province    = citytable[i][2]  # city pronivce
            population  = citytable[i][3]  # city population
            self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{city_name}"))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{province}"))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{population:,}"))

    def info_check(self):
        #ekranda city adini yazdirmak icin
        self.city = self.cityLine.text().title()
        #self.cityLabel.setText(self.city)
        self.cityLine.clear()
        cur.execute(""" SELECT city FROM city_info 
                        WHERE city LIKE %s """, (self.city,))
        result_city = cur.fetchone()
        #print(result_city)
        self.errlabel.setText("")

        if result_city == None:
            self.errlabel.setText("City not found.")
            self.popLabel.setText("")
            self.provinceLabel.setText("")
            self.cityLabel.setText("")
            self.degrelabel.setText("")
            self.citylandLabel.setText("")
            self.satatuslabel.setText("")            
            self.iconlabel.setPixmap(QtGui.QPixmap(""))
            self.updateDate.setText("")

        else:
            self.show_weather()

    def show_weather(self):
            self.cityLabel.setText(self.city)
            # databaseden city nin bilgileerini cekmek icin
            cur.execute(""" SELECT province, population, land FROM city_info 
                            WHERE city =%s """, (self.city,))
            cityInfo = cur.fetchone()
            # ekranda city nin bolgesini yazdirmak icin
            cityProvince = cityInfo[0]
            self.provinceLabel.setText(cityProvince)
            # ekranda city nin nufusunu yazdirmak icin
            cityPop = cityInfo[1]
            cityPop = f"{cityPop:,}"
            self.popLabel.setText(cityPop)
            # ekranda city ve ülke adini yazdirmak icin
            land = cityInfo[2]
            self.citylandLabel.setText(self.city+", "+land)
            # Api baglantisi
            my_links    = 'https://api.openweathermap.org/data/2.5/weather?q='+f"{self.city}"'&appid='+f"{apiKey}"'&units=metric'
            respons     = requests.get(my_links).json()
            # Sicaklik
            self.degrelabel.setText(str(int(respons['main']['temp']))+"°C")
            # hava durumu
            self.satatuslabel.setText(respons['weather'][0]['description'])
            # update date
            my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(respons['dt']))
            self.updateDate.setText(my_time)
            # hava durumu iconu
            self.iconlabel.setPixmap(QtGui.QPixmap(respons['weather'][0]['icon']+'@2x.png'))

    def netherland_city(self):
        self.land = 'Netherland'
        self.showTabel()

    def usa_city(self):
        self.land = 'Usa'
        self.showTabel()

    def tr_city(self):
        self.land = 'Turkey'
        self.showTabel()
        
    @pyqtSlot()
    def on_click(self):
        row         = self.tableWidget.currentRow() 
        self.city   = (self.tableWidget.item(row, 0).text())
        print(self.city)             
        self.show_weather()
     
if __name__ == "__main__":
    app     = QApplication(sys.argv)
    welcome = MainMenu()
    widget  = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(770)
    widget.setFixedWidth(940)
    widget.show()

    try:
        sys.exit(app.exec_())

    except:
        print("Exiting")
