import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


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
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            print(self.coords)
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
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


if __name__ == '__main__':
    coords = input('Введите координаты объекта через пробел: ').split()
    scale = input('Введите масштаб одним числом: ')
    app = QApplication(sys.argv)
    ex = Example(coords, scale)
    ex.show()
    sys.exit(app.exec())