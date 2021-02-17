""" Модуль выполнения команд """
# /usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import logging
from typing import Dict, Union

from . import error_handler

# Недопустимые управляюещие символы в json (взято из RFC 1345, начина с с символа 0000)
INVALID_CONTROL_CHARACTERS = ["\u0000", "\u0001", "\u0002", "\u0003", "\u0004", "\u0005", "\u0006", "\u0007", "\u0008",
                              "\u0009", "\u0010", "\u0011", "\u0012", "\u0013", "\u0014", "\u0015", "\u0016", "\u0017",
                              "\u0018", "\u0019",
                              "\u001a", "\u001b", "\u001c", "\u001d", "\u001e", "\u001f", "\u007f",
                              "\u0080", "\u0081", "\u0082", "\u0083", "\u0084", "\u0085", "\u0086", "\u0087", "\u0088",
                              "\u0089",
                              "\u008a", "\u008b", "\u008c", "\u008d", "\u008e", "\u008f",
                              "\u0090", "\u0091", "\u0092", "\u0093", "\u0094", "\u0095", "\u0096", "\u0097", "\u0098",
                              "\u0099",
                              "\u009a", "\u009b", "\u009c", "\u009d", "\u009e", "\u009f",
                              "\ue000", "\ue001", "\ue002", "\ue003", "\ue004", "\ue005", "\ue006", "\ue007", "\ue008",
                              "\ue009", "\ue010", "\ue011", "\ue012", "\ue013", "\ue014", "\ue015", "\ue016",
                              "\ue017", "\ue018", "\ue019",
                              "\ue01a", "\ue01b", "\ue01c", "\ue01d", "\ue01e", "\ue01f",
                              "\ue020", "\ue021", "\ue022", "\ue023", "\ue024", "\ue025", "\ue026", "\ue027", "\ue027",
                              "\u080f", "\ufeff"]


