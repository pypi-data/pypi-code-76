from datetime import datetime

ALLOWED_ASSET_TYPES = [
    'ip', 'ipv4', 'ipv6',
    'domain', 'fqdn',
    'url',
    'keyword'
]

ALLOWED_ASSET_EXPOSURES = [
    'external', 'internal', 'restricted', 'unknown'
]

class Asset():
    def __init__(self, value="", type="keyword", exposure='unknown', tags=[], raw={}):
        if str(type).lower() not in ALLOWED_ASSET_TYPES:
            raise Exception("Bad asset type.")
        if str(exposure).lower() not in ALLOWED_ASSET_EXPOSURES:
            raise Exception("Bad asset exposure.")
        self.type = str(type).lower()
        self.value = value
        self.exposure = exposure
        self.tags = tags
        self.raw = raw


    def __str__(self):
        return f"{self.type}:{self.value}"

    def __dict__(self):
        return {
            'value': self.value,
            'type': self.type,
            'exposure': self.exposure,
            'tags': self.tags,
            'raw': self.raw
        }

    def to_csv(self, delimiter=';'):
        return [
            self.value,  # asset_value
            self.value,  # asset_name
            self.type,  # asset_type
            f"Synced with PatrowlAssets: {self.value}",  # asset_description
            'low',  # asset_criticity
            ','.join(self.tags),  # asset_tags
            '', # owner
            '', # team
            self.exposure, # asset_exposure
            str(datetime.now())
        ]
