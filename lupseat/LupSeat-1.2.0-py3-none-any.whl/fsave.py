from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import math
import os
import papersize

from models.room import *
from models.parser import *

def papersize_to_imagesize(image_size):
    if "flip" in image_size:
        if image_size.split(' ')[0] == "flip":
            paperformat = image_size.split(' ')[1]
        else:
            paperformat = image_size.split(' ')[0]
        return tuple(map(lambda x: int(x)*2, papersize.parse_papersize(paperformat, unit="pt")))[::-1]
    return tuple(map(lambda x: int(x)*2, papersize.parse_papersize(image_size, unit="pt")))

def get_stdt_list(rm, stdts, str_form, sort_by):
    # TODO Fix sort_by
    stdt_list = []
    fmt = SliceFormatter()
    for row in range(rm.max_row):
        for col in range(rm.max_col):
            if rm.seats[row][col] == None:
                continue

            if rm.seats[row][col].sid == -1:
                continue

            row_chr = int_to_chr(row)
            col_chr = str(col + 1)

            sid = rm.seats[row][col].sid
            fname = stdts[sid].first
            lname = stdts[sid].last

            stdt_str = fmt.format(str_form, sid=str(sid), fname=fname, lname=lname)
            seat_str = "{}{}".format(row_chr.upper(), col_chr)

            if sort_by == "fname":
                sort_key = fname
            if sort_by == "lname":
                sort_key = lname
            if sort_by == "sid":
                sort_key = sid
            if sort_by == "seat":
                sort_key = seat_str
            stdt_list.append([seat_str, stdt_str, sort_key])

    stdt_list = sorted(stdt_list, key=lambda x: x[2])
    stdt_list = list(map(lambda x: x[:2], stdt_list))

    return stdt_list

def save_chart(rm, filepath, stdts, str_form, seed, sort_by):
    """Saves seats with student info to a file

    Args:
        stdst (dict{Student}): map of students, identified by sid
        filepath (str): filepath for output
        str_form (str): output format for each student, specified by user
        seed (int): seed for randomizer
    """
    stdt_list =  get_stdt_list(rm, stdts, str_form, sort_by=sort_by)

    with open(filepath, 'w') as outfile:
        for stdt_fmt in stdt_list:
            outfile.write(",".join(stdt_fmt) + '\n')
        outfile.write("\nSeed:{}\n".format(seed))

    print("Finished saving to file: {}".format(filepath))

# For graphical chart output
def draw_grid(d_ctx, position, height, width_1, width_2, alternate_flag):
    lines = []
    # TOP
    pt1 = (position[0], position[1])
    pt2 = (position[0] + width_1 + width_2, position[1])
    lines.append([pt1, pt2])
    # BOTTOM
    pt1 = (position[0], position[1] + height)
    pt2 = (position[0] + width_1 + width_2, position[1] + height)
    lines.append([pt1, pt2])
    # LEFT
    pt1 = (position[0], position[1])
    pt2 = (position[0], position[1] + height)
    lines.append([pt1, pt2])
    # RIGHT
    pt1 = (position[0] + width_1 + width_2, position[1])
    pt2 = (position[0] + width_1 + width_2, position[1] + height)
    lines.append([pt1, pt2])
    # CENTER
    pt1 = (position[0] + width_1, position[1])
    pt2 = (position[0] + width_1, position[1] + height)
    lines.append([pt1, pt2])

    # Fill in grid
    if alternate_flag:
        d_ctx.rectangle([position[0], position[1], position[0] + width_1 + width_2, position[1] + height], fill="lightgray")

    # Draw lines
    for line in lines:
        d_ctx.line(line, fill="black", width=1)

def draw_chart_header(d_ctx, seed, margin, title_font_size, font_size, image_size):
    # Draw title
    font = ImageFont.truetype("assets/Roboto-Light.ttf", title_font_size)
    d_ctx.text([margin[0], margin[1]], "Seating Chart", font=font, fill="black")

    # Draw seed
    font = ImageFont.truetype("assets/Roboto-Light.ttf", font_size)
    x = image_size[0] - margin[0] - font.getsize("Seed: {}".format(seed))[0]
    y = margin[1]
    d_ctx.text([x, y], "Seed: {}".format(seed), font=font, fill="black")

