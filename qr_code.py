"""
Quick Response generator : QR-Code

A projetct construct with a group in NSI. The first step is to easly create
a QR-Code of version 1 (21x21) from an hyperlien (with a short length) and
to export it in a .png picture.

This script also provide some tools to read a QR-Code with the camera, and open the
webroser to see the site.

See the Jupiter Notebook for see some examples.

Thanks for all contributors
"""

from Data.constants import *

from kandinsky import fill_rect

from numpy import zeros, array, ndarray


class QrCode:
    def __init__(self, string: str = "",
                 box_color: str | tuple = (0, 0, 0), pattern_color: str | tuple = (0, 0, 0),
                 level_correction: str = M,
                 mask_pattern: str = MASK_PATTERN_4
                 ):
        """A simple implementation of a QR-Code in a 2D matrice"""
        self.string = string
        self.level_correction: str = level_correction
        self.mask_pattern: str = mask_pattern
        self.version: int = self.find_best_version()
        self.size: int = size(self.version)

        self.box_color: str | tuple = box_color
        self.pattern_color: str | tuple = pattern_color

        self.array: ndarray = array(QrCode.fill(self.version, 0))

        self.init_matrice() # to draw simple pattern in the matrice of the QR-Code

    def __str__(self) -> str:
        return str(self.array)

    __repr__ = __str__

    @staticmethod
    def fill(version: int = VERSION_1, fill: int = 0) -> list[list]:
        _size = size(version)
        return [[fill for _ in range(_size)] for _ in range(_size)]

    @staticmethod
    def check_data_type(string: str) -> str:
        if string.isdigit():
            return TYPE_1
        elif all(letter in CHAR_TYPE_2 for letter in string):
            return TYPE_2
        elif all(ord(letter) <= 255 for letter in string):
            return TYPE_3
        else:
            return TYPE_4

    def apply_positioning(self, x: int = 0, y: int = 0):
        for _x in range(1, 6):
            self.array[y][x + _x] = 2
            self.array[y + 6][x + _x] = 2
        for _y in range(7):
            self.array[y + _y][x] = 2
            self.array[y + _y][x + 6] = 2

        for _y in range(3):
            for _x in range(3):
                self.array[y + 2 + _y][x + 2 + _x] = 2

    def apply_alternance_band(self, x0: int, y0: int, x1: int, y1: int):
        if y1 == y0:
            for x in range(x0, x1):
                self.array[y0][x] = 1 if not x%2 else 0
        elif x1 == x0:
            for y in range(y0, y1):
                self.array[y][x0] = 1 if not y%2 else 0

    def get_infos(self) -> list[int]:
        list_infos: list[str] = [self.level_correction, self.mask_pattern]
        format_information: list[int] = []

        for info in list_infos:
            format_information.extend([int(nbr) for nbr in list(info)])

        if len(format_information) != self.version:
            format_information.extend([0 for _ in range(15 - len(format_information))])

        return format_information

    def apply_infos(self, x0: int, y0: int, x1: int, y1: int):
        format_information: list[int] = self.get_infos()

        if y1 == y0:
            format_information = format_information[:6] + [-1, format_information[6]] + [-1 for _ in range(5)] + format_information[7:]

            for x in range(self.size):
                self.array[y0][x] = format_information[x] if format_information[x] != -1 else self.array[x][y0]

        elif x1 == x0:
            format_information = format_information[:7] + [-1 for _ in range(5)] + format_information[7:9] + [-1] + format_information[9:]

            for y in range(self.size):
                self.array[-y-1][x0] = format_information[y] if format_information[y] != -1 else self.array[x0][-y-1]

    def init_matrice(self):
        length_espacement: int = self.size - 16

        self.apply_positioning(0, 0)
        self.apply_positioning(9 + length_espacement, 0)
        self.apply_positioning(0, 9 + length_espacement)

        self.apply_alternance_band(8, 6, 13, 6)
        self.apply_alternance_band(6, 8, 6, 13)

        self.array[13][8] = 1

        self.apply_infos(0, 8, 21, 8)
        self.apply_infos(8, 21, 8, 0)

    def find_best_version(self) -> int:
        data_type: int = QrCode.check_data_type(self.string)

        return VERSION_1

    def draw(self, pos_x: int = 65, pos_y: int = 20, thickness: int = 8, spacing: int = 0):
        for x, y in [(x, y) for y in range(self.size) for x in range(self.size)]:
            if self.array[y][x] == 0: color = (200, 200, 200)
            elif self.array[y][x] == 1: color = self.box_color
            elif self.array[y][x] == 2: color = self.pattern_color
            else: color = (255, 255, 255)

            fill_rect(pos_x + x * (thickness + spacing), pos_y + y * (thickness + spacing), thickness, thickness, color)

if __name__ == '__main__':
    qr = QrCode("")
    qr.draw(spacing=1)