# pylint: disable = abstract-method
from opencensus.ext.azure.log_exporter import AzureLogHandler, Envelope, Message  # pylint: disable = unused-import
from loggerbundle.extra.ExtraKeysResolver import ExtraKeysResolver

class AzureLogWithExtraHandler(AzureLogHandler):

    def log_record_to_envelope(self, record):
        envelope = super().log_record_to_envelope(record) # type: Envelope

        message = envelope.data.baseData # type: Message

        recordDict = record.__dict__
        extraKeys = ExtraKeysResolver.getExtraKeys(record)

        message.properties['loggerName'] = record.name

        for k in extraKeys:
            if k != 'message':
                message.properties['extra_{}'.format(k)] = str(recordDict[k])

        return envelope
