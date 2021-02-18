import base64
import email
from email import generator
from email.message import MIMEPart
from email.mime.message import MIMEMessage
import logging
from os.path import join
import re
from typing import List, Union, Tuple, Iterator

ANONYMISED_SUFFIX = "_anon"
"""The suffix to put on a file that has been anonymised."""

EMAIL_PATTERN = "<(.*?)>"
"""A regex pattern to get the RFC5322 addr-spec from an email address string.
Even with an optional display-name present."""


def preprocess_mime_message(mime_message: str) -> str:
    """The MIME message contained in the blob storage has characters escaped, as
    well as quotation marks surrounding. This is gonna mess up the MIME parsing,
    so we want to make sure this stuff is all straightened out.

    Args:
        mime_message (str): The MIME message to process.

    Returns:
        str: The preprocessed MIME message.
    """
    # trim quotation marks surrounding
    mime_message = mime_message[1:len(mime_message) - 1]

    # unescape escaped chars
    mime_message = mime_message.replace("\\n", "\n").replace(
        "\\\"", "\"").replace("\\t", "\t").replace("3D\"",
                                                   "\"")  #.replace("=\n", "")

    return mime_message


def write_message(output_dir: str,
                  transaction_id: str,
                  message: MIMEMessage,
                  suffix: str = "") -> None:
    """Write a message to an EML file in a given location.

    This is useful for if you want to open a reconstructed email in outlook.

    Args:
        output_dir (str): The directory to write the file to.
        transaction_id (str): The transaction ID of the email.
        message (MIMEMessage): The parsed MIME message to write.
        suffix (str): The suffix to add to the filename.
    """
    filename = transaction_id + suffix + ".eml"
    logging.info(f"    Writing message '{filename}'")
    with open(join(output_dir, filename), "w") as eml_file:
        gen = generator.Generator(eml_file)
        gen.flatten(message)


def write_attachment(output_dir: str, transaction_id: str,
                     part: MIMEPart) -> None:
    """Write an attachment file to disk.

    Args:
        output_dir (str): The directory to write the file to.
        transaction_id (str): The transaction ID of the email.
        part (MIMEPart): The MIME part representing the attachment.
    """
    filename = f"{transaction_id}_{part.get_filename()}"
    logging.info(f"    Writing attachment '{filename}'")
    with open(join(output_dir, filename), "wb") as attachment_file:
        decoded = base64.b64decode(part.get_payload())
        attachment_file.write(decoded)


def write_html(output_dir: str, transaction_id: str, part: MIMEPart) -> None:
    """Write the HTML part of an email to disk.

    Args:
        output_dir (str): The directory to write the file to.
        transaction_id (str): The transaction ID of the email.
        part (MIMEPart): The MIME part representing the attachment.
    """
    filename = f"{transaction_id}_html.html"
    logging.info(f"    Writing email body '{filename}'")
    with open(join(output_dir, filename), "w") as body_file:
        # the replace is due to weird formatting of HTML in MIME
        body_file.write(part.get_payload().replace("=\n", ""))


def anonymise_mime_message(msg: MIMEMessage) -> MIMEMessage:
    """Replace all of the sensitive fields in the MIME message with messages
    indicating that this message has been anonymised.

    The fields that get replaced are "Subject", "Thread-Topic", as well as the
    body of the email. Attachments are preserved.
    """
    msg.replace_header("Subject", "The subject has been removed for anonymity")

    # the thread topic isn't always present
    if msg.get("Thread-Topic") is not None:
        msg.replace_header("Thread-Topic",
                           "The topic has been removed for anonymity")

    for part in msg.walk():
        # the only parts that contain the body are text/html and text/plain
        # TODO(sam): I think sometimes these can be encoded as base64?
        #            Might need special handling...
        if part.get_content_type() == "text/html" \
                or part.get_content_type() == "text/plain":
            if not is_file(part):
                part.set_payload("The body has been removed for anonymity")

    return msg


def is_file(part: MIMEPart) -> bool:
    """Return True if this MIMEPart is attached as a file."""
    disposition = part.get_content_disposition()
    return disposition == "inline" or disposition == "attachment"


def is_html(part: MIMEPart) -> bool:
    """Return True if this MIMEPart is HTML."""
    return part.get_content_type() == "text/html"


def write_mime_message_payloads(
    output_dir: str,
    transaction_id: str,
    msg: MIMEMessage,
):
    """For each payload in the MIME message, write out the ones that are
    attached as files.

    Args:
        msg (MIMEMessage): The parsed MIME message.
        transaction_id (str): The transaction ID of the email.
        output_dir (str): The directory to write the payloads in.
    """
    for part in msg.walk():
        if is_html(part) and not is_file(part):
            write_html(output_dir, transaction_id, part)

            # for some reason, outlook doesn't like EML files with HTML in them,
            # so we blank out the HTML payload here to display it correctly
            part.set_payload("")
        elif is_file(part):
            write_attachment(output_dir, transaction_id, part)


def process_mime_message(mime_message: str,
                         transaction_id: str,
                         output_dir: str,
                         anonymise: bool = False) -> None:
    """Process a MIME message, writing it and its attachments to files.

    Args:
        mime_message (str): The MIME message as a string.
        transaction_id (str): The transaction ID of the email.
        output_dir (str): The dir to put files in.
        anonymise (bool): Whether to write an anonymised version of the email too.
    """
    logging.info(f"--> Processing message for transaction '{transaction_id}'")
    preprocessed_msg = preprocess_mime_message(mime_message)
    parsed_msg = email.message_from_string(preprocessed_msg)

    # write the email to a file
    write_message(output_dir, transaction_id, parsed_msg)

    # write the email attachments to files
    write_mime_message_payloads(output_dir, transaction_id, parsed_msg)

    if anonymise:
        # anonymise the message and write it to the output dir
        anonymised_msg = anonymise_mime_message(parsed_msg)
        write_message(output_dir,
                      transaction_id,
                      anonymised_msg,
                      suffix=ANONYMISED_SUFFIX)


def extract_emails(addrs: str) -> List[str]:
    return re.findall(EMAIL_PATTERN, addrs)


def filter_by_organisation(addrs: Iterator[str],
                           organisation: str) -> Iterator[str]:
    return [addr for addr in addrs if addr.endswith(organisation)]


def normalise_addresses(addrs: Iterator[str]) -> Iterator[str]:
    return [addr.lower() for addr in addrs]


def get_to_addresses(
        mime_message: str,
        organisation_url: Union[str, None] = "") -> Tuple[List[str], bool]:
    if organisation_url is None:
        organisation_url = ""

    preprocessed_msg = preprocess_mime_message(mime_message)
    parsed_msg = email.message_from_string(preprocessed_msg)

    # extract the to addresses
    to_emails = []
    if parsed_msg.get("To") is not None:
        to_emails += extract_emails(parsed_msg["To"])

    # extract the Cc addresses
    if parsed_msg.get("Cc") is not None:
        to_emails += extract_emails(parsed_msg["Cc"])

    # extract the from addresses
    from_emails = []
    if parsed_msg.get("From") is not None:
        from_emails += extract_emails(parsed_msg["From"])

    # filter them by organisation, if the length after filter is > 0, then it's internal
    # as we already know at least one recipient is in the organisation (or we wouldn't have it!)
    from_emails = filter_by_organisation(from_emails, organisation_url)
    is_internal = len(from_emails) > 0

    # filter by the organisation URL
    return (normalise_addresses(
        filter_by_organisation(to_emails, organisation_url)), is_internal)
