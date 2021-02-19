"""
@author  : MG
@Time    : 2021/1/26 14:57
@File    : qq_email.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
import mimetypes
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

logger = logging.getLogger()


def build_email(from_mail, to_mail_list, subject, attach_file_paths: Optional[Union[list, dict]] = None):
    msg = MIMEMultipart()
    msg["Subject"] = Header(subject, "utf-8")
    # msg["From"] = Header(from_mail, "utf-8")
    msg["From"] = from_mail
    # msg["To"] = Header(",".join(to_mail_list), "utf-8")
    msg["To"] = ",".join(to_mail_list)

    if attach_file_paths is not None:
        if isinstance(attach_file_paths, list):
            for attach_file_path in attach_file_paths:
                ctype, encoding = mimetypes.guess_type(attach_file_path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)
                print("maintype, subtype", maintype, subtype)
                if maintype == 'text':
                    with open(attach_file_path) as f:
                        mime = MIMEText(f.read(), _subtype=subtype)
                elif maintype == 'image':
                    with open(attach_file_path, 'rb') as f:
                        mime = MIMEImage(f.read(), _subtype=subtype)
                elif maintype == 'audio':
                    with open(attach_file_path, 'rb') as f:
                        mime = MIMEAudio(f.read(), _subtype=subtype)
                else:
                    with open(attach_file_path, 'rb') as f:
                        mime = MIMEBase(maintype, subtype)
                        mime.set_payload(f.read())

                encoders.encode_base64(mime)
                _, file_name = os.path.split(attach_file_path)
                mime.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(mime)
        elif isinstance(attach_file_paths, dict):
            maintype, subtype = "application", "vnd.ms-excel"
            for table_name, io in attach_file_paths.items():
                file_name = f'{table_name}.csv'
                mime = MIMEBase(maintype, subtype)
                mime.set_payload(io.getvalue())
                encoders.encode_base64(mime)
                mime.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(mime)

        else:
            raise ValueError(f"不支持 attach_file_paths <{type(attach_file_paths)}>")

    return msg


def send_email_qq(from_mail, to_mail_list, password, msg):
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    try:
        smtp.ehlo()
        # smtp.starttls()
        smtp.login(from_mail, password)
        smtp.sendmail(from_mail, to_mail_list, msg.as_string())
    except smtplib.SMTPException as e:
        logger.exception("发送邮件异常")
    finally:
        smtp.quit()


if __name__ == "__main__":
    pass
