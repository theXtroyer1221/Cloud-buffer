from PIL import Image, ImageOps
import secrets
import os


def save_picture(form_picture):
    im = Image.open(form_picture)
    old_size = im.size
    desired_size = 125
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    delta_w = desired_size - new_size[0]
    delta_h = desired_size - new_size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2),
               delta_h - (delta_h // 2))
    new_im = ImageOps.expand(im, padding)

    new_im.save("minecraft.png")


save_picture("cloudBuffer/static/profile_pics/872c8a20318ea3a9.png")