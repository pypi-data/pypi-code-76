#!/usr/bin/env python

"""
Pandoc filter for using beamer multi-graphics ability
"""

from panflute import run_filter, Image, RawInline, MetaList, MetaInlines


def image(elem, doc):
    """
    Transform image element.

    Arguments
    ---------
        elem:
            current element
        doc:
            pandoc document
    """
    if doc.format == "beamer" and isinstance(elem, Image):
        classes = frozenset(elem.classes)

        # Loop on all multigraphics definition
        for definition in doc.defined:

            # Are the classes correct?
            if classes >= definition["classes"]:

                graphics = []

                if (
                    "height" in elem.attributes
                    or "width" in elem.attributes
                    or "height" in definition
                    or "width" in definition
                ):
                    graphics.append(
                        "height=%s"
                        % str(
                            elem.attributes.get(
                                "height", definition.get("height", "\\textheight")
                            )
                        )
                    )
                    graphics.append(
                        "width=%s"
                        % str(
                            elem.attributes.get(
                                "width", definition.get("width", "\\textwidth")
                            )
                        )
                    )

                options = []

                if "start" in elem.attributes:
                    options.append("start=%d" % int(elem.attributes["start"]))

                if "end" in elem.attributes:
                    options.append("end=%d" % int(elem.attributes["end"]))

                options.append(
                    "format=%s"
                    % str(elem.attributes.get("format", definition["format"]))
                )

                return RawInline(
                    "\\multiinclude[graphics={%s},%s]{%s}"
                    % (",".join(graphics), ",".join(options), elem.url),
                    "tex",
                )

    return None


def prepare(doc):
    """
    Prepare the document

    Arguments
    ---------
        doc:
            The pandoc document
    """

    # Prepare the definitions
    doc.defined = []

    # Get the meta data
    meta = doc.get_metadata("pandoc-beamer-multigraphics")

    if isinstance(meta, list):

        # Loop on all definitions
        for definition in meta:

            # Verify the definition
            if (
                isinstance(definition, dict)
                and "classes" in definition
                and isinstance(definition["classes"], list)
            ):
                definition["classes"] = frozenset(definition["classes"])
                definition["format"] = str(definition.get("format", "pdf"))
                if "width" in definition:
                    definition["width"] = str(definition["width"])
                if "height" in definition:
                    definition["height"] = str(definition["height"])

                doc.defined.append(definition)


def finalize(doc):
    """
    Finalize the document

    Arguments
    ---------
        doc:
            The pandoc document
    """
    # Add header-includes if necessary
    if "header-includes" not in doc.metadata:
        doc.metadata["header-includes"] = MetaList()
    # Convert header-includes to MetaList if necessary
    elif not isinstance(doc.metadata["header-includes"], MetaList):
        doc.metadata["header-includes"] = MetaList(doc.metadata["header-includes"])

    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{xmpmulti}", "tex"))
    )


def main(doc=None):
    """
    main function.

    Arguments
    ---------
        doc:
            pandoc document
    """
    return run_filter(image, doc=doc, prepare=prepare, finalize=finalize)


if __name__ == "__main__":
    main()
