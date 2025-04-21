from PIL import Image


def compress_image(path, extension, max_size=(1920, 1080)):
    image = Image.open(path)
    print(image.size)
    image.thumbnail(max_size)
    image.save(path, quality=85, format=extension)
    print(image.size)
