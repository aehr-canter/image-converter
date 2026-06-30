
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
    """
    Convert an image file to an ASCII-art string.

    Parameters
    ----------
    image_path : str
        Path to the source image (JPEG, PNG, GIF, BMP, WEBP, …).
    width : int
        Number of characters per row (default 100).
    detailed : bool
        Use the 70-char detailed ramp; False → simple 10-char ramp.
    invert : bool
        Invert brightness mapping (useful for dark-background terminals).
    color : bool
        Wrap each character in ANSI 256-colour escape codes.

    Returns
    -------
    str
        The full ASCII-art string, ready to print or save.
    """
    img = Image.open(image_path)

    # Preserve aspect ratio.  Terminal characters are ~2× taller than wide,
    # so we scale height by 0.45 to avoid a vertically stretched result.
    aspect  = img.height / img.width
    height  = int(width * aspect * 0.45)
    img     = img.resize((width, height))

    ramp    = RAMP_DETAILED if detailed else RAMP_SIMPLE
    gray    = img.convert("L")          # grayscale copy for brightness
    rgb_img = img.convert("RGB")        # RGB copy for optional colouring

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            brightness      = gray.getpixel((x, y))
            char            = pixel_to_char(brightness, ramp, invert)

            if color:
                r, g, b     = rgb_img.getpixel((x, y))
                # ANSI 24-bit true-colour escape
                char        = f"\033[38;2;{r};{g};{b}m{char}\033[0m"

            row.append(char)
        lines.append("".join(row))

    return "\n".join(lines)

