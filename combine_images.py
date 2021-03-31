import tempfile

from PIL import Image


def horizontal_combo(content1, content2, content3, filename):
    images = [content1, content2, content3]
    widths, heights = zip(*(i.size for i in images))

    unit = min(heights + widths)
    total_width = unit * 3
    max_height = unit

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(filename)


def vertical_combo(content1, content2, content3, filename):
    images = [Image.open(content1), Image.open(content2), Image.open(content3)]
    widths, heights = zip(*(i.size for i in images))

    total_width = max(widths)
    max_height = min(heights + widths)

    new_im = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save(filename)

#
# def vertical_horizontal_combo(images):
#     with tempfile.TemporaryDirectory() as path:
#         horizontal_combo(images[0], images[1], images[2], path + "image0.jpg")
#         horizontal_combo(images[3], images[4], images[5], path + "image1.jpg")
#         horizontal_combo(images[6], images[7], images[8], path + "image1.jpg")
#         vertical_combo(path + "image0.jpg", path + "image1.jpg", path + "image2.jpg", path + "answer")
