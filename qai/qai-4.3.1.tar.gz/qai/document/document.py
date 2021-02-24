from typing import List


class Segment:

    offset: int
    length: int
    segment_id: str
    content: str

    def __init__(self, offset: int, length: int, segment_id: str, content: str):
        self.offset = offset
        self.length = length
        self.segment_id = segment_id
        self.content = content

    def __str__(self) -> str:
        if self.content:
            return self.content
        return super().__str__()


class Paragraph:

    offset: int
    length: int
    content: str
    segments: List[Segment]

    def __init__(self, offset: int, length: int, content: str, segments: List[Segment]):
        self.offset = offset
        self.length = length
        self.content = content
        self.segments = segments

    def __str__(self) -> str:
        if self.content:
            return self.content
        return super().__str__()


class Document:

    content: str
    segments: List[Segment]
    paragraphs: List[Paragraph]

    def __init__(self, json_response):
        self.segments = []
        self.paragraphs = []

        if json_response:
            self.content = json_response['content']

            paragraph_segments = []
            offset = None
            length = 0
            pcontent = ''

            for segment in json_response['segments']:
                scontent = self.content[segment['offset']:segment['offset'] + segment['length']]
                seg = Segment(segment['offset'], segment['length'], segment['segmentId'], scontent)
                self.segments.append(seg)
                paragraph_segments.append(seg)

                pcontent += scontent
                length += segment['length']
                if offset is None:
                    offset = segment['offset']

                if scontent.endswith('\n'):
                    self.paragraphs.append(Paragraph(offset, length, pcontent, paragraph_segments))
                    paragraph_segments = []
                    offset = None
                    length = 0
                    pcontent = ''
        else:
            self.content = ''

    def __str__(self) -> str:
        if self.content:
            return self.content
        return super().__str__()
