"""
Misc helper functions.
"""
import json
import os
import shutil
import subprocess


class Color:
    """Color formats."""
    alpha_num = 100

    def __init__(self, hex_color):
        self.hex_color = hex_color

    def __str__(self):
        return self.hex_color

    @property
    def rgb(self):
        """Convert a hex color to rgb."""
        red, green, blue = hex_to_rgb(self.hex_color)
        return "%s,%s,%s" % (red, green, blue)

    @property
    def xrgba(self):
        """Convert a hex color to xrdb rgba."""
        return hex_to_xrgba(self.hex_color)

    @property
    def alpha(self):
        """Add URxvt alpha value to color."""
        return "[%s]%s" % (self.alpha_num, self.hex_color)


def read_file(input_file):
    """Read data from a file and trim newlines."""
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def read_file_json(input_file):
    """Read data from a json file."""
    with open(input_file, "r") as json_file:
        data = json.load(json_file)

    return data


def read_file_raw(input_file):
    """Read data from a file as is, don't strip
       newlines or other special characters.."""
    with open(input_file, "r") as file:
        data = file.readlines()
    return data


def save_file(data, export_file):
    """Write data to a file."""
    create_dir(os.path.dirname(export_file))

    try:
        with open(export_file, "w") as file:
            file.write(data)
    except PermissionError:
        print("warning: Couldn't write to %s." % export_file)


def save_file_json(data, export_file):
    """Write data to a json file."""
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def create_dir(directory):
    """Alias to create the cache dir."""
    os.makedirs(directory, exist_ok=True)


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    return tuple(bytes.fromhex(color.strip("#")))


def hex_to_xrgba(color):
    """Convert a hex color to xrdb rgba."""
    col = color.lower().strip("#")
    return "%s%s/%s%s/%s%s/ff" % (*col,)


def rgb_to_hex(color):
    """Convert an rgb color to hex."""
    return "#%02x%02x%02x" % (*color,)


def darken_color(color, amount):
    """Darken a hex color."""
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten_color(color, amount):
    """Lighten a hex color."""
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def disown(cmd):
    """Call a system command in the background,
       disown it and hide it's output."""
    subprocess.Popen(cmd,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


def msg(input_msg, notify):
    """Print to the terminal and display a libnotify
       notification."""
    if notify and shutil.which("notify"):
        disown(["notify-send", input_msg])

    print(input_msg)
