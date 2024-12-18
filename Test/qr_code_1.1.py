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

from itertools import cycle

from numpy import array, ndarray


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
        self.data_type: str = QrCode.check_data_type(self.string)
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

    def find_best_version(self) -> int:
        return VERSION_1 # for the moment

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

    def check_length_string(self) -> int:
        data_type = int(self.data_type, base=2)

        if self.version <= 9:
            match data_type:
                case 1: return 10
                case 2: return 9
                case 4: return 8
                case 8: return 8

        elif 10 <= self.version <= 26:
            match data_type:
                case 1: return 12
                case 2: return 11
                case 4: return 16
                case 8: return 10

        elif 27 <= self.version <= 40:
            match data_type:
                case 1: return 14
                case 2: return 13
                case 4: return 16
                case 8: return 12

    def get_length_string(self) -> list[int]:
        length: int = self.check_length_string()
        length_string: list[int] = [int(nbr) for nbr in list(bin(len(self.string))[2:].rjust(length, '0'))]
        return length_string

    def convert_string(self) -> list[int]:
        if self.data_type != TYPE_3:
            raise NotImplementedError("For the moment, just the encoding of octet type is available.")

        list_bin: list[int] = []

        for char in self.string:
            binary: list[int] = list(bin(ord(char))[2:].rjust(8, '0'))
            list_bin.extend([int(nbr) for nbr in binary])

        return list_bin

    def get_total_nbr_bits(self) -> int:
        return 128 # for the moment

    def get_encoding_string(self) -> list[int]:
        data_type: list[int] = [int(nbr) for nbr in self.data_type]
        length_string: list[int] = self.get_length_string()
        convert_string: list[int] = self.convert_string()

        encoding_bits: list[int] = data_type + length_string + convert_string
        total_nbr_bits: int = self.get_total_nbr_bits()

        if len(encoding_bits) > total_nbr_bits:
            raise NotImplementedError("For the moment, just the version 1 is available.")

        elif len(encoding_bits) < total_nbr_bits:
            delta: int = total_nbr_bits - len(encoding_bits)

            if delta <= 4:
                encoding_bits.extend([0 for _ in range(delta)])

            elif delta > 4:
                encoding_bits.extend([0 for _ in range(4)])

                length_to_8_multiple: int = 8 - (len(encoding_bits)%8)
                encoding_bits.extend([0 for _ in range(length_to_8_multiple)])

                delta: int = total_nbr_bits - len(encoding_bits)

                if len(encoding_bits) > total_nbr_bits:
                    for _ in range(abs(delta)):
                        encoding_bits.pop()

                else:
                    pad: cycle = cycle(["11101100", "00010001"])
                    nbr_pad = int(delta / 8)

                    for _ in range(nbr_pad):
                        encoding_bits.extend([int(nbr) for nbr in next(pad)])

        return encoding_bits

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

    def draw(self, pos_x: int = 65, pos_y: int = 20, thickness: int = 8, spacing: int = 0):
        for x, y in [(x, y) for y in range(self.size) for x in range(self.size)]:
            if self.array[y][x] == 0: color = (200, 200, 200)
            elif self.array[y][x] == 1: color = self.box_color
            elif self.array[y][x] == 2: color = self.pattern_color
            else: color = (255, 255, 255)

            fill_rect(pos_x + x * (thickness + spacing), pos_y + y * (thickness + spacing), thickness, thickness, color)

if __name__ == '__main__':
    qr = QrCode("Hello, word!")
    qr.draw(spacing=1)