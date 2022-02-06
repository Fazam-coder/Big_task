import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic


class Example(QWidget):
    def __init__(self, coords, scale):
        super().__init__()
        self.coords = coords
        self.scale = scale
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        map_view = "map"
        map_params = {"ll": ",".join(self.coords),
                      "spn": ",".join([self.scale, self.scale]),
                      "l": map_view}
        self.response = requests.get(map_request, params=map_params)
        if not self.response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

    def initUI(self):
        uic.loadUi('design.ui', self)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.btn_find.clicked.connect(self.find_adress)

    def find_adress(self):
        if not self.edit_adress.text():
            return
        self.coords = get_coords(self.edit_adress.text())
        self.scale = get_scale(self.edit_adress.text())
        self.update_image()
        self.response = requests.get(self.response.url + '&pt=' + ','.join(self.coords) + ',pm2dgl')
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def update_image(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if float(self.coords[0]) - 3 * float(self.scale) >= -180:
                self.coords[0] = str(float(self.coords[0]) - 2.5 * float(self.scale))
        if event.key() == Qt.Key_Right:
            if float(self.coords[0]) + 3 * float(self.scale) <= 180:
                self.coords[0] = str(float(self.coords[0]) + 2.5 * float(self.scale))
        if event.key() == Qt.Key_Up:
            if float(self.coords[1]) + 3 * float(self.scale) <= 90:
                self.coords[1] = str(float(self.coords[1]) + 2.5 * float(self.scale))
        if event.key() == Qt.Key_Down:
            if float(self.coords[1]) - 3 * float(self.scale) >= -90:
                self.coords[1] = str(float(self.coords[1]) - 2.5 * float(self.scale))
        self.update_image()

    def closeEvent(self, event):
        os.remove(self.map_file)


def get_coords(adress):
    request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + adress + "&format=json"
    response = requests.get(request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates.split()


def get_scale(adress):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": adress,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(geocoder_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    corner = toponym['boundedBy']['Envelope']
    lower_corner = list(map(float, corner['lowerCorner'].split()))
    upper_corner = list(map(float, corner['upperCorner'].split()))
    delta_x = abs(lower_corner[0] - upper_corner[0])
    delta_y = abs(lower_corner[1] - upper_corner[1])
    return str(max(delta_x, delta_y))


if __name__ == '__main__':
    coords = input('Введите координаты объекта через пробел: ').split()
    scale = input('Введите масштаб одним числом: ')
    app = QApplication(sys.argv)
    ex = Example(coords, scale)
    ex.show()
    sys.exit(app.exec())