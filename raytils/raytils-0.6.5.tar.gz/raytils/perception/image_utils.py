from PIL import Image, ExifTags


def get_image_size(filepath):
    """Return image size (width, height) without loading. Respects correct orientation."""
    image = Image.open(filepath)

    try:
        orientation = None
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(image.getexif().items())

        if exif[orientation] == 3:
            image = image.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            image = image.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            image = image.transpose(Image.ROTATE_90)
        image.close()
    except (AttributeError, KeyError, IndexError):
        pass  # Image doesn't have ExIF data

    return image.size
