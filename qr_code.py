from Data.constants import *

from kandinsky import fill_rect


class QrCode:
    def __init__(self, string: str, length: int = 21):
        self.length = length
        self.string = string
        self.array: list[list[0]] = QrCode.zeros(length, length)

    @staticmethod
    def zeros(length: int = 21, width: int = 21) -> list[list[0]]:
        return [[0 for _ in range(length)] for _ in range(width)]

    @staticmethod
    def positioning(x, array: list[list]) -> list[list]:
        

    @staticmethod
    def apply_positioning(array: list[list]):
        pass

    @staticmethod
    def apply_positioning(array: list[list]):
        pass

    @staticmethod
    def init_matrice(array: list[list]) -> list[list]:
        pass

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

    @staticmethod
    def find_best_version(string: str, level_correction: bytes = M) -> bytes:
        data_type: bytes = QrCode.check_data_type(string)
        



    def draw(self, pos_x: int = 65, pos_y: int = 20, thickness: int = 8, spacing: int = 0):
        for x, y in [(x, y) for y in range(self.length) for x in range(self.length)]:
            print(x, y)
            color: tuple[int, int, int] = (0, 0, 0) if self.array[x][y] == 1 else (200, 200, 200)
            fill_rect(pos_x + x * (thickness + spacing), pos_y + y * (thickness + spacing), thickness, thickness, color)

if __name__ == '__main__':
    qr = QrCode("")
    #qr.draw(spacing=1)