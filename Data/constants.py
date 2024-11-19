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


ROOT_DIR: Path = Path(os.path.dirname(__file__))
DIR_DATA: Path = ROOT_DIR / "data"

VERSION_CAPACITIES: dict = load_json(DIR_DATA + "version_capacities.json")


# Constants to define the level of error correction
L = bytes(0b00) # 7%
M = bytes(0b01) # 15% (by default)
Q = bytes(0b10) # 25%
H = bytes(0b11) # 30%

# Constants to define the data type
TYPE_1 = bytes(0b0001) # Numbers only: numeric (decimal digits from 0 to 9)
TYPE_2 = bytes(0b0010) # Letters and numbers: alphanumeric (decimal digits from 0 to 9, 
                # and upper-case letters (not lower-case!), 
                # and the symbols $, %, *, +, -, ., /, and : as well as a space)
TYPE_3 = bytes(0b0100) # Text coded in 8-bit values (ISO-8859-1 character set)
TYPE_4 = bytes(0b1000) # Japanese kanji ideogram (JIS Shift pose character)

CHAR_TYPE_1 = "0123456789" # all symbols authorized for type 1
CHAR_TYPE_2 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:" # all symbols authorized for type 2

# Constants to define the mask pattern
MASK_PATTERN_0 = bytes(0b000)
MASK_PATTERN_1 = bytes(0b001)
MASK_PATTERN_2 = bytes(0b010)
MASK_PATTERN_3 = bytes(0b011)
MASK_PATTERN_4 = bytes(0b100) # by default
MASK_PATTERN_5 = bytes(0b101)
MASK_PATTERN_6 = bytes(0b110)
MASK_PATTERN_7 = bytes(0b111)

# Constants to define QR-Code size
VERSION_1 = 21 # by default
VERSION_2 = 25
VERSION_3 = 29
VERSION_4 = 33
VERSION_5 = 37
VERSION_6 = 41
VERSION_7 = 45
VERSION_8 = 49
VERSION_9 = 53
VERSION_10 = 57
VERSION_11 = 61
VERSION_12 = 65
VERSION_13 = 69
VERSION_14 = 73
VERSION_15 = 77
VERSION_16 = 81
VERSION_17 = 85
VERSION_18 = 89
VERSION_19 = 93
VERSION_20 = 97
VERSION_21 = 101
VERSION_22 = 105
VERSION_23 = 109
VERSION_24 = 113
VERSION_25 = 117
VERSION_26 = 121
VERSION_27 = 125
VERSION_28 = 129
VERSION_29 = 133
VERSION_30 = 137
VERSION_31 = 141
VERSION_32 = 145
VERSION_33 = 149
VERSION_34 = 153
VERSION_35 = 157
VERSION_36 = 161
VERSION_37 = 165
VERSION_38 = 169
VERSION_39 = 173
VERSION_40 = 177
