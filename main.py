
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

    aspect  = img.height / img.width
    height  = int(width * aspect * 0.45)
    img     = img.resize((width, height))

    ramp    = RAMP_DETAILED if detailed else RAMP_SIMPLE
    gray    = img.convert("L")       
    rgb_img = img.convert("RGB")   

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input",           help="Path to the input image")
    parser.add_argument("-W", "--width",   type=int, default=100,
                        help="Output width in characters (default: 100)")
    parser.add_argument("-o", "--output",  default=None,
                        help="Save output to this .txt file instead of printing")
    parser.add_argument("--simple",        action="store_true",
                        help="Use a simple 10-character ramp instead of the detailed 70-char one")
    parser.add_argument("--invert",        action="store_true",
                        help="Invert brightness (good for dark terminal backgrounds)")
    parser.add_argument("--color",         action="store_true",
                        help="Print with ANSI true-colour codes (terminal only, not saved)")
    return parser.parse_args()


def main() -> None:
    args   = parse_args()
    source = Path(args.input)

    if not source.exists():
        sys.exit(f"Error: file not found — {source}")

    print(f"Converting '{source.name}'  (width={args.width}) …")

    ascii_art = image_to_ascii(
        image_path = str(source),
        width      = args.width,
        detailed   = not args.simple,
        invert     = args.invert,
        color      = args.color and args.output is None,
    )

    if args.output:
        out = Path(args.output)
        out.write_text(ascii_art, encoding="utf-8")
        print(f"Saved to '{out}'")
    else:
        print(ascii_art)


if __name__ == "__main__":
    main()