# ************* RFC 1345 *********************
#
#  NU     0000    NULL (NUL)
#  SH     0001    START OF HEADING (SOH)
#  SX     0002    START OF TEXT (STX)
#  EX     0003    END OF TEXT (ETX)
#  ET     0004    END OF TRANSMISSION (EOT)
#  EQ     0005    ENQUIRY (ENQ)
#  AK     0006    ACKNOWLEDGE (ACK)
#  BL     0007    BELL (BEL)
#  BS     0008    BACKSPACE (BS)
#  HT     0009    CHARACTER TABULATION (HT)
#  LF     000a    LINE FEED (LF)
#  VT     000b    LINE TABULATION (VT)
#  FF     000c    FORM FEED (FF)
#  CR     000d    CARRIAGE RETURN (CR)
#  SO     000e    SHIFT OUT (SO)
#  SI     000f    SHIFT IN (SI)
#  DL     0010    DATALINK ESCAPE (DLE)
#  D1     0011    DEVICE CONTROL ONE (DC1)
#  D2     0012    DEVICE CONTROL TWO (DC2)
#  D3     0013    DEVICE CONTROL THREE (DC3)
#  D4     0014    DEVICE CONTROL FOUR (DC4)
#  NK     0015    NEGATIVE ACKNOWLEDGE (NAK)
#  SY     0016    SYNCRONOUS IDLE (SYN)
#  EB     0017    END OF TRANSMISSION BLOCK (ETB)
#  CN     0018    CANCEL (CAN)
#  EM     0019    END OF MEDIUM (EM)
#  SB     001a    SUBSTITUTE (SUB)
#  EC     001b    ESCAPE (ESC)
#  FS     001c    FILE SEPARATOR (IS4)
#  GS     001d    GROUP SEPARATOR (IS3)
#  RS     001e    RECORD SEPARATOR (IS2)
#  US     001f    UNIT SEPARATOR (IS1)
#  DT     007f    DELETE (DEL)
#  PA     0080    PADDING CHARACTER (PAD)
#  HO     0081    HIGH OCTET PRESET (HOP)
#  BH     0082    BREAK PERMITTED HERE (BPH)
#  NH     0083    NO BREAK HERE (NBH)
#  IN     0084    INDEX (IND)
#  NL     0085    NEXT LINE (NEL)
#  SA     0086    START OF SELECTED AREA (SSA)
#  ES     0087    END OF SELECTED AREA (ESA)
#  HS     0088    CHARACTER TABULATION SET (HTS)
#  HJ     0089    CHARACTER TABULATION WITH JUSTIFICATION (HTJ)
#  VS     008a    LINE TABULATION SET (VTS)
#  PD     008b    PARTIAL LINE FORWARD (PLD)
#  PU     008c    PARTIAL LINE BACKWARD (PLU)
#  RI     008d    REVERSE LINE FEED (RI)
#  S2     008e    SINGLE-SHIFT TWO (SS2)
#  S3     008f    SINGLE-SHIFT THREE (SS3)
#  DC     0090    DEVICE CONTROL STRING (DCS)
#  P1     0091    PRIVATE USE ONE (PU1)
#  P2     0092    PRIVATE USE TWO (PU2)
#  TS     0093    SET TRANSMIT STATE (STS)
#  CC     0094    CANCEL CHARACTER (CCH)
#  MW     0095    MESSAGE WAITING (MW)
#  SG     0096    START OF GUARDED AREA (SPA)
#  EG     0097    END OF GUARDED AREA (EPA)
#  SS     0098    START OF STRING (SOS)
#  GC     0099    SINGLE GRAPHIC CHARACTER INTRODUCER (SGCI)
#  SC     009a    SINGLE CHARACTER INTRODUCER (SCI)
#  CI     009b    CONTROL SEQUENCE INTRODUCER (CSI)
#  ST     009c    STRING TERMINATOR (ST)
#  OC     009d    OPERATING SYSTEM COMMAND (OSC)
#  PM     009e    PRIVACY MESSAGE (PM)
#  AC     009f    APPLICATION PROGRAM COMMAND (APC)
#         e000    indicates unfinished (Mnemonic)
#  /c     e001    JOIN THIS LINE WITH NEXT LINE (Mnemonic)
#  UA     e002    Unit space A (ISO-IR-8-1 064)
#  UB     e003    Unit space B (ISO-IR-8-1 096)
#  "3     e004    NON-SPACING UMLAUT (ISO-IR-38 201) (character part)
#  "1     e005    NON-SPACING DIAERESIS WITH ACCENT (ISO-IR-70 192)
#                 (character part)
#  "!     e006    NON-SPACING GRAVE ACCENT (ISO-IR-103 193) (character part)
#  "'     e007    NON-SPACING ACUTE ACCENT (ISO-IR-103 194) (character
#                 part)
#  ">     e008    NON-SPACING CIRCUMFLEX ACCENT (ISO-IR-103 195)
#                 (character part)
#  "?     e009    NON-SPACING TILDE (ISO-IR-103 196) (character part)
#  "-     e00a    NON-SPACING MACRON (ISO-IR-103 197) (character part)
#  "(     e00b    NON-SPACING BREVE (ISO-IR-103 198) (character part)
#  ".     e00c    NON-SPACING DOT ABOVE (ISO-IR-103 199) (character part)
#  ":     e00d    NON-SPACING DIAERESIS (ISO-IR-103 200) (character part)
#  "0     e00e    NON-SPACING RING ABOVE (ISO-IR-103 202) (character part)
#  ""     e00f    NON-SPACING DOUBLE ACCUTE (ISO-IR-103 204) (character
#                 part)
#  "<     e010    NON-SPACING CARON (ISO-IR-103 206) (character part)
#  ",     e011    NON-SPACING CEDILLA (ISO-IR-103 203) (character part)
#  ";     e012    NON-SPACING OGONEK (ISO-IR-103 206) (character part)
#  "_     e013    NON-SPACING LOW LINE (ISO-IR-103 204) (character
#                 part)
#  "=     e014    NON-SPACING DOUBLE LOW LINE (ISO-IR-38 217) (character
#                 part)
#  "/     e015    NON-SPACING LONG SOLIDUS (ISO-IR-128 201) (character
#                 part)
#  "i     e016    GREEK NON-SPACING IOTA BELOW (ISO-IR-55 39) (character
#                 part)
#  "d     e017    GREEK NON-SPACING DASIA PNEUMATA (ISO-IR-55 38)
#                 (character part)
#  "p     e018    GREEK NON-SPACING PSILI PNEUMATA (ISO-IR-55 37)
#                 (character part)
#  ;;     e019    GREEK DASIA PNEUMATA (ISO-IR-18 92)
#  ,,     e01a    GREEK PSILI PNEUMATA (ISO-IR-18 124)
#  b3     e01b    GREEK SMALL LETTER MIDDLE BETA (ISO-IR-18 99)
#  Ci     e01c    CIRCLE (ISO-IR-83 0294)
#  f(     e01d    FUNCTION SIGN (ISO-IR-143 221)
#  ed     e01e    LATIN SMALL LETTER EZH (ISO-IR-158 142)
#  am     e01f    ANTE MERIDIAM SIGN (ISO-IR-149 0267)
#  pm     e020    POST MERIDIAM SIGN (ISO-IR-149 0268)
#  Tel    e021    TEL COMPATIBILITY SIGN (ISO-IR-149 0269)
#  a+:    e022    ARABIC LETTER ALEF FINAL FORM COMPATIBILITY (IBM868 144)
#  Fl     e023    DUTCH GUILDER SIGN (IBM437 159)
#  GF     e024    GAMMA FUNCTION SIGN (ISO-10646-1DIS 032/032/037/122)
#  >V     e025    RIGHTWARDS VECTOR ABOVE (ISO-10646-1DIS 032/032/038/046)
#  !*     e026    GREEK VARIA (ISO-10646-1DIS 032/032/042/164)
#  ?*     e027    GREEK PERISPOMENI (ISO-10646-1DIS 032/032/042/165)
#  J<     e028    LATIN CAPITAL LETTER J WITH CARON (lowercase: 000/000/001/240)


