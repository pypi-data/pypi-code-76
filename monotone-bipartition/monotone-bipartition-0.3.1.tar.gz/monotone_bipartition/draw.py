import svgwrite


def draw(recs, path):
    """Draw bipartition induced by rectangles. Assumes domain is normalized."""
    dwg = svgwrite.Drawing(path, size=(100, 100), profile='tiny')

    # Add seperating rectangles.
    for rec in recs:
        assert rec.dim == 2
        xlo, ylo = rec.bot
        xhi, yhi = rec.top

        # Accept region. Top left corner.

        point = round(xlo * 100), 0
        size = round(100 * (1 - xlo)), round(100 * (1 - yhi))

        dwg.add(
            svgwrite.shapes.Rect(
                insert=point,
                size=size,
                fill="green",
                opacity="0.2",
            )
        )

        # Reject region. Top left corner.

        point = 0, round((1 - yhi) * 100)
        size = round(100 * xlo), round(100 * yhi)

        dwg.add(
            svgwrite.shapes.Rect(
                insert=point,
                size=size,
                fill="red",
                opacity="0.2",
            )
        )

    dwg.save()