def calc_chart_im_specs(image_size, margin_ratio, stdt_list):
    margin = (round(image_size[0] * margin_ratio), round(image_size[1] * margin_ratio))
    top_margin = margin[1]
    title_font_size = round(top_margin / 2)

    font_size = round(title_font_size / 2)
    text_margin = font_size

    # Get text lengths
    font = ImageFont.truetype("assets/Roboto-Light.ttf", font_size)
    max_len_seats = max(map(lambda x: font.getsize(x[0])[0], stdt_list))
    max_len_str = max(map(lambda x: font.getsize(x[1])[0], stdt_list))

    height = text_margin * 2 + font.getsize("dummy")[1]
    width_1 = text_margin * 2 + max_len_seats
    width_2 = text_margin * 2 + max_len_str

    num_cols = math.floor((image_size[0] - margin[0] * 2) / (width_1 + width_2))
    row_margin = (image_size[0] - margin[0] * 2) / num_cols - width_1 - width_2

    return margin, top_margin, title_font_size, font_size, text_margin, max_len_seats, max_len_str, height, width_1, width_2, row_margin

def save_gchart(rm, filepath, image_size, stdts, str_form, seed, sort_by):
    image_size = papersize_to_imagesize(image_size)
    stdt_list =  get_stdt_list(rm, stdts, str_form, sort_by=sort_by)

    images = [Image.new("RGB", image_size, "white")]
    d_ctx = ImageDraw.Draw(images[0])

    margin_ratio = 0.05
    res = calc_chart_im_specs(image_size, margin_ratio, stdt_list)
    (margin, top_margin, title_font_size, font_size, text_margin, max_len_seats, max_len_str, height, width_1, width_2, row_margin) = res

    draw_chart_header(d_ctx, seed, margin, title_font_size, font_size, image_size)

    position = [0, 0]
    position[0] = margin[0]
    position[1] = margin[1] + top_margin

    font = ImageFont.truetype("assets/Roboto-Light.ttf", font_size)
    alternate_flag = False
    for stdt in stdt_list:
        # Draw grid
        alternate_flag = not alternate_flag
        draw_grid(d_ctx, position, height, width_1, width_2, alternate_flag)

        # Draw text
        d_ctx.text([position[0] + text_margin, position[1] + text_margin], stdt[0], font=font, fill="black")
        d_ctx.text([position[0] + text_margin * 3 + max_len_seats, position[1] + text_margin], stdt[1], font=font, fill="black")

        # Update position
        position[1] += height

        # Change cols if necessary
        if position[1] + height + margin[1] > image_size[1]:
            position[0] += width_1 + width_2 + row_margin
            position[1] = margin[1] + top_margin
            if len(images) > 1:
                position[1] = margin[1]

        if position[0] + width_1 + width_2 + margin[0] > image_size[0]:
            images.append(Image.new("RGB", image_size, "white"))
            d_ctx = ImageDraw.Draw(images[-1])
            position[0] = margin[0]
            position[1] = margin[1]
            
    pdf = FPDF(unit = "pt", format = [image_size[0], image_size[1]])
    for index, image in enumerate(images):
        cur_filepath = str(index) + "temp.jpg"
        image.save(cur_filepath, "JPEG")
        pdf.add_page()
        pdf.image(cur_filepath, 0, 0)
        os.remove(cur_filepath)
    pdf.output(filepath, "F")
    print("Finished saving to image file: {}".format(filepath))

# For graphical room output
def calc_room_im_specs(rm, image_size, margin_ratio, font_ratio, seat_ratio):
    seat_space_ratio = seat_ratio[0]
    seat_size_ratio = seat_ratio[1]
    separator_ratio = seat_ratio[2]

    # Get title and margin
    margin = (round(image_size[0] * margin_ratio), round(image_size[1] * margin_ratio))
    top_margin = margin[1] * 2
    title_font_size = round(top_margin / 2)
    key_font_size = round(title_font_size / 2)
    key_margin = round(key_font_size / 2)
    key_box_size = key_font_size

    # Effective image size (for calculations only)
    eff_im_x = image_size[0] - margin[0] * 2
    eff_im_y = image_size[1] - (margin[1] * 2 + top_margin)

    # Get separator size based on ratio
    max_num_breaks = max(list(map(len, rm.row_breaks))) - 1
    row_separator_size = round(eff_im_x * separator_ratio / max_num_breaks)

    # Space per seat i.e. seat_margin + seat_size + row_separator (for calculations only)
    space_per_seat_x = eff_im_x / rm.max_col
    space_per_seat_y = eff_im_y / rm.max_row
    seat_size = (round(space_per_seat_x * seat_size_ratio), round(space_per_seat_y * seat_size_ratio))
    seat_margin = (round(space_per_seat_x * seat_space_ratio), round(space_per_seat_y * (seat_space_ratio + separator_ratio)))
    font_margin = (round(margin_ratio * seat_size[0]), round(margin_ratio * seat_size[1]))
    font_size = min(round(font_ratio * seat_size[0]), round(font_ratio * seat_size[1]))

    return margin, top_margin, title_font_size, key_font_size, key_box_size, row_separator_size, seat_size, seat_margin, font_margin, key_margin, font_size

