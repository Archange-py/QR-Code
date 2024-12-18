"""
Quick Response generator : QR-Code

A projetct construct with a group in NSI. The first step is to easly create
a QR-Code of version 1 (21x21) from an hyperlien (with a short length) and
to export it in a .png picture.

This script also provide some tools to read a QR-Code from a given picture,
and decode encoded data.

See the Jupiter Notebook for see some examples.

Thanks for all contributors (see the GitHub)
"""

from Data.constants import *

from kandinsky import fill_rect

from itertools import cycle

from qrcode import QRCode, ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

from pathlib import Path

from os.path import dirname, join
from os import chdir

import numpy as np

from pyzbar.pyzbar import decode
import cv2


# Main functions

def make_qr(link: str = "https://github.com/Archange-py",
            save_path: str = join(Path.home(), "Images/qr_code.png"),
            qr_version: int = VERSION_1, qr_correction: str = M, qr_size: int = 10,
            color: str = "black", bg_color: str = "white"):
    """A function that create a .png picture from specific data with the qr_code library.

    Args:
        link (str, optional): The data that you want encode. Defaults to "https://github.com/Archange-py".
        save_path (str, optional): The absolute path of the picture. Defaults to join(Path.home(), "Images/qr_code.png").
        qr_version (int, optional): A constant that represent the version of the QR code. Defaults to VERSION_1.
        qr_correction (str, optional): A constant that represent the level correction: L, M, Q, H. Defaults to M.
        qr_size (int, optional): The size of one module. Defaults to 10.
        color (str, optional): The color of modules. Defaults to "black".
        bg_color (str, optional): The background color. Defaults to "white".
    """

    # Replace with library constants
    if qr_correction == L: qr_correction = ERROR_CORRECT_L
    elif qr_correction == M: qr_correction = ERROR_CORRECT_M
    elif qr_correction == Q: qr_correction = ERROR_CORRECT_Q
    elif qr_correction == H: qr_correction = ERROR_CORRECT_H

    # Create the QR code object
    qr = QRCode(version=qr_version, error_correction=qr_correction, box_size=qr_size, border=4)
    qr.add_data(link)
    qr.make(fit=True)

    chdir(dirname(save_path)) # change the directory

    # Save the picture into the directory
    img = qr.make_image(fill_color=color, back_color=bg_color)

    save_img_list = save_path.split("\\") # split the path to to obtain the name of the picture
    img.save(save_img_list[-1])

