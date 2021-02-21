import os
from pathlib import Path
from bikesanity.processing.publish_journal import PublishJournal, PublicationFormats
from bikesanity.io_utils.log_handler import init_logging, log


BASE_DIRECTORY = 'CycleSanityJournals'
base_path = os.path.join(Path.home(), BASE_DIRECTORY)

input_path = base_path
output_path = base_path

journal_id = '14924'

init_logging()

journal_publisher = PublishJournal(input_path, output_path, journal_id)
journal_publisher.publish_journal_id(PublicationFormats.PDF)
