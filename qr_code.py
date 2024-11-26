from Data.constants import *

from kandinsky import fill_rect


class QrCode:
    def __init__(self, string: str):
        """A simple implementation of a QR-Code in a 2D matrice"""
        self.string = string
        self.level_correction: bytes = M
        self.version: int = self.find_best_version()
        self.size: int = size(self.version)
        self.array: list[list] = QrCode.fill(self.version, 0)

        self.init_matrice() # to draw simple pattern in the matrice of the QR-Code

    @staticmethod
    def fill(version: int = VERSION_1, fill: int = 0) -> list[list]:
        _size = size(version)
        return [[fill for _ in range(_size)] for _ in range(_size)]

    @staticmethod
    def check_data_type(string: str) -> bytes:
        if string.isdigit():
            return TYPE_1
        elif all(letter in CHAR_TYPE_2 for letter in string):
            return TYPE_2
        elif all(ord(letter) <= 255 for letter in string):
            return TYPE_3
        else:
            return TYPE_4

    def apply_positioning(self, x: int = 0, y: int = 0) -> list[list]:
        for _x in range(1, 6):
            self.array[x + _x][y] = 1
            self.array[x + _x][y + 6] = 1
        for _y in range(7):
            self.array[x][y + _y] = 1
            self.array[x + 6][y + _y] = 1

        for _y in range(3):
            for _x in range(3):
                self.array[x + 2 + _x][y + 2 + _y] = 1

    def apply_alternance_band(self, x0: int, y0: int, x1: int, y1: 0):
        if y1 == y0:
            for x in range(x0, x1):
                self.array[x][y0] = 1 if not x%2 else 0
        elif y1 > y0:
            for y in range(y0, y1):
                self.array[x0][y] = 1 if not y%2 else 0

    def init_matrice(self):
        length_espacement: int = size(self.version) - 16

        self.apply_positioning(0, 0)
        self.apply_positioning(9 + length_espacement, 0)
        self.apply_positioning(0, 9 + length_espacement)

        self.apply_alternance_band(8, 6, 13, 6)
        self.apply_alternance_band(6, 8, 6, 13)

        self.array[8][13] = 1

        infos: list[]
        self.apply_infos()

    def find_best_version(self) -> bytes:
        data_type: bytes = QrCode.check_data_type(self.string)

        return VERSION_1

    def draw(self, pos_x: int = 65, pos_y: int = 20, thickness: int = 8, spacing: int = 0):
        for x, y in [(x, y) for y in range(self.size) for x in range(self.size)]:
            color: tuple[int, int, int] = (0, 0, 0) if self.array[x][y] == 1 else "1"#(200, 200, 200)
            fill_rect(pos_x + x * (thickness + spacing), pos_y + y * (thickness + spacing), thickness, thickness, color)

if __name__ == '__main__':
    qr = QrCode("")
    qr.draw(spacing=0)