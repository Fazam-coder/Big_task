import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, coords, scale):
        super().__init__()
        self.getImage(coords, scale)
        self.initUI()

    def getImage(self, coords, scale):
        map_request = "http://static-maps.yandex.ru/1.x/"
        map_view = "map"
        map_params = {"ll": ",".join(coords),
                      "spn": ",".join([scale, scale]),
                      "l": map_view}
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
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

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    coords = input('Введите координаты объекта через пробел: ').split()
    scale = input('Введите масштаб одним числом: ')
    app = QApplication(sys.argv)
    ex = Example(coords, scale)
    ex.show()
    sys.exit(app.exec())