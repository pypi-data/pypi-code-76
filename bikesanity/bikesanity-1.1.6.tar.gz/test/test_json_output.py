import os
from pathlib import Path
from bikesanity.processing.publish_journal import PublishJournal, PublicationFormats


BASE_DIRECTORY = 'CycleSanityJournals'
base_path = os.path.join(Path.home(), BASE_DIRECTORY)

input_path = base_path
output_path = base_path

journal_id = '23353'

journal_publisher = PublishJournal(input_path, output_path, journal_id)
journal_publisher.publish_journal_id(PublicationFormats.JSON_MODEL)
