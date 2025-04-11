from PIL import Image


def compress_image(path, extension, max_size=(200, 200)):
    image = Image.open(path)
    print(image.size)
    image.thumbnail(max_size)
    image.save(path, quality=85, format=extension)
    print(image.size)
