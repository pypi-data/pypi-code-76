import numpy as np
import cv2

__all__ = ["image_list_to_grid", "write_text_cv2"]


def write_text_cv2(image, text, x=None, y=None, centre=True, font=None, scale=None, thickness=None, colour=None):
    """Place text on an image around a point (x, y) top left (centre=False) or centre (centre=True)

    Args:
        image: np.array to draw on (m, n, 3)
        text: Text to be put on the image
        x: text co-ordinate x
        y: text co-ordinate y
        centre: If true (x, y) anchor is the centre not top-left
        font: cv2.FONT (default = cv2.FONT_HERSHEY_SIMPLEX)
        scale: Text scale (default = 1)
        thickness: Text thickness (default = 1)
        colour: Colour to draw text with (default = (0, 0, 0)

    Returns:
        image: With text drawn
    """
    if y is None:
        y = image.shape[0] / 2
    if x is None:
        x = image.shape[1] / 2

    x = image.shape[1] // 2 if x is None else x
    y = image.shape[0] // 2 if y is None else y
    font = cv2.FONT_HERSHEY_SIMPLEX if font is None else font
    scale = 1 if scale is None else scale
    thickness = 1 if thickness is None else thickness
    colour = (0, 0, 0) if colour is None else colour
    text = str(text)

    text_size = cv2.getTextSize(text, font, scale, thickness)[0]

    if centre:
        x -= text_size[0] / 2
        y -= text_size[1] / 2

    cv2.putText(image, text, (int(x), int(y)), font, scale, colour, thickness)
    return image


def image_list_to_grid(images_list: list, columns: int = None, resize: bool = False, background_colour=None):
    """Convert a list of Numpy nd.array images to a single grid image

    Args:
        images_list: List of numpy images
        columns: Desired number of columns (optional)
        resize: If the images are of different sizes this will  (optional)

    Returns:
        Grid of all images in the image_list
    """
    max_size = images_list[0].shape
    for image in images_list:
        max_size = tuple(max(max_size[i], image.shape[i]) for i in range(len(max_size)))

    if background_colour is None:
        background_colour = (0, 0, 0)

    center_h = max_size[0] / 2
    center_w = max_size[1] / 2
    canvas = []
    for image in images_list:
        if resize:
            canvas.append(cv2.resize(image, max_size[:2]))
        else:
            c = np.ones(max_size, dtype=image.dtype) * background_colour
            ch, cw = image.shape[:2]
            ch, cw = ch / 2, cw / 2
            sh, eh, sw, ew = int(center_h - ch), int(center_h + ch), int(center_w - cw), int(center_w + cw),
            c[sh:eh, sw:ew] = image
            canvas.append(c)

    if columns is None:
        columns = int((canvas[0].shape[0] / canvas[0].shape[1]) * (len(canvas) ** 0.5)) + 1
    pad_by = (columns - (len(canvas) % columns))
    pad_by = 0 if pad_by == columns else pad_by
    padding = [np.zeros_like(canvas[-1])] * pad_by
    padded_canvas = canvas + padding

    rows = len(padded_canvas) // columns

    padded_canvas = np.asarray(padded_canvas)
    length, height, width, intensity = padded_canvas.shape

    result = padded_canvas.reshape(rows, columns, height, width, intensity).swapaxes(1, 2).reshape(
        height * rows, width * columns, intensity)

    return result
