
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Run: pip install Pillow")
    
    
RAMP_DETAILED = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
RAMP_SIMPLE = "@%#*+=-:. "

def pixel_to_char(brightness: int, ramp: str, invert: bool) -> str:
    if invert:
        brightness = 255 - brightness
    index = int((brightness / 255) * (len(ramp) - 1))
    return ramp[index]

def image_to_ascii(
    image_path: str,
    width: int = 100,
    detailed: bool = True,
    invert: bool = False,
    color: bool = False
) -> str:
    

    