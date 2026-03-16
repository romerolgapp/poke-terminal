from PIL import Image
import sys
import time

UPPER_BLOCK = "▀"

def rgb_fg(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"

def rgb_bg(r, g, b):
    return f"\x1b[48;2;{r};{g};{b}m"

def reset():
    return "\x1b[0m"

def move_cursor(row=1, col=1):
    return f"\x1b[{row};{col}H"

def hide_cursor():
    return "\x1b[?25l"

def show_cursor():
    return "\x1b[?25h"

def clear_screen():
    return "\x1b[2J"

def split_two_frames_horizontal(image_path):
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    half_w = w // 2
    frame1 = img.crop((0, 0, half_w, h))
    frame2 = img.crop((half_w, 0, w, h))
    return [frame1, frame2]

def rgba_to_rgb_on_black(pixel):
    r, g, b, a = pixel
    if a == 255:
        return (r, g, b)
    # Mezcla simple sobre fondo negro
    r2 = int(r * a / 255)
    g2 = int(g * a / 255)
    b2 = int(b * a / 255)
    return (r2, g2, b2)

def frame_to_ansi(img):
    img = img.convert("RGBA")
    w, h = img.size
    lines = []

    # recorremos de 2 en 2 filas porque un carácter representa 2 píxeles verticales
    for y in range(0, h, 2):
        line = []
        for x in range(w):
            top = img.getpixel((x, y))
            if y + 1 < h:
                bottom = img.getpixel((x, y + 1))
            else:
                bottom = (0, 0, 0, 255)

            tr, tg, tb = rgba_to_rgb_on_black(top)
            br, bg, bb = rgba_to_rgb_on_black(bottom)

            line.append(
                f"{rgb_fg(tr, tg, tb)}{rgb_bg(br, bg, bb)}{UPPER_BLOCK}"
            )
        line.append(reset())
        lines.append("".join(line))

    return "\n".join(lines)

def animate(frames, fps=4, row=1, col=1, loops=0):
    ansi_frames = [frame_to_ansi(f) for f in frames]
    delay = 1.0 / fps

    sys.stdout.write(hide_cursor())
    sys.stdout.write(clear_screen())
    sys.stdout.flush()

    try:
        count = 0
        while True:
            for frame in ansi_frames:
                sys.stdout.write(move_cursor(row, col))
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(delay)

            if loops > 0:
                count += 1
                if count >= loops:
                    break
    finally:
        sys.stdout.write(reset())
        sys.stdout.write(show_cursor())
        sys.stdout.write("\n")
        sys.stdout.flush()

if __name__ == "__main__":
    ruta = "/home/lgromero/Descargas/scream_tail/Sleep-Anim.png"
    frames = split_two_frames_horizontal(ruta)
    animate(frames, fps=3, row=2, col=5)