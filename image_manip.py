from PIL import Image
import math


def grid(imgs: list, cols: int = None, rows: int = None):
    if rows is None:
        rows = math.ceil(len(imgs) / cols)
    elif cols is None or rows == 1:
        cols = math.ceil(len(imgs) / rows)
    img_w, img_h = (0, 0)
    for img in imgs:
        if img.size[0] * img.size[1] >= img_w * img_h:
            img_w, img_h = imgs[0].size
    background = Image.new("RGBA", (img_w * cols, img_h * rows), (255, 255, 255, 255))
    i = 1
    while i <= len(imgs):
        img = imgs[i-1].resize(size=(img_w, img_h))
        col = i % cols
        if col == 0:
            col = cols
            row = math.floor(i / col)
        else:
            row = math.floor(i / cols) + 1
        horiz_offset = (col - 1) * img_w
        vert_offset = (row - 1) * img_h
        offset = (horiz_offset, vert_offset)
        background.paste(im=img, box=offset)
        i = i + 1
    return background