class Executor:
    """ Класс, выполняющий запросы """

    def __init__(self, session_id: str, uuid: str, url: str, timeout: Union[str, float, int]):
        """
        Инициализация класса Executor
        :param session_id: session_id
        :param uuid: (manager) uuid
        :param timeout: таймауты запросов
        """
        self.query = {
            "uuid": uuid,
            "command": "your command"
        }
        self.session_id = session_id
        self.base_url = url
        self.timeout = timeout

    def execute_request(self, params: Union[Dict, str], method: str = "POST") -> [
            requests.models.Response, Dict, str]:
        """
        выполнить запрос
        :param params: (Dict) запрос - для метода POST
                        (str) URL файла для метода GET
        :param method: (str) "POST" / "GET" / "PUT"
        :return: (Dict) ответ сервера
        """
        # преобразование параметров (dict) к параметрам (str)
        # для избежания проблемы с чтением true/false (json-формат)
        json_params = json.dumps(params)

        if method == "GET":
            # выкачать файл GET-запросом

            # имя cookies: session (для скачивания файла)
            cookies = {'session': self.session_id}

            # выкачать файл GET-запросом
            r = requests.request(method="GET", url=params, cookies=cookies, timeout=self.timeout)
            return r
        elif method == "PUT":
            cookies = {'session': self.session_id}
            with open(params, 'rb') as file:
                r = requests.put(self.base_url + "/upload.php?",
                                 data=file,
                                 cookies=cookies,
                                 headers={
                                     'content-type': 'application/octet-stream',
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'Upload-Position': "0",
                                     'Last-Part': "1"
                                        })
            return r
        else:
            # Request headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'text/plain'
            }

            # parse request queries
            request_queries = params.get("queries")
            request_queries = next(iter(request_queries))
            request_command = request_queries.get("command")
            request_code = request_command.get("plm_type_code")
            request_state = request_command.get("state")

            # для следующих операций передавать запрос в виде строки с кодировкой utf-8
            # (т.к. в запросе могут быть русские буквы)
            # command: 502 (dimension), state: 5 (rename)
            if request_code == 502 and request_state == 5:
                params = str(params)
                params = params.replace("'", "\"")
                headers = {
                    "Content-Type": "text/plain",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "X-Requested-With": "XMLHttpRequest"
                }
                r = requests.post(url=self.base_url, headers=headers, data=params.encode("utf-8"))
            # command: 503 (fact), state: 24 (rename)
            # command: 505 (group), state: 4 (set_name)
            elif (request_code == 503 and request_state == 24) \
                    or (request_code == 505 and request_state == 4):
                params = str(params)
                params = params.replace("'", "\"")
                headers.update({"Content-Type": "text/plain"})
                r = requests.post(url=self.base_url, headers=headers, data=params.encode('utf-8'))
            # для следующих операций передавать запрос в виде строки с кодировкой utf-8
            # (т.к. в запросе могут быть русские буквы)
            # И заменять ключевые слова Python False, True и None на соответствующие значения json: false, true, null
            # command: 503 (fact), state: 4 (create_calc)
            # command: 502 (dimension), state: 11 (create_calc)
            # command: 208 (user_cube), state: 30 (save_ext_info_several_sources_request)
            # command: 208 (user_cube), state: 12 (test_source_connection_request)
            # command: 208 (user_cube), state: 14 (data_preview_request)
            # command: 208 (user_cube), state: 42 (get_fields_request)
            # command: 208 (user_cube), state: 44 (create_cube_request)
            elif (request_code == 503 and request_state == 4) \
                    or (request_code == 502 and request_state == 11) \
                    or (request_code == 208 and request_state == 30) \
                    or (request_code == 208 and request_state == 12) \
                    or (request_code == 208 and request_state == 14) \
                    or (request_code == 208 and request_state == 42) \
                    or (request_code == 208 and request_state == 44):
                old_params = params
                params = str(params)
                new_param = ""
                for elem in params:
                    if elem == "'":
                        new_param += "\""
                        continue
                    if elem == "\"":
                        new_param += "'"
                        continue
                    new_param += elem
                new_param = new_param.replace("False", "false")
                new_param = new_param.replace("True", "true")
                new_param = new_param.replace("None", "null")
                headers.update({"Content-Type": "text/plain"})

                # Для следующих операций используются свои headers
                # command: 208 (user_cube), state: 14 (data_preview_request)
                # command: 208 (user_cube), state: 42 (get_fields_request)
                # command: 208 (user_cube), state: 44 (create_cube_request)
                if (request_state == 42) or (request_state == 44) or (request_state == 14):
                    headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                r = requests.request(method="POST", url=self.base_url, headers=headers, data=new_param.encode('utf-8'),
                                     timeout=self.timeout)
            # для остальных случае передавать data в формате json
            else:
                r = requests.request(method="POST", url=self.base_url, headers=headers, data=json_params,
                                     timeout=self.timeout)
            # Check for invalid control characters in response
            try:
                response = r.json()

            except json.decoder.JSONDecodeError as e:
                logging.exception("EXCEPTION!!! json.decoder.JSONDecodeError:")
                logging.exception(e)
                str_response = r.text
                for i in INVALID_CONTROL_CHARACTERS:
                    str_response = str_response.replace(i, '')
                json_acceptable_string = str_response.replace("'", "\"")
                response = json.loads(json_acceptable_string)
                error_handler.request_asserts(response, r)
                return response

            error_handler.request_asserts(response, r)
            return response
