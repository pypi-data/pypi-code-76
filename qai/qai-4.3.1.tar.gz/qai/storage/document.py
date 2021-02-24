import re
from typing import List

from bs4 import BeautifulSoup


class Segment:
    """
    start: Segment start, calculated from document start
    end: Segment end, calculated from document start
    tag: Segment tag name e.g. span
    html: Segment html
    text: Segment plain text
    start_text: Segment text start, calculated from segment start i.e. return 6 for <span>hello</span>
    end_text: Segment text end, calculated from segment start i.e. return 11 for <span>hello</span>
    attrs: dict containing element html attributes and their values
    """
    start: int
    end: int
    tag: str
    html: str
    text: str
    start_text: int
    end_text: int
    attrs: dict

    def __init__(self, start: int, end: int, tag: str, html: str, text: str = None, start_text: int = None,
                 end_text: int = None, attrs: dict = None):
        self.start = start
        self.end = end
        self.tag = tag
        self.html = html
        if text:
            self.text = text
            self.start_text = start_text
            self.end_text = end_text
        self.attrs = attrs if attrs is not None else {}

    def get_segment_id(self):
        if self.attrs and 'segment_id' in self.attrs:
            return self.attrs['segment_id']
        return None

    def __str__(self) -> str:
        if self.html:
            return self.html
        return super().__str__()


class Paragraph:
    """
    start: Paragraph start, calculated from document start
    end: Paragraph end, calculated from document start
    html: Paragraph html
    text: Paragraph plain text i.e. segments plain texts separated by a space
    segments: list of Segments within the paragraph
    """
    start: int
    end: int
    html: str
    text: str
    segments: List[Segment]

    def __init__(self, start: int, end: int, html: str, text: str, segments: List[Segment]):
        self.start = start
        self.end = end
        self.html = html
        self.text = text
        self.segments = segments

    def __str__(self) -> str:
        if self.html:
            return self.html
        return super().__str__()


class Document:
    text: str
    paragraphs: List[Paragraph]

    def __init__(self, html: str):
        """
        Current document format stored in bigtable ccontains:
            spans for segments
            br(s) as paragraph separator
        :param html: document html
        """
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            segment = None
            paragraph = None
            paragraph_segments = []
            paragraphs = []
            paragraph_start = 0
            paragraph_text = ''
            document_text = ''
            for element in soup.find_all():
                # update previous segment end position
                # because of invalid html tags `end = start + element_len` didn't work e.g. <br> should be <br/>
                if segment is not None:
                    segment.end = element.sourcepos
                    segment.html = html[segment.start:segment.end]
                    segment.start_text = segment.html.find(segment.text)
                    segment.end_text = segment.start_text + len(segment.text)
                    segment = None

                if paragraph is not None:
                    paragraph.end = element.sourcepos
                    paragraph.html = html[paragraph.start:paragraph.end]
                    paragraph = None

                if len(paragraph_segments) == 0:
                    paragraph_start = element.sourcepos

                tag = element.name
                if tag == 'span':
                    start = element.sourcepos
                    text = element.get_text().strip()
                    paragraph_text += text + ' '
                    attrs = element.attrs
                    segment = Segment(start, 0, tag, '', text, 0, 0, attrs)
                    paragraph_segments.append(segment)
                elif tag == 'br':
                    # double br
                    if element.nextSibling and element.nextSibling.name == 'br':
                        continue

                    if len(paragraph_segments) > 0:
                        paragraph = Paragraph(paragraph_start, 0, '', paragraph_text[0:-1], paragraph_segments)
                        paragraphs.append(paragraph)
                        document_text += paragraph_text
                        paragraph_segments = []
                        paragraph_text = ''
                else:
                    raise NotImplementedError()

            if segment is not None:
                segment.end = len(html)
                segment.html = html[segment.start:segment.end]

            if paragraph is not None:
                paragraph.end = len(html)
                paragraph.html = html[paragraph.start:paragraph.end]

            self.text = document_text[0:-1]
            self.paragraphs = paragraphs
        else:
            self.text = ''
            self.paragraphs = []

    def __str__(self) -> str:
        if self.text:
            return self.text
        return super().__str__()


class PlainDocument:
    text: str
    paragraphs: List[Paragraph]

    def __init__(self, plain_text: str, nlp):
        """
        Current extension document format stored in bigtable ccontains plain text and new lines
        WE DO DIFFERENT SEGMENTATION, SO COMPARING DOCUMENTS SEGMENTS WITH REST PAYLOAD SEGMENT WON'T WORK
        :param plain_text: document content
        """
        self.nlp = nlp
        if plain_text:
            paragraphs = []
            document_text = ''
            start = 0
            for match in re.finditer('(\\s)*(\\n)+(\\s)*(\\n)*', plain_text, re.MULTILINE):  # paragraph split
                end = match.start()  # text end, without the new lines separators
                text = plain_text[start:end]
                document_text += text + ' '

                end = match.end()  # with new lines separators
                html = plain_text[start:end]

                segments = self._extract_segments(text, start)
                paragraph = Paragraph(start, end, html, text, segments)
                paragraphs.append(paragraph)
                start = match.end()

            plain_text_len = len(plain_text)
            if plain_text_len > start:
                text = plain_text[start:plain_text_len]
                document_text += text + ' '
                segments = self._extract_segments(text, start)
                paragraph = Paragraph(start, plain_text_len, text, text, segments)
                paragraphs.append(paragraph)

            self.text = document_text[0:-1]
            self.paragraphs = paragraphs
        else:
            self.text = ''
            self.paragraphs = []

    def _extract_segments(self, paragraph_text, paragraph_start):
        segments = []
        for sent in self.nlp(paragraph_text, disable=['tagger', 'ner']).sents:
            segment = Segment(paragraph_start + sent.start_char, paragraph_start + sent.end_char, '', sent.text,
                              sent.text, sent.start_char, sent.end_char)
            segments.append(segment)
        return segments

    def __str__(self) -> str:
        if self.text:
            return self.text
        return super().__str__()
