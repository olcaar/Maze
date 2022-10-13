import os
from pathlib import Path

from PIL import Image

img = Image.open("graphics/Animations/Human/Minifantasy_CreaturesHumanBaseWalk.png")


def cut_into_images(image, new_width, new_height):
    directory = Path(image.filename).stem
    sprites = []
    for j in range(0, 4):
        for i in range(0, 4):
            sprites.append(image.crop((i * 32, j * 32, i * 32 + 32, j * 32 + 32)))

    images = []
    for image in sprites:
        width, height = image.size  # Get dimensions

        left = (width - new_width) / 2 - 1
        top = (height - new_height) / 2 - 1
        right = (width + new_width) / 2 + 1
        bottom = (height + new_height) / 2 + 1

        images.append(image.crop((left, top, right, bottom)))

    # create directory with name of the image
    os.mkdir(directory)
    # save images to directory
    for i, image in enumerate(images):
        image.save(f'{directory}/{directory}_{i}.png')


cut_into_images(img, 8, 8)