# For graphical room output
def draw_room_header(d_ctx, title_font_size, key_font_size, key_margin, margin, image_size, key_box_size):
    # Title
    font = ImageFont.truetype("assets/Roboto-Light.ttf", title_font_size)
    d_ctx.text([margin[0], margin[1]], "Seating Chart", font=font, fill="black")

    # Draw labels for key
    font = ImageFont.truetype("assets/Roboto-Light.ttf", key_font_size)
    lb_length = max(font.getsize("Empty")[0], font.getsize("Taken")[0])
    lb_height = max(font.getsize("Empty")[1], font.getsize("Taken")[1])
    lb_begin_x = image_size[0] - margin[0] - lb_length
    d_ctx.text([lb_begin_x, margin[1]], "Empty", font=font, fill="black")
    d_ctx.text([lb_begin_x, margin[1] + lb_height + key_margin], "Taken", font=font, fill="black")

    # Draw boxes for key
    x0 = lb_begin_x - key_box_size - key_margin
    y0 = margin[1]
    x1 = lb_begin_x - key_margin
    y1 = margin[1] + key_box_size
    d_ctx.rectangle([x0, y0, x1, y1], fill="white", outline="black")
    d_ctx.rectangle([x0, y0+lb_height+key_margin, x1, y1+lb_height+key_margin], fill="lightblue", outline="black")

# For graphical room output
def draw_seat(d_ctx, label, position, seat_size, fill_color, font_size, font_margin):
    x0 = position[0]
    y0 = position[1]
    x1 = position[0] + seat_size[0]
    y1 = position[1] + seat_size[1]

    d_ctx.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black")

    fx = x0 + font_margin[0]
    fy = y0 + font_margin[1]
    font = ImageFont.truetype("assets/Roboto-Light.ttf", font_size)
    d_ctx.text([fx, fy], label, font=font, fill="black")

def save_groom(rm, filepath, image_size):
    """Saves seats with student info to an image file

    Args:
        filepath (str): filepath for output
    """
    # Margin ratio used for overall image margin as well as font image margin within seats
    margin_ratio = 0.06
    # Used to size font within seats
    font_ratio = 0.5
    # Used to size the seats themselves
    seat_space_ratio = 0.1
    seat_size_ratio = 0.7
    separator_ratio = 0.2

    # Algorithmically calculate size info
    image_size = papersize_to_imagesize(image_size)
    seat_ratio = (seat_space_ratio, seat_size_ratio, separator_ratio)
    res = calc_room_im_specs(rm, image_size, margin_ratio, font_ratio, seat_ratio)
    (margin, top_margin, title_font_size, key_font_size, key_box_size, row_separator_size, seat_size, seat_margin, font_margin, key_margin, font_size) = res

    # Create image
    image = Image.new("RGB", image_size, "white")
    d_ctx = ImageDraw.Draw(image)

    # Set start position
    start_position = [0, 0]
    start_position[0] += margin[0]
    start_position[1] += margin[1] + top_margin
    position = [0, 0]
    position[0] = start_position[0]
    position[1] = start_position[1]

    draw_room_header(d_ctx, title_font_size, key_font_size, key_margin, margin, image_size, key_box_size)

    for row in range(rm.max_row):
        for col in range(rm.max_col):
            # Set seat label
            label = chr(row + ord('A')) + str(col+1)

            # Draw seat and label
            if rm.seats[row][col] == None:
                pass
            elif rm.seats[row][col].broken:
                draw_seat(d_ctx, label, position, seat_size, "red", font_size, font_margin)
            elif rm.seats[row][col].sid == -1:
                draw_seat(d_ctx, label, position, seat_size, "white", font_size, font_margin)
            else:
                draw_seat(d_ctx, label, position, seat_size, "lightblue", font_size, font_margin)

            # Update position
            position[0] += seat_size[0] + seat_margin[0]
            if col in rm.row_breaks[row]:
                position[0] += row_separator_size

        # Update position
        position[0] = start_position[0]
        position[1] += seat_size[1] + seat_margin[1]

    image.save(filepath, "JPEG")
    print("Finished saving to image file: {}".format(filepath))

