import win32com.client

wdFormatWord = 16
wdFormatPDF = 17

def pdf2docx(pdf_path, doc_path):
    word = win32com.client.Dispatch("word.Application")
    word.visible = False
    wb = word.Documents.Open(pdf_path)
    wb.SaveAs2(doc_path, FileFormat=wdFormatWord)
    wb.Close()
    word.Quit()

def docx2pdf(doc_path, pdf_path):
    word = win32com.client.Dispatch('Word.Application')
    word.visible = False
    doc = word.Documents.Open(doc_path)
    doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
