"""This file contains useful constants for Qr-Code parameters"""

from pathlib import Path

import json
import os


def load_json(path: str) -> dict:
    """A function to load data in a json file.

    Args:
        path (str): The relative path of the file.

    Returns:
        dict: Return a dict wich contains data.
    """
    name: str = os.path.split(path)[1]

    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


DIR_DATA: Path = Path(os.path.dirname(__file__))
VERSION_CAPACITIES: dict = load_json(DIR_DATA / "version_capacities.json")

# A lambda function to determinate the size of the QR-Code with the number of the version
size = lambda version: 4 * version + 17

# Constants to define the level of error correction
L = "00" # 7%
M = "01" # 15% (by default)
Q = "10" # 25%
H = "11" # 30%

# Constants to define the data type
TYPE_1 = "0001" # Numbers only: numeric (decimal digits from 0 to 9)
TYPE_2 = "0010" # Letters and numbers: alphanumeric (decimal digits from 0 to 9, 
                # and upper-case letters (not lower-case!), 
                # and the symbols $, %, *, +, -, ., /, and : as well as a space)
TYPE_3 = "0100" # Text coded in 8-bit values (ISO-8859-1 character set)
TYPE_4 = "1000" # Japanese kanji ideogram (JIS Shift pose character)

CHAR_TYPE_1 = "0123456789" # all symbols authorized for type 1
CHAR_TYPE_2 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:" # all symbols authorized for type 2

# Constants to define the mask pattern
MASK_PATTERN_0 = "000"
MASK_PATTERN_1 = "001"
MASK_PATTERN_2 = "010"
MASK_PATTERN_3 = "011"
MASK_PATTERN_4 = "100" # by default
MASK_PATTERN_5 = "101"
MASK_PATTERN_6 = "110"
MASK_PATTERN_7 = "111"

# Constants to define QR-Code size
VERSION_1 = 1 # by default
VERSION_2 = 2
VERSION_3 = 3
VERSION_4 = 4
VERSION_5 = 5
VERSION_6 = 6
VERSION_7 = 7
VERSION_8 = 8
VERSION_9 = 9
VERSION_10 = 10
VERSION_11 = 11
VERSION_12 = 12
VERSION_13 = 13
VERSION_14 = 14
VERSION_15 = 15
VERSION_16 = 16
VERSION_17 = 17
VERSION_18 = 18
VERSION_19 = 19
VERSION_20 = 20
VERSION_21 = 21
VERSION_22 = 22
VERSION_23 = 23
VERSION_24 = 24
VERSION_25 = 25
VERSION_26 = 26
VERSION_27 = 27
VERSION_28 = 28
VERSION_29 = 29
VERSION_30 = 30
VERSION_31 = 31
VERSION_32 = 32
VERSION_33 = 33
VERSION_34 = 34
VERSION_35 = 35
VERSION_36 = 36
VERSION_37 = 37
VERSION_38 = 38
VERSION_39 = 39
VERSION_40 = 40
