from weasyprint import HTML
import os
from subprocess import call, Popen, PIPE
import mammoth
import markdown2
import logging
from typing import List, Dict
import re
import fnmatch
import contextlib
import shutil
import pypandoc


"""
Transformations can be any Python callable with this signature:
    - working_dir: str
    - logger: logging.Logger
    - options: dict = None

Transformations MUST provide a "description" property
as a dictionary formatted like this:
    {
        "label": "[transformation name]",  # human-friendly name for display
        "help": "[transformation help]",  # help text
        "options: [
            {
                "id": "option id",  # id of option to be used in options dictionary
                "label": "[option label]",  # human-friendly name for display
                "values: {"value": "human friendly label"},
                "default: "default_value",
                "free_input": False
            }
        ]
    }

This dict will be returned with all other transformations described at
GET /transformations/

User interfaces may rely upon those descriptions, so be as complete as possible.
"""

DONE_MESSAGE = "{}: {} files done."


def _find_files(which: str, where: str = ".") -> List[str]:
    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [
        "{}{}{}".format(where, os.path.sep, name)
        for name in os.listdir(where)
        if rule.match(name)
    ]


def _try_to_remove(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False


def _pic_to_tiled_tiff(source: str, destination: str, dpi: int = 300) -> int:
    tif_source = "{}.delme.tif".format(source)
    _, extension = os.path.splitext(source)
    if extension.lower() in {".pdf", ".ai"}:
        pdftoppm_dest = "{}.delme".format(
            source
        )  # pdftoppm adds .tif extension already...
        status = call(
            ["pdftoppm", "-singlefile", "-tiff", source, "-r", str(dpi), pdftoppm_dest]
        )
    else:
        status = call(["convert", "-auto-orient", source, tif_source])
    if status > 0:
        _try_to_remove(tif_source)
        return status
    status = call(
        [
            "vips",
            "im_vips2tiff",
            tif_source,
            "{}:deflate,tile:256x256,pyramid".format(destination),
        ]
    )
    if status > 0:
        _try_to_remove(destination)
    _try_to_remove(tif_source)
    return status


class _classproperty:
    """
    Decorator to had dynamic class properties
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def do_nothing(working_dir: str, logger: logging.Logger, options: dict = None):
    logger.info("Do Nothing :-)")


do_nothing.description = {
    "label": "Ne fait rien",
    "help": "Ne fait rien absolument rien. Utile pour tester l'API.",
    "options": [],
}


def markdown_to_html(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.md files...")
    for markdown_file_path in _find_files("*.md", working_dir):
        with open(markdown_file_path, "r") as markdown_file:
            logger.info(
                "Convert {} to HTML".format(os.path.basename(markdown_file_path))
            )
            html = markdown2.markdown("\r\n".join(markdown_file.readlines()))
            with open("{}.html".format(markdown_file_path), "w") as html_file:
                html_file.write(html)
        os.remove(markdown_file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("Markdown to HTML", nb_of_files_treated))


markdown_to_html.description = {
    "label": "Markdown vers HTML",
    "help": "Convertir les fichiers *.md en fichiers *.html",
    "options": [],
}


def html_to_pdf(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.html files...")
    for html_file_path in _find_files("*.html", working_dir):
        logger.info("Convert {} to PDF".format(os.path.basename(html_file_path)))
        page = HTML(html_file_path)
        page.write_pdf("{}.pdf".format(html_file_path))
        os.remove(html_file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("HTML to PDF", nb_of_files_treated))


html_to_pdf.description = {
    "label": "HTML vers PDF",
    "help": "Convertir les fichiers *.html en fichiers *.pdf",
    "options": [],
}


def wkhtml_to_image(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.html files...")
    for html_file_path in _find_files("*.html", working_dir):
        logger.info("Convert {} to image".format(os.path.basename(html_file_path)))
        destination_file = "{}.png".format(html_file_path)
        return_code = call(["wkhtmltoimage", html_file_path, destination_file])
        if return_code != 0:
            logger.error("Transformation encountered an error with the subprocess.")
            with contextlib.suppress(FileNotFoundError):
                os.remove(destination_file)
        os.remove(html_file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("WKHTML to image", nb_of_files_treated))


wkhtml_to_image.description = {
    "label": "WKHTML vers image",
    "help": "Convertir les fichiers *.html en image *.png en utilisant wkhtmltoimage",
    "options": [],
}


def wkhtml_to_pdf(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.html files...")
    for html_file_path in _find_files("*.html", working_dir):
        logger.info("Convert {} to PDF".format(os.path.basename(html_file_path)))
        destination_file = "{}.pdf".format(html_file_path)
        return_code = call(["wkhtmltopdf", html_file_path, destination_file])
        if return_code != 0:
            logger.error("Transformation encountered an error with the subprocess.")
            with contextlib.suppress(FileNotFoundError):
                os.remove(destination_file)
        os.remove(html_file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("WKHTML to PDF", nb_of_files_treated))


wkhtml_to_pdf.description = {
    "label": "WKHTML vers PDF",
    "help": "Convertir les fichiers *.html en fichiers *.pdf en utilisant wkhtmltopdf",
    "options": [],
}


class tesseract:
    def __init__(self, working_dir: str, logger: logging.Logger, options: dict = None):
        image_types = ("png", "jpg", "jpeg", "gif", "tif")
        images_files = []
        for image_type in image_types:
            images_files.extend(_find_files("*.{}".format(image_type), working_dir))

        logger.info("Looking for {} files...".format(", ".join(image_types)))
        nb_of_files_treated = 0
        for images_file in images_files:
            logger.info("Trying OCR on {}".format(os.path.basename(images_file)))
            destination_file = "{}.out".format(images_file)
            return_code = call(
                [
                    "tesseract",
                    "-l",
                    self._validate_lang(options.get("lang", "eng")),
                    images_file,
                    destination_file,
                ]
            )
            if return_code != 0:
                logger.error("Transformation encountered an error with the subprocess.")
                with contextlib.suppress(FileNotFoundError):
                    os.remove(destination_file)
            os.remove(images_file)
            nb_of_files_treated += 1
        logger.info(DONE_MESSAGE.format("Tesseract", nb_of_files_treated))

    def _validate_lang(self, lang: str) -> str:
        return lang if lang in self._available_langs() else "eng"

    def _available_langs(self) -> List:
        p = Popen(["tesseract", "--list-langs"], stdout=PIPE)
        langs = []
        for line in p.stdout.readlines()[1:]:
            langs.append(line.decode("UTF-8").strip())
        return langs

    @_classproperty
    def description(cls):
        known_langs_w_labels = {"fra": "français", "eng": "anglais", "lat": "latin"}
        descr = {
            "label": "Tesseract OCR",
            "help": "Faire de la reconnaissance de caractères sur des fichiers images",
            "options": [],
        }
        p = Popen(["tesseract", "--list-langs"], stdout=PIPE)
        values = {}
        for line in p.stdout.readlines()[1:]:
            lang = line.decode("UTF-8").strip()
            values[lang] = known_langs_w_labels.get(lang, lang)
        descr["options"].append(
            {
                "id": "lang",
                "label": "choix de la langue",
                "values": values,
                "default": "eng",
                "free_input": False,
            }
        )
        return descr


class _MammothImageWriter(object):
    def __init__(self, output_dir: str):
        self._output_dir = output_dir
        self._image_number = 1

    def __call__(self, element) -> Dict[str, str]:
        extension = element.content_type.partition("/")[2]
        image_filename = "{0}.{1}".format(self._image_number, extension)
        with open(os.path.join(self._output_dir, image_filename), "wb") as image_dest:
            with element.open() as image_source:
                shutil.copyfileobj(image_source, image_dest)

        self._image_number += 1

        return {"src": image_filename}


def docx_to_markdown(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.docx files...")
    options = {} if options is None else options
    embedded_images = True if options.get("embedded_images", "yes") == "yes" else False
    image_converter = None
    if not embedded_images:
        image_converter = mammoth.images.img_element(_MammothImageWriter(working_dir))
    for file_path in _find_files("*.docx", working_dir):
        with open(file_path, "rb") as docx_file:
            logger.info("Convert {} to markdown".format(os.path.basename(file_path)))
            result = mammoth.convert_to_markdown(
                docx_file, convert_image=image_converter
            )
            with open("{}.md".format(file_path), "w") as markdown_file:
                markdown_file.write(result.value)
        os.remove(file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("DOCX to Markdown", nb_of_files_treated))


docx_to_markdown.description = {
    "label": "DOCX vers Markdown",
    "help": "Convertir des fichiers *.docx en fichiers *.md",
    "options": [
        {
            "id": "embedded_images",
            "label": "Inclure les images dans le fichier markdown",
            "values": {"yes": "oui", "no": "non"},
            "default": "no",
        }
    ],
}


def to_tiled_tif(working_dir: str, logger: logging.Logger, options: dict = None):
    options = {} if options is None else options
    dpi = options.get("dpi", 300)
    nb_of_files_treated = 0
    extensions = {".ai", ".pdf", ".png", ".jpg", ".jpeg", ".jpe", ".gif", ".bmp"}
    files = []
    for extension in extensions:
        files = files + _find_files("*{}".format(extension), working_dir)
    for file_path in files:
        logger.info("Convert {} to tif".format(os.path.basename(file_path)))
        _, current_extension = os.path.splitext(file_path)
        result_file = "{}.tiled.tif".format(file_path)
        status = _pic_to_tiled_tiff(file_path, result_file, dpi)
        if status > 0:
            logger.error(
                "Transformation failed for file {}. Exit code  = {}".format(
                    file_path, status
                )
            )
            _try_to_remove(result_file)
        else:
            nb_of_files_treated += 1
            _try_to_remove(file_path)
    logger.info(DONE_MESSAGE.format("To tiled TIFF", nb_of_files_treated))


to_tiled_tif.description = {
    "label": "Pic to tiled TIF",
    "help": "Conversion image (pdf, png, jpg, ai, gif, bmp, tif, vers .TIF tuilé.",
    "options": [
        {
            "id": "dpi",
            "label": "Points par pouces",
            "values": {"300": "300"},
            "default": "300",
            "free_input": True,
        }
    ],
}


def tif_to_png(working_dir: str, logger: logging.Logger, options: dict = None):
    nb_of_files_treated = 0
    logger.info("Looking for *.tif files...")
    for file_path in _find_files("*.tif", working_dir):
        logger.info("Convert {} to PNG".format(os.path.basename(file_path)))
        destination_file = "{}.png".format(file_path)
        return_code = call(["convert", file_path, destination_file])
        if return_code != 0:
            logger.error("Transformation encountered an error with the subprocess.")
            with contextlib.suppress(FileNotFoundError):
                os.remove(destination_file)
        os.remove(file_path)
        nb_of_files_treated += 1
    logger.info(DONE_MESSAGE.format("TIFF to PNG", nb_of_files_treated))


tif_to_png.description = {
    "label": "TIFF to PNG",
    "help": "Conversion image .tif vers .png en utilisant convert (imagemagick)",
    "options": [],
}


class pandoc:
    def __init__(self, working_dir: str, logger: logging.Logger, options: dict = None):
        nb_of_files_treated = 0
        out_format = options.get("destination_format", None) if options else None
        if out_format not in pypandoc.get_pandoc_formats()[1]:
            logger.info(
                'Unknown pandoc output format "{}". Nothing to do here.'.format(
                    out_format
                )
            )
            logger.info(DONE_MESSAGE.format("HTML to PDF", nb_of_files_treated))
            return
        for in_file in _find_files("*.*", working_dir):
            base_name = os.path.basename(in_file)
            if base_name in ["job.json", "out.log"]:
                continue
            logger.info(
                "Convert {} to {}".format(os.path.basename(in_file), out_format)
            )
            try:
                pypandoc.convert_file(
                    in_file, out_format, outputfile="{}.{}".format(in_file, out_format)
                )
                os.remove(in_file)
                nb_of_files_treated += 1
            except RuntimeError as e:
                logger.info("Pandoc error, ignoring file: {}".format(e))
        logger.info(DONE_MESSAGE.format("Pandoc", nb_of_files_treated))

    @_classproperty
    def description(cls):
        version = pypandoc.get_pandoc_version()
        in_formats, out_formats = pypandoc.get_pandoc_formats()
        descr = {
            "label": "Pandoc",
            "help": "Utiliser Pandoc {}. Formats supportés en entrée: {}.".format(
                version, ", ".join(in_formats)
            ),
            "options": [
                {
                    "id": "destination_format",
                    "label": "format de destination",
                    "values": dict(zip(out_formats, out_formats)),
                }
            ],
        }
        return descr
