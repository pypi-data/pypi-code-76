import PyPDF2
from pdfminer.high_level import extract_text

class LeitorPDF:
    def __init__(self):
        pass

    def show_all_text(self, document):
        text_in_document = []
        pdf_file = open(document, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pages = pdf_reader.numPages

        for i in range(pages):
            page_obj = pdf_reader.getPage(i)
            text_in_document.append(page_obj.extractText())
        return ' '.join(text_in_document)

    def text_pdf_with_table(self, document):
        text_in_pdf = extract_text(document)
        return text_in_pdf
