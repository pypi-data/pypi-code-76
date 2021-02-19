from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class ConvertDates2UKNorm(NormalizerBase):
    NAME = "convert_dates2UK_norm"

    DESCRIPTION_TRAINING = """Convert Dates from US 2 UK format.
                             e.g: December 24 -> the 24th of December
                                                                   """

    DESCRIPTION_DECODING = """"""

    MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "November", "December"]

    def __init__(self, src_lang: str, tgt_lang: str):
        super().__init__(src_lang, tgt_lang)

    def _convert_dates2UK(self, text: str):
        res_text = text.split()
        if len(res_text) <= 1:
            return text
        else:
            for i, month in enumerate(res_text):
                # check if the word if a month
                if month in self.MONTHS and len(res_text) > i+1:
                    day = res_text[i+1]
                    day = day.split(",")[0]
                    day = day.split(".")[0]
                    # check if the next word is a month day
                    if day.isnumeric():
                        if int(day) in range(1,31):
                            # check if it is beginning of sentence to write "the" in capitals
                            the = "the"
                            if i == 0:
                                the = "The"
                            # check which number is to write the correct ordinal
                            ordinal = "th"
                            if day in ["1", "21", "31"]:
                                ordinal = "st"
                            if day in ["2", "22"]:
                                ordinal = "nd"
                            if day in ["3", "23"]:
                                ordinal = "rd"
                            text = text.replace(month+" "+day, the+" "+day+ordinal+" of "+month)
        
        return text


    # Called when training
    def process_train(self, seg: Seg) -> None:
        if self.src_lang == "en":
            seg.src = self._convert_dates2UK(seg.src)
        if self.tgt_lang == "en":
            seg.tgt = self._convert_dates2UK(seg.tgt)

    # Called when using model (before calling model to translate)
    def process_src_decoding(self, seg: Seg) -> None:
        if self.src_lang == "en":
            seg.src = self._convert_dates2UK(seg.src)

    # Called after the model translated (in case this would be necessary; usually not the case)
    def process_tgt_decoding(self, seg: Seg) -> None:
        if self.tgt_lang == "en":
            seg.tgt = self._convert_dates2UK(seg.tgt)