def recognize_qr(path: str = None, webcam: bool = False, time: int = 100) -> None | str:
    """A function that decode some QR code with the camera,
    or decode with a specific picture.

    Args:
        path (str, optionnal): The absolute path of your picture. Defaults to None.
        webcam (bool, optionnal): The boolean to activate the video flux. Defaults to False.
        time (int, optionnal): The limit time to decode the data with the camera. Defaults to 100.

    Returns:
        None | str: Return the decoded data, or just show the video flux.
    """
    if webcam == False:

        img = cv2.imread(path)  # image avec le QRcode qu'on veut décoder
        for barcode in decode(img):     # boucle qui décode les info de l'image
            message = barcode.data.decode('utf-8')  # variable qui contien le message décodé de type str
        return message  # affichage du message décodé

    elif webcam == True:

        video = cv2.VideoCapture(0) # variable qui contien les capture de la video (webcam en question)
        video.set(3,640) # atribution de la largeur (width) de la fenetre qui montrera la webcam
        video.set(4, 480) # atribution de la hauteur (height) de la fenetre qui montrera la webcam

        n = 0

        while n != time: # boucle qui met à jour les information obtenu de la webcam
            success, img = video.read() # lecture des info de la webcam
            for barcode in decode(img): # boucle qui décode les info obtenu de la webcam
                message = barcode.data.decode('utf-8') # variable qui contien le message décodé de type str
                points = np.array([barcode.polygon],np.int32) # creation des point pour un polygone
                points = points.reshape((-1,1,2))
                points2 = barcode.rect  # variable qui contient les points a chaque coins du QRcode
                cv2.polylines(img,[points],True,(0,255,0),5) # affichage des lignes qui entoure le QRcode trouvé
                cv2.putText(img,message,(points2[0],points2[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2) # affichage du message décodé dans la fenetre
            cv2.imshow('Result', img) # affichage de la fenetre de ce que voit la webcam
            cv2.waitKey(1) # 1ms d'attente

            n += 1

        cv2.destroyWindow('Result')

# Secondary functions

def fill(version: int = VERSION_1, fill: int = 0) -> list[list]:
    """A simple function that create a 2D list fill with an item.

    Args:
        version (int, optional): The version of the QR code, uses to determinate the size. Defaults to VERSION_1.
        fill (int, optional): The item. Defaults to 0.

    Returns:
        list[list]: Return a 2D list filled with the item argument.
    """
    _size = size(version)
    return [[fill for _ in range(_size)] for _ in range(_size)]

def check_data_type(string: str) -> str:
    """A simple function that recognized the type of the string.

    Args:
        string (str): The data that you want to encode.

    Returns:
        str: Return the constant that precize the specific type: TYPE_1, TYPE_2, TYPE_3, TYPE_4.
    """
    if string.isdigit():
        return TYPE_1
    elif all(letter in CHAR_TYPE_2 for letter in string):
        return TYPE_2
    elif all(ord(letter) <= 255 for letter in string):
        return TYPE_3
    else:
        return TYPE_4

def find_best_version(string: str, *_) -> int:
    """A function to determinate with the length of the encoding data
    the version of the QR code.

    Args:
        string (str): The data that you want to encode.

    Returns:
        int: Return the constant that precize the specific version: VERSION_1, ..., VERSION_40.
    """
    return VERSION_1 # just for the moment, in according with the specifications

def apply_positioning(array: list[list], x: int = 0, y: int = 0) -> list[list]:
    """A function that apply positionning pattern from an x,y position on the array.

    Args:
        array (list[list]): An array that represent the QR code.
        x (int, optional): The x position in the up left. Defaults to 0.
        y (int, optional): The y postion in the up left. Defaults to 0.

    Returns:
        list: The array that has been modified.
    """
    for _x in range(1, 6):
        array[y][x + _x] = 2
        array[y + 6][x + _x] = 2

    for _y in range(7):
        array[y + _y][x] = 2
        array[y + _y][x + 6] = 2

    for _y in range(3):
        for _x in range(3):
            array[y + 2 + _y][x + 2 + _x] = 2

    return array

def apply_alternance_band(array: list[list], x0: int, y0: int, x1: int, y1: int) -> list[list]:
    """A function that apply alternance band from an x0, y0 position to an x1, y1 point on the array.

    Args:
        array (list[list]): An array that represent the QR code.
        x0 (int): The x0 position.
        y0 (int): The y0 position.
        x1 (int): The x1 position.
        y1 (int): The y1 position.

    Returns:
        list[list]: The array that has been modified.
    """
    if y1 == y0:
        for x in range(x0, x1):
            array[y0][x] = 1 if not x%2 else 0

    elif x1 == x0:
        for y in range(y0, y1):
            array[y][x0] = 1 if not y%2 else 0

    return array

def get_infos(array: list[list], level_correction: str = M, mask_pattern: str = MASK_PATTERN_4) -> list[int]:
    """A function that return a list with the format information.

    Args:
        array (list[list]): An array that represent the QR code.
        level_correction (str, optional): A constant that represent the level correction:
                                          L, M, Q, H. Defaults to M
        mask_pattern (str, optional): A constant tha represent the mask pattern: 
                                      MASK_PATTERN_0, ..., MASK_PATTERN_7. Default to MASK_PATTERN_4

    Returns:
        list[int]: A list of 0 and 1 to indicate the format information.
    """
    list_infos: list[str] = [level_correction, mask_pattern]
    format_information: list[int] = []

    for info in list_infos:
        format_information.extend([int(nbr) for nbr in list(info)])

    if len(format_information) != find_best_version(array):
        format_information.extend([0 for _ in range(15 - len(format_information))])

    return format_information

def apply_infos(array: list[list], format_information: list[int], x0: int, y0: int, x1: int, y1: int) -> list[list]:
    """A function that apply format information from an x0, y0 position
    to an x1, y1 horizontal or vertical point on the array.

    Args:
        array (list[list]): An array that represent the QR code.
        format_information (list[int]): The list with the format information.
        x0 (int): The x0 position.
        y0 (int): The y0 position.
        x1 (int): The x1 position.
        y1 (int): The y1 position.

    Returns:
        list[list]: The array that has been modified.
    """
    size: int = len(array[0])

    if y1 == y0:
        format_information = format_information[:6] + [-1, format_information[6]] + [-1 for _ in range(5)] + format_information[7:]

        for x in range(size):
            array[y0][x] = format_information[x] if format_information[x] != -1 else array[x][y0]

    elif x1 == x0:
        format_information = format_information[:7] + [-1 for _ in range(5)] + format_information[7:9] + [-1] + format_information[9:]

        for y in range(size):
            array[-y-1][x0] = format_information[y] if format_information[y] != -1 else array[x0][-y-1]

    return array

def check_length_string(version: int = VERSION_1, data_type: str = TYPE_3) -> int:
    """A simple function to obtain the size of the character count indicators
    for each mode and version.

    Args:
        version (int, optional): A constant that represent the version of your Qr code. Defaults to 1.
        data_type (str, optional): A constant that represent the data type encoded into your Qr code. Defaults to TYPE_3.

    Returns:
        int: Return the length that the character count indicator must has.
    """
    data_type = int(data_type, base=2)

    if version <= 9:
        match data_type:
            case 1: return 10
            case 2: return 9
            case 4: return 8
            case 8: return 8

    elif 10 <= version <= 26:
        match data_type:
            case 1: return 12
            case 2: return 11
            case 4: return 16
            case 8: return 10

    elif 27 <= version <= 40:
        match data_type:
            case 1: return 14
            case 2: return 13
            case 4: return 16
            case 8: return 12

def get_length_string(string: str) -> list[int]:
    """A function to get the length information of the encoded data.

    Args:
        string (str): The data that you want to encode.

    Returns:
        list[int]: Return a list of 0 or 1 to indicate the length od the data.
    """
    length: int = check_length_string()
    length_string: list[int] = [int(nbr) for nbr in list(bin(len(string))[2:].rjust(length, '0'))]

    return length_string

def convert_string(string: str) -> list[int]:
    """A function to convert a string into binary encoding. For the moment,
    it's just available for the text coded in 8-bit values (ISO-8859-1 character set).

    Args:
        string (str): The data that you want to encode.

    Returns:
        list[int]: Return a list of 0 or 1 to indicate the binary encoding of the data.
    """
    list_bin: list[int] = []

    for char in string:
        binary: list[int] = list(bin(ord(char))[2:].rjust(8, '0'))
        list_bin.extend([int(nbr) for nbr in binary])

    return list_bin

def get_total_nbr_bits(string: str, *_) -> int:
    """A function to determinate the total number of bits that you
    can encoding in a QR code. For the moment, it return a number
    according of the version 1 and a text coded in 8-bit values.

    Args:
        string (str): The data that you want to encode.

    Returns:
        int: Return the total number of bits that you can encoding.
    """
    return 128 # just for the moment

def get_encoding_string(string: str) -> list[int]:
    """The algorithm uses to obtain the final chain of the encoding
    data, then we have just to push it in the QR code array with a
    specific pattern.

    Args:
        string (str): The data that you want to encode.

    Raises:
        NotImplementedError: Raise an error if the length of the encoded
        data is greater than the limit of the version 1.

    Returns:
        list[int]: Return a list of 0 or 1 to indicate the final binary encoding of the data.
    """
    data_type: list[int] = [int(nbr) for nbr in check_data_type(string)]
    length_string: list[int] = get_length_string(string)
    converted_string: list[int] = convert_string(string)

    encoding_bits: list[int] = data_type + length_string + converted_string
    total_nbr_bits: int = get_total_nbr_bits(string)

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

def init_matrice(array: list[list], string: str) -> list[list]:
    """A function to place different initial patterns into the array.

    Args:
        array (list[list]): An array that represent the QR code.
        string (str): The data that you want to encode.

    Returns:
        list: Return the update array.
    """
    length_espacement: int = size(find_best_version(string)) - 16

    array = apply_positioning(array, 0, 0)
    array = apply_positioning(array, 9 + length_espacement, 0)
    array = apply_positioning(array, 0, 9 + length_espacement)

    array = apply_alternance_band(array, 8, 6, 13, 6)
    array = apply_alternance_band(array, 6, 8, 6, 13)

    array[13][8] = 1

    array = apply_infos(array, get_infos(array), 0, 8, 21, 8)
    array = apply_infos(array, get_infos(array), 8, 21, 8, 0)

    return array

def draw(array: list[list], pos_x: int = 65, pos_y: int = 20, thickness: int = 8, spacing: int = 0, box_color: str | tuple = (0, 0, 0), pattern_color: str | tuple = (0, 0, 0)):
    """A function uses to draw the QR code with the represented array into a kandinsky window.

    Args:
        array (list[list]): An array that represent the QR code.
        pos_x (int, optional): The x position to start the drawing. Defaults to 65.
        pos_y (int, optional): The y position to start the drawing. Defaults to 20.
        thickness (int, optional): The size of different modules. Defaults to 8.
        spacing (int, optional): The space between different modules. Defaults to 0.
        box_color (str | tuple, optional): The color of different encoded modules. Defaults to (0, 0, 0).
        pattern_color (str | tuple, optional): The color of different static modules.. Defaults to (0, 0, 0).
    """
    size: int = len(array[0])

    for x, y in [(x, y) for y in range(size) for x in range(size)]:
        if array[y][x] == 0: color = (200, 200, 200)
        elif array[y][x] == 1: color = box_color
        elif array[y][x] == 2: color = pattern_color
        else: color = (255, 255, 255)

        fill_rect(pos_x + x * (thickness + spacing), pos_y + y * (thickness + spacing), thickness, thickness, color)
