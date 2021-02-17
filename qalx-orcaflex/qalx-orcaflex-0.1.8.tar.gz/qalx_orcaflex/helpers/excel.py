from openpyxl.styles import Font, Alignment, Side, Border

KELLY_HEX = [
    "FFB300",  # Vivid Yellow
    "803E75",  # Strong Purple
    "FF6800",  # Vivid Orange
    "A6BDD7",  # Very Light Blue
    "C10020",  # Vivid Red
    "CEA262",  # Grayish Yellow
    "817066",  # Medium Gray
    # The following don't work well for people with defective color vision
    "007D34",  # Vivid Green
    "F6768E",  # Strong Purplish Pink
    "00538A",  # Strong Blue
    "FF7A5C",  # Strong Yellowish Pink
    "53377A",  # Strong Violet
    "FF8E00",  # Vivid Orange Yellow
    "B32851",  # Strong Purplish Red
    "F4C800",  # Vivid Greenish Yellow
    "7F180D",  # Strong Reddish Brown
    "93AA00",  # Vivid Yellowish Green
    "593315",  # Deep Yellowish Brown
    "F13A13",  # Vivid Reddish Orange
    "232C16",  # Dark Olive Green
]


def set_range_border(
    ws,
    cell_range,
    left=Side(),
    right=Side(),
    top=Side(),
    bottom=Side(),
    horizontal=Side(),
    vertical=Side(),
):
    rows = list(ws.iter_rows(cell_range))
    top_row = rows[0]
    bottom_row = rows[-1]
    top_row[0].border = Border(left=left, top=top, right=vertical, bottom=horizontal)
    top_row[-1].border = Border(left=vertical, top=top, right=right, bottom=horizontal)
    bottom_row[0].border = Border(
        left=left, top=horizontal, right=vertical, bottom=bottom
    )
    bottom_row[-1].border = Border(
        left=vertical, top=horizontal, right=right, bottom=bottom
    )

    if len(rows) == 1:
        rows[0][0].border = Border(left=left, top=top, right=vertical, bottom=bottom)
        rows[0][-1].border = Border(left=vertical, top=top, right=right, bottom=bottom)
        for c in rows[0][1:-1]:
            c.border = Border(left=vertical, top=top, right=horizontal, bottom=bottom)
    else:
        for trc in top_row[1:-1]:
            trc.border = Border(
                left=vertical, top=top, right=vertical, bottom=horizontal
            )

        for trc in bottom_row[1:-1]:
            trc.border = Border(
                left=vertical, top=horizontal, right=vertical, bottom=bottom
            )

        for row in rows[1:-1]:
            row[0].border = Border(
                left=left, top=horizontal, right=vertical, bottom=horizontal
            )
            row[-1].border = Border(
                left=vertical, top=horizontal, right=right, bottom=horizontal
            )
            for c in row[1:-1]:
                c.border = Border(
                    left=vertical, top=horizontal, right=vertical, bottom=horizontal
                )


LARGE_BOLD = Font(bold=True, size=14)
BOLD = Font(bold=True)
CENTRE = Alignment(horizontal="center")
RIGHT = Alignment(horizontal="right")
THICK = Side(border_style="thick", color="FF000000")
THIN = Side(border_style="thin", color="FF000000")
