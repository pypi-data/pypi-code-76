from doctrans.models.option import Option, Lang, Extension, DocTrans, TextTrans, Font


def run(input_file_list: [str],
        output_directory: str,
        doc_trans: DocTrans,
        text_trans: TextTrans,
        font: Font,
        format: Extension,
        from_lang: Lang,
        to_lang: Lang,
        use_thread: bool = True) -> None:
    from doctrans.models.translator import Translator
    from doctrans.models.pymupdf.translator import PymupdfTranslator
    from doctrans.models.pydocx.translator import DocxTranslator
    import os
    from datetime import datetime

    def getTranslator(option: Option) -> Translator:
        if option.doc_trans == DocTrans.PYMUPDF:
            return PymupdfTranslator(option)
        elif option.doc_trans == DocTrans.PYDOCX:
            return DocxTranslator(option)
        else:
            raise NotImplementedError

    for input_path in input_file_list:
        try:
            filename = os.path.splitext(os.path.basename(input_path))[0]
            from_ext = Extension(os.path.splitext(input_path)[-1])

            option = Option(
                doc_trans=doc_trans,
                text_trans=text_trans,
                font=font,
                from_lang=from_lang,
                to_lang=to_lang,
                from_ext=from_ext,
                to_ext=format,
                use_thread=use_thread
            )

            translator = getTranslator(option)

            keycode = f"{option.doc_trans.value}_{datetime.now().strftime('%y%m%d_%H%M%S')}"
            outfilename = f"{os.path.splitext(filename)[0]}.trans_{keycode}{option.to_ext.value}"
            output_path = os.path.join(output_directory, outfilename)

            translator.run(input_path, output_path)

        except Exception as e:
            print(f"Error while translate [ {input_path} ]!")
            print(e.__repr__())


def run_default(input_file_list: [str], output_directory: str) -> None:
    from doctrans.models.translator import Translator
    from doctrans.models.option import PDF_BASIC_OPTION, DOCX_BASIC_OPTION
    import os

    for input_path in input_file_list:
        from_ext = Extension(os.path.splitext(input_path)[-1])

        option = None
        if from_ext == Extension.PDF:
            option = PDF_BASIC_OPTION
        elif from_ext == Extension.DOCX:
            option = DOCX_BASIC_OPTION

        run([input_path], output_directory,
            doc_trans=option.doc_trans,
            text_trans=option.text_trans,
            font=option.font,
            format=option.to_ext,
            from_lang=option.from_lang,
            to_lang=option.to_lang,
            use_thread=option.use_thread)
