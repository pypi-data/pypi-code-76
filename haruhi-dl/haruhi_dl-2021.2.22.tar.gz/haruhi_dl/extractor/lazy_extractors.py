# coding: utf-8
# flake8: noqa
from __future__ import unicode_literals

import re


class LazyLoadExtractor(object):
    _module = None

    @classmethod
    def ie_key(cls):
        return cls.__name__[:-2]

    def __new__(cls, *args, **kwargs):
        mod = __import__(cls._module, fromlist=(cls.__name__,))
        real_cls = getattr(mod, cls.__name__)
        instance = real_cls.__new__(real_cls)
        instance.__init__(*args, **kwargs)
        return instance


    # suitable() inserts below
    @classmethod
    def suitable(cls, url):
        """Receives a URL and returns True if suitable for this IE."""

        # This does not use has/getattr intentionally - we want to know whether
        # we have cached the regexp for *this* class, whereas getattr would also
        # match the superclass
        if '_VALID_URL_RE' not in cls.__dict__:
            cls._VALID_URL_RE = re.compile(cls._VALID_URL)
        return cls._VALID_URL_RE.match(url) is not None



class LazyLoadSearchExtractor(LazyLoadExtractor):
    pass


class LazyLoadSelfhostedExtractor(LazyLoadExtractor):

    # suitable_selfhosted() inserts below
    @classmethod
    def suitable_selfhosted(cls, url, webpage):
        """Receives a URL and webpage contents, and returns True if suitable for this IE."""

        if cls._SH_VALID_URL:
            if '_SH_VALID_URL_RE' not in cls.__dict__:
                cls._SH_VALID_URL_RE = re.compile(cls._SH_VALID_URL)
            if cls._SH_VALID_URL_RE.match(url) is None:
                return False

        if webpage is None:
            # if no webpage, assume just matching the URL is fine
            if cls._SH_VALID_URL:
                return True
            # failing, there's nothing more to check
            return False

        if any(p in webpage for p in (cls._SH_VALID_CONTENT_STRINGS or ())):
            return True

        # no strings? check regexes!
        if '_SH_CONTENT_REGEXES_RES' not in cls.__dict__:
            cls._SH_VALID_CONTENT_REGEXES_RES = (re.compile(rgx)
                                                 for rgx in cls._SH_VALID_CONTENT_REGEXES or ())
        if not any(rgx.match(webpage) is not None for rgx in cls._SH_VALID_CONTENT_REGEXES_RES):
            return False



class ABCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?abc\\.net\\.au/news/(?:[^/]+/){1,2}(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.abc'


class ABCIViewIE(LazyLoadExtractor):
    _VALID_URL = 'https?://iview\\.abc\\.net\\.au/(?:[^/]+/)*video/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.abc'


class AbcNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://abcnews\\.go\\.com/(?:[^/]+/)+(?P<display_id>[0-9a-z-]+)/story\\?id=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.abcnews'


class AMPIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.amp'


class AbcNewsVideoIE(AMPIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            abcnews\\.go\\.com/\n                            (?:\n                                [^/]+/video/(?P<display_id>[0-9a-z-]+)-|\n                                video/embed\\?.*?\\bid=\n                            )|\n                            fivethirtyeight\\.abcnews\\.go\\.com/video/embed/\\d+/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.abcnews'


class ABCOTVSIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<site>abc(?:7(?:news|ny|chicago)?|11|13|30)|6abc)\\.com(?:(?:/[^/]+)*/(?P<display_id>[^/]+))?/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.abcotvs'


class ABCOTVSClipsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://clips\\.abcotvs\\.com/(?:[^/]+/)*video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.abcotvs'


class AcademicEarthCourseIE(LazyLoadExtractor):
    _VALID_URL = '^https?://(?:www\\.)?academicearth\\.org/playlists/(?P<id>[^?#/]+)'
    _module = 'haruhi_dl.extractor.academicearth'


class ACastIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:embed|www)\\.)?acast\\.com/|\n                            play\\.acast\\.com/s/\n                        )\n                        (?P<channel>[^/]+)/(?P<id>[^/#?]+)\n                    '
    _module = 'haruhi_dl.extractor.acast'


class ACastChannelIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?acast\\.com/|\n                            play\\.acast\\.com/s/\n                        )\n                        (?P<id>[^/#?]+)\n                    '
    _module = 'haruhi_dl.extractor.acast'

    @classmethod
    def suitable(cls, url):
        return False if ACastIE.suitable(url) else super(ACastChannelIE, cls).suitable(url)


class ADNIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?animedigitalnetwork\\.fr/video/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.adn'


class AdobeConnectIE(LazyLoadExtractor):
    _VALID_URL = 'https?://\\w+\\.adobeconnect\\.com/(?P<id>[\\w-]+)'
    _module = 'haruhi_dl.extractor.adobeconnect'


class AdobeTVBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVEmbedIE(AdobeTVBaseIE):
    _VALID_URL = 'https?://tv\\.adobe\\.com/embed/\\d+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVIE(AdobeTVBaseIE):
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?watch/(?P<show_urlname>[^/]+)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVPlaylistBaseIE(AdobeTVBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVShowIE(AdobeTVPlaylistBaseIE):
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?show/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVChannelIE(AdobeTVPlaylistBaseIE):
    _VALID_URL = 'https?://tv\\.adobe\\.com/(?:(?P<language>fr|de|es|jp)/)?channel/(?P<id>[^/]+)(?:/(?P<category_urlname>[^/]+))?'
    _module = 'haruhi_dl.extractor.adobetv'


class AdobeTVVideoIE(AdobeTVBaseIE):
    _VALID_URL = 'https?://video\\.tv\\.adobe\\.com/v/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.adobetv'


class AdobePassIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.adobepass'


class TurnerBaseIE(AdobePassIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.turner'


class AdultSwimIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?adultswim\\.com/videos/(?P<show_path>[^/?#]+)(?:/(?P<episode_path>[^/?#]+))?'
    _module = 'haruhi_dl.extractor.adultswim'


class AfreecaTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:live|afbbs|www)\\.)?afreeca(?:tv)?\\.com(?::\\d+)?\n                            (?:\n                                /app/(?:index|read_ucc_bbs)\\.cgi|\n                                /player/[Pp]layer\\.(?:swf|html)\n                            )\\?.*?\\bnTitleNo=|\n                            vod\\.afreecatv\\.com/PLAYER/STATION/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.afreecatv'


class TokFMAuditionIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://audycje\\.tokfm\\.pl/audycja/|tokfm:audition:)(?P<id>\\d+),?'
    _module = 'haruhi_dl.extractor.agora'


class TokFMPodcastIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://audycje\\.tokfm\\.pl/podcast/|tokfm:podcast:)(?P<id>\\d+),?'
    _module = 'haruhi_dl.extractor.agora'


class WyborczaPodcastIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?\n            (?:wyborcza\\.pl/podcast(?:/0,172673\\.html)?\n            |wysokieobcasy\\.pl/wysokie-obcasy/0,176631\\.html)\n        (?:\\?(?:[^&]+?&)*?podcast=(?P<episode_id>\\d+))?\n    '
    _module = 'haruhi_dl.extractor.agora'


class WyborczaVideoIE(LazyLoadExtractor):
    _VALID_URL = 'wyborcza:video:(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.agora'


class AirMozillaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://air\\.mozilla\\.org/(?P<id>[0-9a-z-]+)/?'
    _module = 'haruhi_dl.extractor.airmozilla'


class AlbiclaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://albicla\\.com/[a-zA-Z\\d]+/post/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.albicla'


class AlJazeeraIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?aljazeera\\.com/(?:programmes|video)/.*?/(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.aljazeera'


class AlphaPornoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?alphaporno\\.com/videos/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.alphaporno'


class AmericasTestKitchenIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?americastestkitchen\\.com/(?:episode|videos)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.americastestkitchen'


class AnimeOnDemandIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?anime-on-demand\\.de/anime/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.animeondemand'


class AnvatoIE(LazyLoadExtractor):
    _VALID_URL = 'anvato:(?P<access_key_or_mcp>[^:]+):(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.anvato'


class AolIE(LazyLoadExtractor):
    _VALID_URL = '(?:aol-video:|https?://(?:www\\.)?aol\\.(?:com|ca|co\\.uk|de|jp)/video/(?:[^/]+/)*)(?P<id>[0-9a-f]+)'
    _module = 'haruhi_dl.extractor.aol'


class AllocineIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?allocine\\.fr/(?:article|video|film)/(?:fichearticle_gen_carticle=|player_gen_cmedia=|fichefilm_gen_cfilm=|video-)(?P<id>[0-9]+)(?:\\.html)?'
    _module = 'haruhi_dl.extractor.allocine'


class AliExpressLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://live\\.aliexpress\\.com/live/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.aliexpress'


class AliExpressProductIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|[a-z]{2})\\.)?aliexpress\\.(?:com|ru)/item/(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.aliexpress'


class APAIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[^/]+\\.apa\\.at/embed/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.apa'


class AparatIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?aparat\\.com/(?:v/|video/video/embed/videohash/)(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.aparat'


class AppleConnectIE(LazyLoadExtractor):
    _VALID_URL = 'https?://itunes\\.apple\\.com/\\w{0,2}/?post/idsa\\.(?P<id>[\\w-]+)'
    _module = 'haruhi_dl.extractor.appleconnect'


class AppleTrailersIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.|movie)?trailers\\.apple\\.com/(?:trailers|ca)/(?P<company>[^/]+)/(?P<movie>[^/]+)'
    _module = 'haruhi_dl.extractor.appletrailers'


class AppleTrailersSectionIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?trailers\\.apple\\.com/#section=(?P<id>justadded|exclusive|justhd|mostpopular|moviestudios)'
    _module = 'haruhi_dl.extractor.appletrailers'


class ArchiveOrgIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?archive\\.org/(?:details|embed)/(?P<id>[^/?#]+)(?:[?].*)?$'
    _module = 'haruhi_dl.extractor.archiveorg'


class ArkenaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                video\\.arkena\\.com/play2/embed/player\\?|\n                                play\\.arkena\\.com/(?:config|embed)/avp/v\\d/player/media/(?P<id>[^/]+)/[^/]+/(?P<account_id>\\d+)\n                            )\n                        '
    _module = 'haruhi_dl.extractor.arkena'


class ARDMediathekBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ard'


class ARDBetaMediathekIE(ARDMediathekBaseIE):
    _VALID_URL = 'https://(?:(?:beta|www)\\.)?ardmediathek\\.de/(?P<client>[^/]+)/(?:player|live|video)/(?P<display_id>(?:[^/]+/)*)(?P<video_id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.ard'


class ARDIE(LazyLoadExtractor):
    _VALID_URL = '(?P<mainurl>https?://(www\\.)?daserste\\.de/[^?#]+/videos(?:extern)?/(?P<display_id>[^/?#]+)-(?P<id>[0-9]+))\\.html'
    _module = 'haruhi_dl.extractor.ard'


class ARDMediathekIE(ARDMediathekBaseIE):
    _VALID_URL = '^https?://(?:(?:(?:www|classic)\\.)?ardmediathek\\.de|mediathek\\.(?:daserste|rbb-online)\\.de|one\\.ard\\.de)/(?:.*/)(?P<video_id>[0-9]+|[^0-9][^/\\?]+)[^/\\?]*(?:\\?.*)?'
    _module = 'haruhi_dl.extractor.ard'

    @classmethod
    def suitable(cls, url):
        return False if ARDBetaMediathekIE.suitable(url) else super(ARDMediathekIE, cls).suitable(url)


class ArteTVBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.arte'


class ArteTVPlus7IE(ArteTVBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?arte\\.tv/(?P<lang>fr|de|en|es|it|pl)/videos/(?P<id>\\d{6}-\\d{3}-[AF])'
    _module = 'haruhi_dl.extractor.arte'


class ArteTVEmbedIE(ArteTVPlus7IE):
    _VALID_URL = '(?x)\n        https://www\\.arte\\.tv\n        /player/v3/index\\.php\\?json_url=\n        (?P<json_url>\n            https?://api\\.arte\\.tv/api/player/v1/config/\n            (?P<lang>[^/]+)/(?P<id>\\d{6}-\\d{3}-[AF])\n        )\n    '
    _module = 'haruhi_dl.extractor.arte'


class ArteTVPlaylistIE(ArteTVBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?arte\\.tv/(?P<lang>fr|de|en|es|it|pl)/videos/(?P<id>RC-\\d{6})'
    _module = 'haruhi_dl.extractor.arte'


class AsianCrushIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>(?:(?:asiancrush|yuyutv|midnightpulp)\\.com|cocoro\\.tv))/video/(?:[^/]+/)?0+(?P<id>\\d+)v\\b'
    _module = 'haruhi_dl.extractor.asiancrush'


class AsianCrushPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>(?:(?:asiancrush|yuyutv|midnightpulp)\\.com|cocoro\\.tv))/series/0+(?P<id>\\d+)s\\b'
    _module = 'haruhi_dl.extractor.asiancrush'


class AtresPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?atresplayer\\.com/[^/]+/[^/]+/[^/]+/[^/]+/(?P<display_id>.+?)_(?P<id>[0-9a-f]{24})'
    _module = 'haruhi_dl.extractor.atresplayer'


class ATTTechChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://techchannel\\.att\\.com/play-video\\.cfm/([^/]+/)*(?P<id>.+)'
    _module = 'haruhi_dl.extractor.atttechchannel'


class ATVAtIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?atv\\.at/(?:[^/]+/){2}(?P<id>[dv]\\d+)'
    _module = 'haruhi_dl.extractor.atvat'


class AudiMediaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?audi-mediacenter\\.com/(?:en|de)/audimediatv/(?:video/)?(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.audimedia'


class AudioBoomIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?audioboom\\.com/(?:boos|posts)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.audioboom'


class AudiomackIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?audiomack\\.com/song/(?P<id>[\\w/-]+)'
    _module = 'haruhi_dl.extractor.audiomack'


class AudiomackAlbumIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?audiomack\\.com/album/(?P<id>[\\w/-]+)'
    _module = 'haruhi_dl.extractor.audiomack'


class AWAANIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?show/(?P<show_id>\\d+)/[^/]+(?:/(?P<video_id>\\d+)/(?P<season_id>\\d+))?'
    _module = 'haruhi_dl.extractor.awaan'


class AWAANBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.awaan'


class AWAANVideoIE(AWAANBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?(?:video(?:/[^/]+)?|media|catchup/[^/]+/[^/]+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.awaan'


class AWAANLiveIE(AWAANBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?live/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.awaan'


class AWAANSeasonIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:awaan|dcndigital)\\.ae/(?:#/)?program/(?:(?P<show_id>\\d+)|season/(?P<season_id>\\d+))'
    _module = 'haruhi_dl.extractor.awaan'


class AZMedienIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?P<host>\n                            telezueri\\.ch|\n                            telebaern\\.tv|\n                            telem1\\.ch\n                        )/\n                        [^/]+/\n                        (?P<id>\n                            [^/]+-(?P<article_id>\\d+)\n                        )\n                        (?:\n                            \\#video=\n                            (?P<kaltura_id>\n                                [_0-9a-z]+\n                            )\n                        )?\n                    '
    _module = 'haruhi_dl.extractor.azmedien'


class BaiduVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://v\\.baidu\\.com/(?P<type>[a-z]+)/(?P<id>\\d+)\\.htm'
    _module = 'haruhi_dl.extractor.baidu'


class BandcampIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[^/]+\\.bandcamp\\.com/track/(?P<title>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.bandcamp'


class BandcampAlbumIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?P<subdomain>[^.]+)\\.)?bandcamp\\.com(?:/album/(?P<album_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.bandcamp'

    @classmethod
    def suitable(cls, url):
        return (False
                if BandcampWeeklyIE.suitable(url) or BandcampIE.suitable(url)
                else super(BandcampAlbumIE, cls).suitable(url))


class BandcampWeeklyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bandcamp\\.com/?\\?(?:.*?&)?show=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bandcamp'


class BBCCoUkIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?bbc\\.co\\.uk/\n                        (?:\n                            programmes/(?!articles/)|\n                            iplayer(?:/[^/]+)?/(?:episode/|playlist/)|\n                            music/(?:clips|audiovideo/popular)[/#]|\n                            radio/player/|\n                            sounds/play/|\n                            events/[^/]+/play/[^/]+/\n                        )\n                        (?P<id>(?:[pbm][\\da-z]{7}|w[\\da-z]{7,14}))(?!/(?:episodes|broadcasts|clips))\n                    '
    _module = 'haruhi_dl.extractor.bbc'


class BBCCoUkArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/articles/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.bbc'


class BBCCoUkPlaylistBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.bbc'


class BBCCoUkIPlayerPlaylistIE(BBCCoUkPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/iplayer/(?:episodes|group)/(?P<id>(?:[pbm][\\da-z]{7}|w[\\da-z]{7,14}))'
    _module = 'haruhi_dl.extractor.bbc'


class BBCCoUkPlaylistIE(BBCCoUkPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/(?P<id>(?:[pbm][\\da-z]{7}|w[\\da-z]{7,14}))/(?:episodes|broadcasts|clips)'
    _module = 'haruhi_dl.extractor.bbc'


class BBCIE(BBCCoUkIE):
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.(?:com|co\\.uk)/(?:[^/]+/)+(?P<id>[^/#?]+)'
    _module = 'haruhi_dl.extractor.bbc'

    @classmethod
    def suitable(cls, url):
        EXCLUDE_IE = (BBCCoUkIE, BBCCoUkArticleIE, BBCCoUkIPlayerPlaylistIE, BBCCoUkPlaylistIE)
        return (False if any(ie.suitable(url) for ie in EXCLUDE_IE)
                else super(BBCIE, cls).suitable(url))


class BeamProBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.beampro'


class BeamProLiveIE(BeamProBaseIE):
    _VALID_URL = 'https?://(?:\\w+\\.)?(?:beam\\.pro|mixer\\.com)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.beampro'

    @classmethod
    def suitable(cls, url):
        return False if BeamProVodIE.suitable(url) else super(BeamProLiveIE, cls).suitable(url)


class BeamProVodIE(BeamProBaseIE):
    _VALID_URL = 'https?://(?:\\w+\\.)?(?:beam\\.pro|mixer\\.com)/[^/?#&]+\\?.*?\\bvod=(?P<id>[^?#&]+)'
    _module = 'haruhi_dl.extractor.beampro'


class BeegIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?beeg\\.(?:com|porn(?:/video)?)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.beeg'


class BehindKinkIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?behindkink\\.com/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<id>[^/#?_]+)'
    _module = 'haruhi_dl.extractor.behindkink'


class BellMediaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?\n        (?P<domain>\n            (?:\n                ctv|\n                tsn|\n                bnn(?:bloomberg)?|\n                thecomedynetwork|\n                discovery|\n                discoveryvelocity|\n                sciencechannel|\n                investigationdiscovery|\n                animalplanet|\n                bravo|\n                mtv|\n                space|\n                etalk|\n                marilyn\n            )\\.ca|\n            (?:much|cp24)\\.com\n        )/.*?(?:\\b(?:vid(?:eoid)?|clipId)=|-vid|~|%7E|/(?:episode)?)(?P<id>[0-9]{6,})'
    _module = 'haruhi_dl.extractor.bellmedia'


class BeatportIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.|pro\\.)?beatport\\.com/track/(?P<display_id>[^/]+)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.beatport'


class MTVServicesInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.mtv'


class BetIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bet\\.com/(?:[^/]+/)+(?P<id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.bet'


class BFIPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.bfi\\.org\\.uk/[^/]+/film/watch-(?P<id>[\\w-]+)-online'
    _module = 'haruhi_dl.extractor.bfi'


class BigflixIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bigflix\\.com/.+/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.bigflix'


class BildIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bild\\.de/(?:[^/]+/)+(?P<display_id>[^/]+)-(?P<id>\\d+)(?:,auto=true)?\\.bild\\.html'
    _module = 'haruhi_dl.extractor.bild'


class BiliBiliIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|bangumi)\\.)?\n                        bilibili\\.(?:tv|com)/\n                        (?:\n                            (?:\n                                video/[aA][vV]|\n                                anime/(?P<anime_id>\\d+)/play\\#\n                            )(?P<id_bv>\\d+)|\n                            video/[bB][vV](?P<id>[^/?#&]+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.bilibili'


class BiliBiliBangumiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://bangumi\\.bilibili\\.com/anime/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bilibili'

    @classmethod
    def suitable(cls, url):
        return False if BiliBiliIE.suitable(url) else super(BiliBiliBangumiIE, cls).suitable(url)


class BilibiliAudioBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.bilibili'


class BilibiliAudioIE(BilibiliAudioBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?bilibili\\.com/audio/au(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bilibili'


class BilibiliAudioAlbumIE(BilibiliAudioBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?bilibili\\.com/audio/am(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bilibili'


class BiliBiliPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.bilibili\\.com/player\\.html\\?.*?\\baid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bilibili'


class BioBioChileTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:tv|www)\\.biobiochile\\.cl/(?:notas|noticias)/(?:[^/]+/)+(?P<id>[^/]+)\\.shtml'
    _module = 'haruhi_dl.extractor.biobiochiletv'


class BitChuteIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bitchute\\.com/(?:video|embed|torrent/[^/]+)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.bitchute'


class BitChuteChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bitchute\\.com/channel/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.bitchute'


class BIQLEIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?biqle\\.(?:com|org|ru)/watch/(?P<id>-?\\d+_\\d+)'
    _module = 'haruhi_dl.extractor.biqle'


class BleacherReportIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bleacherreport\\.com/articles/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.bleacherreport'


class BleacherReportCMSIE(AMPIE):
    _VALID_URL = 'https?://(?:www\\.)?bleacherreport\\.com/video_embed\\?id=(?P<id>[0-9a-f-]{36}|\\d{5})'
    _module = 'haruhi_dl.extractor.bleacherreport'


class BlinkxIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://(?:www\\.)blinkx\\.com/#?ce/|blinkx:)(?P<id>[^?]+)'
    _module = 'haruhi_dl.extractor.blinkx'


class BloombergIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bloomberg\\.com/(?:[^/]+/)*(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.bloomberg'


class BokeCCBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.bokecc'


class BokeCCIE(BokeCCBaseIE):
    _VALID_URL = 'https?://union\\.bokecc\\.com/playvideo\\.bo\\?(?P<query>.*)'
    _module = 'haruhi_dl.extractor.bokecc'


class BostonGlobeIE(LazyLoadExtractor):
    _VALID_URL = '(?i)https?://(?:www\\.)?bostonglobe\\.com/.*/(?P<id>[^/]+)/\\w+(?:\\.html)?'
    _module = 'haruhi_dl.extractor.bostonglobe'


class BpbIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bpb\\.de/mediathek/(?P<id>[0-9]+)/'
    _module = 'haruhi_dl.extractor.bpb'


class BRIE(LazyLoadExtractor):
    _VALID_URL = '(?P<base_url>https?://(?:www\\.)?br(?:-klassik)?\\.de)/(?:[a-z0-9\\-_]+/)+(?P<id>[a-z0-9\\-_]+)\\.html'
    _module = 'haruhi_dl.extractor.br'


class BRMediathekIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?br\\.de/mediathek/video/[^/?&#]*?-(?P<id>av:[0-9a-f]{24})'
    _module = 'haruhi_dl.extractor.br'


class BravoTVIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?bravotv\\.com/(?:[^/]+/)+(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.bravotv'


class BreakIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?break\\.com/video/(?P<display_id>[^/]+?)(?:-(?P<id>\\d+))?(?:[/?#&]|$)'
    _module = 'haruhi_dl.extractor.breakcom'


class BrightcoveLegacyIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://.*brightcove\\.com/(services|viewer).*?\\?|brightcove:)(?P<query>.*)'
    _module = 'haruhi_dl.extractor.brightcove'


class BrightcoveNewIE(AdobePassIE):
    _VALID_URL = 'https?://players\\.brightcove\\.net/(?P<account_id>\\d+)/(?P<player_id>[^/]+)_(?P<embed>[^/]+)/index\\.html\\?.*(?P<content_type>video|playlist)Id=(?P<video_id>\\d+|ref:[^&]+)'
    _module = 'haruhi_dl.extractor.brightcove'


class BusinessInsiderIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?businessinsider\\.(?:com|nl)/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.businessinsider'


class BuzzFeedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?buzzfeed\\.com/[^?#]*?/(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.buzzfeed'


class BYUtvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?byutv\\.org/(?:watch|player)/(?!event/)(?P<id>[0-9a-f-]+)(?:/(?P<display_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.byutv'


class C56IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|player)\\.)?56\\.com/(?:.+?/)?(?:v_|(?:play_album.+-))(?P<textid>.+?)\\.(?:html|swf)'
    _module = 'haruhi_dl.extractor.c56'


class CamdemyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?camdemy\\.com/media/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.camdemy'


class CamdemyFolderIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?camdemy\\.com/folder/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.camdemy'


class CamModelsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cammodels\\.com/cam/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.cammodels'


class CamTubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|api)\\.)?camtube\\.co/recordings?/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.camtube'


class CamWithHerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?camwithher\\.tv/view_video\\.php\\?.*\\bviewkey=(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.camwithher'


class CanalplusIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>mycanal|piwiplus)\\.fr/(?:[^/]+/)*(?P<display_id>[^?/]+)(?:\\.html\\?.*\\bvid=|/p/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.canalplus'


class Canalc2IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?canalc2\\.tv/video/|archives-canalc2\\.u-strasbg\\.fr/video\\.asp\\?.*\\bidVideo=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.canalc2'


class CanvasIE(LazyLoadExtractor):
    _VALID_URL = 'https?://mediazone\\.vrt\\.be/api/v1/(?P<site_id>canvas|een|ketnet|vrt(?:video|nieuws)|sporza)/assets/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.canvas'


class CanvasEenIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site_id>canvas|een)\\.be/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.canvas'


class GigyaBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.gigya'


class VrtNUIE(GigyaBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?vrt\\.be/(?P<site_id>vrtnu)/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.canvas'


class CarambaTVIE(LazyLoadExtractor):
    _VALID_URL = '(?:carambatv:|https?://video1\\.carambatv\\.ru/v/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.carambatv'


class CarambaTVPageIE(LazyLoadExtractor):
    _VALID_URL = 'https?://carambatv\\.ru/(?:[^/]+/)+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.carambatv'


class CartoonNetworkIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?cartoonnetwork\\.com/video/(?:[^/]+/)+(?P<id>[^/?#]+)-(?:clip|episode)\\.html'
    _module = 'haruhi_dl.extractor.cartoonnetwork'


class CBCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cbc\\.ca/(?!player/)(?:[^/]+/)+(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.cbc'

    @classmethod
    def suitable(cls, url):
        return False if CBCPlayerIE.suitable(url) else super(CBCIE, cls).suitable(url)


class CBCPlayerIE(LazyLoadExtractor):
    _VALID_URL = '(?:cbcplayer:|https?://(?:www\\.)?cbc\\.ca/(?:player/play/|i/caffeine/syndicate/\\?mediaId=))(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.cbc'


class CBCWatchBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.cbc'


class CBCWatchVideoIE(CBCWatchBaseIE):
    _VALID_URL = 'https?://api-cbc\\.cloud\\.clearleap\\.com/cloffice/client/web/play/?\\?.*?\\bcontentId=(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.cbc'


class CBCWatchIE(CBCWatchBaseIE):
    _VALID_URL = 'https?://(?:gem|watch)\\.cbc\\.ca/(?:[^/]+/)+(?P<id>[0-9a-f-]+)'
    _module = 'haruhi_dl.extractor.cbc'


class CBCOlympicsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://olympics\\.cbc\\.ca/video/[^/]+/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.cbc'


class CBSLocalIE(AnvatoIE):
    _VALID_URL = 'https?://[a-z]+\\.cbslocal\\.com/(?:\\d+/\\d+/\\d+|video)/(?P<id>[0-9a-z-]+)'
    _module = 'haruhi_dl.extractor.cbslocal'


class CBSNewsLiveVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/live/video/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.cbsnews'


class CCCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?media\\.ccc\\.de/v/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.ccc'


class CCCPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?media\\.ccc\\.de/c/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.ccc'


class CCMAIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ccma\\.cat/(?:[^/]+/)*?(?P<type>video|audio)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ccma'


class CCTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:[^/]+)\\.(?:cntv|cctv)\\.(?:com|cn)|(?:www\\.)?ncpa-classic\\.com)/(?:[^/]+/)*?(?P<id>[^/?#&]+?)(?:/index)?(?:\\.s?html|[?#&]|$)'
    _module = 'haruhi_dl.extractor.cctv'


class CDABaseExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.cda'


class CDAIE(CDABaseExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?cda\\.pl/video|ebd\\.cda\\.pl/[0-9]+x[0-9]+)/(?P<id>[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.cda'


class CeskaTelevizeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ceskatelevize\\.cz/ivysilani/(?:[^/?#&]+/)*(?P<id>[^/#?]+)'
    _module = 'haruhi_dl.extractor.ceskatelevize'


class CeskaTelevizePoradyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ceskatelevize\\.cz/porady/(?:[^/?#&]+/)*(?P<id>[^/#?]+)'
    _module = 'haruhi_dl.extractor.ceskatelevize'


class Channel9IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:channel9\\.msdn\\.com|s\\.ch9\\.ms)/(?P<contentpath>.+?)(?P<rss>/RSS)?/?(?:[?#&]|$)'
    _module = 'haruhi_dl.extractor.channel9'


class CharlieRoseIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?charlierose\\.com/(?:video|episode)(?:s|/player)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.charlierose'


class ChaturbateIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?chaturbate\\.com/(?:fullvideo/?\\?.*?\\bb=)?(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.chaturbate'


class ChilloutzoneIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?chilloutzone\\.net/video/(?P<id>[\\w|-]+)\\.html'
    _module = 'haruhi_dl.extractor.chilloutzone'


class ChirbitIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?chirb\\.it/(?:(?:wp|pl)/|fb_chirbit_player\\.swf\\?key=)?(?P<id>[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.chirbit'


class ChirbitProfileIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?chirbit\\.com/(?:rss/)?(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.chirbit'


class CinchcastIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.cinchcast\\.com/.*?(?:assetId|show_id)=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.cinchcast'


class HBOBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.hbo'


class CinemaxIE(HBOBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?cinemax\\.com/(?P<path>[^/]+/video/[0-9a-z-]+-(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.cinemax'


class CiscoLiveBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ciscolive'


class CiscoLiveSessionIE(CiscoLiveBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ciscolive(?:\\.cisco)?\\.com/[^#]*#/session/(?P<id>[^/?&]+)'
    _module = 'haruhi_dl.extractor.ciscolive'


class CiscoLiveSearchIE(CiscoLiveBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ciscolive(?:\\.cisco)?\\.com/(?:global/)?on-demand-library(?:\\.html|/)'
    _module = 'haruhi_dl.extractor.ciscolive'

    @classmethod
    def suitable(cls, url):
        return False if CiscoLiveSessionIE.suitable(url) else super(CiscoLiveSearchIE, cls).suitable(url)


class CJSWIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cjsw\\.com/program/(?P<program>[^/]+)/episode/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.cjsw'


class CliphunterIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?cliphunter\\.com/w/\n        (?P<id>[0-9]+)/\n        (?P<seo>.+?)(?:$|[#\\?])\n    '
    _module = 'haruhi_dl.extractor.cliphunter'


class ClippitIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?clippituser\\.tv/c/(?P<id>[a-z]+)'
    _module = 'haruhi_dl.extractor.clippit'


class ClipRsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?clip\\.rs/(?P<id>[^/]+)/\\d+'
    _module = 'haruhi_dl.extractor.cliprs'


class ClipsyndicateIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:chic|www)\\.clipsyndicate\\.com/video/play(list/\\d+)?/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.clipsyndicate'


class CloserToTruthIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?closertotruth\\.com/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.closertotruth'


class CloudflareStreamIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:watch\\.)?(?:cloudflarestream\\.com|(?:videodelivery|bytehighway)\\.net)/|\n                            embed\\.(?:cloudflarestream\\.com|(?:videodelivery|bytehighway)\\.net)/embed/[^/]+\\.js\\?.*?\\bvideo=\n                        )\n                        (?P<id>[\\da-f]{32}|[\\w-]+\\.[\\w-]+\\.[\\w-]+)\n                    '
    _module = 'haruhi_dl.extractor.cloudflarestream'


class CloudyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cloudy\\.ec/(?:v/|embed\\.php\\?.*?\\bid=)(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.cloudy'


class ClubicIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?clubic\\.com/video/(?:[^/]+/)*video.*-(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.clubic'


class ClypIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?clyp\\.it/(?P<id>[a-z0-9]+)'
    _module = 'haruhi_dl.extractor.clyp'


class CNBCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.cnbc\\.com/gallery/\\?video=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.cnbc'


class CNBCVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cnbc\\.com/video/(?:[^/]+/)+(?P<id>[^./?#&]+)'
    _module = 'haruhi_dl.extractor.cnbc'


class CNNIE(TurnerBaseIE):
    _VALID_URL = '(?x)https?://(?:(?P<sub_domain>edition|www|money)\\.)?cnn\\.com/(?:video/(?:data/.+?|\\?)/)?videos?/\n        (?P<path>.+?/(?P<title>[^/]+?)(?:\\.(?:[a-z\\-]+)|(?=&)))'
    _module = 'haruhi_dl.extractor.cnn'


class CNNBlogsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[^\\.]+\\.blogs\\.cnn\\.com/.+'
    _module = 'haruhi_dl.extractor.cnn'


class CNNArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:edition|www)\\.)?cnn\\.com/(?!videos?/)'
    _module = 'haruhi_dl.extractor.cnn'


class CoubIE(LazyLoadExtractor):
    _VALID_URL = '(?:coub:|https?://(?:coub\\.com/(?:view|embed|coubs)/|c-cdn\\.coub\\.com/fb-player\\.swf\\?.*\\bcoub(?:ID|id)=))(?P<id>[\\da-z]+)'
    _module = 'haruhi_dl.extractor.coub'


class ComedyCentralFullEpisodesIE(MTVServicesInfoExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?cc\\.com/\n        (?:full-episodes|shows(?=/[^/]+/full-episodes))\n        /(?P<id>[^?]+)'
    _module = 'haruhi_dl.extractor.comedycentral'


class ComedyCentralIE(MTVServicesInfoExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?cc\\.com/\n        (video-clips|episodes|cc-studios|video-collections|shows(?=/[^/]+/(?!full-episodes)))\n        /(?P<title>.*)'
    _module = 'haruhi_dl.extractor.comedycentral'


class ComedyCentralShortnameIE(LazyLoadExtractor):
    _VALID_URL = '^:(?P<id>tds|thedailyshow|theopposition)$'
    _module = 'haruhi_dl.extractor.comedycentral'


class ComedyCentralTVIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?comedycentral\\.tv/(?:staffeln|shows)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.comedycentral'


class ToshIE(MTVServicesInfoExtractor):
    _VALID_URL = '^https?://tosh\\.cc\\.com/video-(?:clips|collections)/[^/]+/(?P<videotitle>[^/?#]+)'
    _module = 'haruhi_dl.extractor.comedycentral'


class CommonMistakesIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        (?:url|URL)$\n    '
    _module = 'haruhi_dl.extractor.commonmistakes'


class UnicodeBOMIE(LazyLoadExtractor):
    _VALID_URL = '(?P<bom>\\ufeff)(?P<id>.*)$'
    _module = 'haruhi_dl.extractor.commonmistakes'


class MmsIE(LazyLoadExtractor):
    _VALID_URL = '(?i)mms://.+'
    _module = 'haruhi_dl.extractor.commonprotocols'


class RtmpIE(LazyLoadExtractor):
    _VALID_URL = '(?i)rtmp[est]?://.+'
    _module = 'haruhi_dl.extractor.commonprotocols'


class CondeNastIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:video|www|player(?:-backend)?)\\.(?:allure|architecturaldigest|arstechnica|bonappetit|brides|cnevids|cntraveler|details|epicurious|glamour|golfdigest|gq|newyorker|self|teenvogue|vanityfair|vogue|wired|wmagazine)\\.com/\n        (?:\n            (?:\n                embed(?:js)?|\n                (?:script|inline)/video\n            )/(?P<id>[0-9a-f]{24})(?:/(?P<player_id>[0-9a-f]{24}))?(?:.+?\\btarget=(?P<target>[^&]+))?|\n            (?P<type>watch|series|video)/(?P<display_id>[^/?#]+)\n        )'
    _module = 'haruhi_dl.extractor.condenast'


class CONtvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?contv\\.com/details-movie/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.contv'


class CrackedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cracked\\.com/video_(?P<id>\\d+)_[\\da-z-]+\\.html'
    _module = 'haruhi_dl.extractor.cracked'


class CrackleIE(LazyLoadExtractor):
    _VALID_URL = '(?:crackle:|https?://(?:(?:www|m)\\.)?(?:sony)?crackle\\.com/(?:playlist/\\d+/|(?:[^/]+/)+))(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.crackle'


class CrooksAndLiarsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://embed\\.crooksandliars\\.com/(?:embed|v)/(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.crooksandliars'


class CrunchyrollBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.crunchyroll'


class CrunchyrollShowPlaylistIE(CrunchyrollBaseIE):
    _VALID_URL = 'https?://(?:(?P<prefix>www|m)\\.)?(?P<url>crunchyroll\\.com/(?!(?:news|anime-news|library|forum|launchcalendar|lineup|store|comics|freetrial|login|media-\\d+))(?P<id>[\\w\\-]+))/?(?:\\?|$)'
    _module = 'haruhi_dl.extractor.crunchyroll'


class CSpanIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?c-span\\.org/video/\\?(?P<id>[0-9a-f]+)'
    _module = 'haruhi_dl.extractor.cspan'


class CtsNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://news\\.cts\\.com\\.tw/[a-z]+/[a-z]+/\\d+/(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.ctsnews'


class CTVNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?ctvnews\\.ca/(?:video\\?(?:clip|playlist|bin)Id=|.*?)(?P<id>[0-9.]+)'
    _module = 'haruhi_dl.extractor.ctvnews'


class CultureUnpluggedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cultureunplugged\\.com/documentary/watch-online/play/(?P<id>\\d+)(?:/(?P<display_id>[^/]+))?'
    _module = 'haruhi_dl.extractor.cultureunplugged'


class CuriosityStreamBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.curiositystream'


class CuriosityStreamIE(CuriosityStreamBaseIE):
    _VALID_URL = 'https?://(?:app\\.)?curiositystream\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.curiositystream'


class CuriosityStreamCollectionIE(CuriosityStreamBaseIE):
    _VALID_URL = 'https?://(?:app\\.)?curiositystream\\.com/(?:collection|series)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.curiositystream'


class CWTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cw(?:tv(?:pr)?|seed)\\.com/(?:shows/)?(?:[^/]+/)+[^?]*\\?.*\\b(?:play|watch)=(?P<id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})'
    _module = 'haruhi_dl.extractor.cwtv'


class DailyMailIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dailymail\\.co\\.uk/(?:video/[^/]+/video-|embed/video/)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.dailymail'


class DailymotionBaseInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.dailymotion'


class DailymotionIE(DailymotionBaseInfoExtractor):
    _VALID_URL = '(?ix)\n                    https?://\n                        (?:\n                            (?:(?:www|touch)\\.)?dailymotion\\.[a-z]{2,3}/(?:(?:(?:embed|swf|\\#)/)?video|swf)|\n                            (?:www\\.)?lequipe\\.fr/video\n                        )\n                        /(?P<id>[^/?_]+)(?:.+?\\bplaylist=(?P<playlist_id>x[0-9a-z]+))?\n                    '
    _module = 'haruhi_dl.extractor.dailymotion'


class DailymotionPlaylistBaseIE(DailymotionBaseInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.dailymotion'


class DailymotionPlaylistIE(DailymotionPlaylistBaseIE):
    _VALID_URL = '(?:https?://)?(?:www\\.)?dailymotion\\.[a-z]{2,3}/playlist/(?P<id>x[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.dailymotion'


class DailymotionUserIE(DailymotionPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?dailymotion\\.[a-z]{2,3}/(?!(?:embed|swf|#|video|playlist)/)(?:(?:old/)?user/)?(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.dailymotion'


class DaumBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.daum'


class DaumIE(DaumBaseIE):
    _VALID_URL = 'https?://(?:(?:m\\.)?tvpot\\.daum\\.net/v/|videofarm\\.daum\\.net/controller/player/VodPlayer\\.swf\\?vid=)(?P<id>[^?#&]+)'
    _module = 'haruhi_dl.extractor.daum'


class DaumClipIE(DaumBaseIE):
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/(?:clip/ClipView.(?:do|tv)|mypot/View.do)\\?.*?clipid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.daum'

    @classmethod
    def suitable(cls, url):
        return False if DaumPlaylistIE.suitable(url) or DaumUserIE.suitable(url) else super(DaumClipIE, cls).suitable(url)


class DaumListIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.daum'


class DaumPlaylistIE(DaumListIE):
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/mypot/(?:View\\.do|Top\\.tv)\\?.*?playlistid=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.daum'

    @classmethod
    def suitable(cls, url):
        return False if DaumUserIE.suitable(url) else super(DaumPlaylistIE, cls).suitable(url)


class DaumUserIE(DaumListIE):
    _VALID_URL = 'https?://(?:m\\.)?tvpot\\.daum\\.net/mypot/(?:View|Top)\\.(?:do|tv)\\?.*?ownerid=(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.daum'


class DBTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dagbladet\\.no/video/(?:(?:embed|(?P<display_id>[^/]+))/)?(?P<id>[0-9A-Za-z_-]{11}|[a-zA-Z0-9]{8})'
    _module = 'haruhi_dl.extractor.dbtv'


class DctpTvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dctp\\.tv/(?:#/)?filme/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.dctp'


class DeezerPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?deezer\\.com/playlist/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.deezer'


class DemocracynowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?democracynow\\.org/(?P<id>[^\\?]*)'
    _module = 'haruhi_dl.extractor.democracynow'


class DFBIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tv\\.dfb\\.de/video/(?P<display_id>[^/]+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.dfb'


class DHMIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dhm\\.de/filmarchiv/(?:[^/]+/)+(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.dhm'


class DiggIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?digg\\.com/video/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.digg'


class DotsubIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dotsub\\.com/view/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.dotsub'


class DouyuShowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://v(?:mobile)?\\.douyu\\.com/show/(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.douyutv'


class DouyuTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?douyu(?:tv)?\\.com/(?:[^/]+/)*(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.douyutv'


class DPlayIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://\n        (?P<domain>\n            (?:www\\.)?(?P<host>dplay\\.(?P<country>dk|fi|jp|se|no))|\n            (?P<subdomain_country>es|it)\\.dplay\\.com\n        )/[^/]+/(?P<id>[^/]+/[^/?#]+)'
    _module = 'haruhi_dl.extractor.dplay'


class DreiSatIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?3sat\\.de/mediathek/(?:(?:index|mediathek)\\.php)?\\?(?:(?:mode|display)=[^&]+&)*obj=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.dreisat'


class DRBonanzaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dr\\.dk/bonanza/[^/]+/\\d+/[^/]+/(?P<id>\\d+)/(?P<display_id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.drbonanza'


class DrTuberIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?drtuber\\.com/(?:video|embed)/(?P<id>\\d+)(?:/(?P<display_id>[\\w-]+))?'
    _module = 'haruhi_dl.extractor.drtuber'


class DRTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?dr\\.dk/(?:tv/se|nyheder|radio(?:/ondemand)?)/(?:[^/]+/)*|\n                            (?:www\\.)?(?:dr\\.dk|dr-massive\\.com)/drtv/(?:se|episode)/\n                        )\n                        (?P<id>[\\da-z_-]+)\n                    '
    _module = 'haruhi_dl.extractor.drtv'


class DRTVLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dr\\.dk/(?:tv|TV)/live/(?P<id>[\\da-z-]+)'
    _module = 'haruhi_dl.extractor.drtv'


class DTubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?d\\.tube/(?:#!/)?v/(?P<uploader_id>[0-9a-z.-]+)/(?P<id>[0-9a-z]{8})'
    _module = 'haruhi_dl.extractor.dtube'


class DVTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.aktualne\\.cz/(?:[^/]+/)+r~(?P<id>[0-9a-f]{32})'
    _module = 'haruhi_dl.extractor.dvtv'


class DumpertIE(LazyLoadExtractor):
    _VALID_URL = '(?P<protocol>https?)://(?:(?:www|legacy)\\.)?dumpert\\.nl/(?:mediabase|embed|item)/(?P<id>[0-9]+[/_][0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.dumpert'


class DefenseGouvFrIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.*?\\.defense\\.gouv\\.fr/layout/set/ligthboxvideo/base-de-medias/webtv/(?P<id>[^/?#]*)'
    _module = 'haruhi_dl.extractor.defense'


class DiscoveryGoBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.discoverygo'


class DiscoveryIE(DiscoveryGoBaseIE):
    _VALID_URL = '(?x)https?://\n        (?P<site>\n            go\\.discovery|\n            www\\.\n                (?:\n                    investigationdiscovery|\n                    discoverylife|\n                    animalplanet|\n                    ahctv|\n                    destinationamerica|\n                    sciencechannel|\n                    tlc\n                )|\n            watch\\.\n                (?:\n                    hgtv|\n                    foodnetwork|\n                    travelchannel|\n                    diynetwork|\n                    cookingchanneltv|\n                    motortrend\n                )\n        )\\.com/tv-shows/(?P<show_slug>[^/]+)/(?:video|full-episode)s/(?P<id>[^./?#]+)'
    _module = 'haruhi_dl.extractor.discovery'


class DiscoveryGoIE(DiscoveryGoBaseIE):
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:\n            discovery|\n            investigationdiscovery|\n            discoverylife|\n            animalplanet|\n            ahctv|\n            destinationamerica|\n            sciencechannel|\n            tlc|\n            velocitychannel\n        )go\\.com/(?:[^/]+/)+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.discoverygo'


class DiscoveryGoPlaylistIE(DiscoveryGoBaseIE):
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:\n            discovery|\n            investigationdiscovery|\n            discoverylife|\n            animalplanet|\n            ahctv|\n            destinationamerica|\n            sciencechannel|\n            tlc|\n            velocitychannel\n        )go\\.com/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.discoverygo'

    @classmethod
    def suitable(cls, url):
        return False if DiscoveryGoIE.suitable(url) else super(
            DiscoveryGoPlaylistIE, cls).suitable(url)


class DiscoveryNetworksDeIE(DPlayIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:tlc|dmax)\\.de|dplay\\.co\\.uk)/(?:programme|show)/(?P<programme>[^/]+)/video/(?P<alternate_id>[^/]+)'
    _module = 'haruhi_dl.extractor.discoverynetworks'


class DiscoveryVRIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?discoveryvr\\.com/watch/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.discoveryvr'


class DisneyIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?P<domain>(?:[^/]+\\.)?(?:disney\\.[a-z]{2,3}(?:\\.[a-z]{2})?|disney(?:(?:me|latino)\\.com|turkiye\\.com\\.tr|channel\\.de)|(?:starwars|marvelkids)\\.com))/(?:(?:embed/|(?:[^/]+/)+[\\w-]+-)(?P<id>[a-z0-9]{24})|(?:[^/]+/)?(?P<display_id>[^/?#]+))'
    _module = 'haruhi_dl.extractor.disney'


class DigitallySpeakingIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:s?evt\\.dispeak|events\\.digitallyspeaking)\\.com/(?:[^/]+/)+xml/(?P<id>[^.]+)\\.xml'
    _module = 'haruhi_dl.extractor.dispeak'


class DropboxIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dropbox[.]com/sh?/(?P<id>[a-zA-Z0-9]{15})/.*'
    _module = 'haruhi_dl.extractor.dropbox'


class DWIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dw\\.com/(?:[^/]+/)+(?:av|e)-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.dw'


class DWArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dw\\.com/(?:[^/]+/)+a-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.dw'


class EaglePlatformIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?:\n                        eagleplatform:(?P<custom_host>[^/]+):|\n                        https?://(?P<host>.+?\\.media\\.eagleplatform\\.com)/index/player\\?.*\\brecord_id=\n                    )\n                    (?P<id>\\d+)\n                '
    _module = 'haruhi_dl.extractor.eagleplatform'


class EbaumsWorldIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ebaumsworld\\.com/videos/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ebaumsworld'


class EchoMskIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?echo\\.msk\\.ru/sounds/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.echomsk'


class EggheadCourseIE(LazyLoadExtractor):
    _VALID_URL = 'https://egghead\\.io/courses/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.egghead'


class EggheadLessonIE(LazyLoadExtractor):
    _VALID_URL = 'https://egghead\\.io/(?:api/v1/)?lessons/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.egghead'


class EHowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ehow\\.com/[^/_?]*_(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.ehow'


class EightTracksIE(LazyLoadExtractor):
    _VALID_URL = 'https?://8tracks\\.com/(?P<user>[^/]+)/(?P<id>[^/#]+)(?:#.*)?$'
    _module = 'haruhi_dl.extractor.eighttracks'


class EinthusanIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<host>einthusan\\.(?:tv|com|ca))/movie/watch/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.einthusan'


class EitbIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?eitb\\.tv/(?:eu/bideoa|es/video)/[^/]+/\\d+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.eitb'


class EllenTubeBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ellentube'


class EllenTubeIE(EllenTubeBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            ellentube:|\n                            https://api-prod\\.ellentube\\.com/ellenapi/api/item/\n                        )\n                        (?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})\n                    '
    _module = 'haruhi_dl.extractor.ellentube'


class EllenTubeVideoIE(EllenTubeBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ellentube\\.com/video/(?P<id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.ellentube'


class EllenTubePlaylistIE(EllenTubeBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ellentube\\.com/(?:episode|studios)/(?P<id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.ellentube'


class ElPaisIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^.]+\\.)?elpais\\.com/.*/(?P<id>[^/#?]+)\\.html(?:$|[?#])'
    _module = 'haruhi_dl.extractor.elpais'


class EmbedlyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www|cdn\\.)?embedly\\.com/widgets/media\\.html\\?(?:[^#]*?&)?url=(?P<id>[^#&]+)'
    _module = 'haruhi_dl.extractor.embedly'


class EngadgetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?engadget\\.com/video/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.engadget'


class EpornerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?eporner\\.com/(?:hd-porn|embed)/(?P<id>\\w+)(?:/(?P<display_id>[\\w-]+))?'
    _module = 'haruhi_dl.extractor.eporner'


class EroProfileIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?eroprofile\\.com/m/videos/view/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.eroprofile'


class EscapistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://?(?:(?:www|v1)\\.)?escapistmagazine\\.com/videos/view/[^/]+/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.escapist'


class EskaGoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?eskago\\.pl/radio/(?P<id>[^/\\s?#]+)'
    _module = 'haruhi_dl.extractor.eskago'


class OnceIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.+?\\.unicornmedia\\.com/now/(?:ads/vmap/)?[^/]+/[^/]+/(?P<domain_id>[^/]+)/(?P<application_id>[^/]+)/(?:[^/]+/)?(?P<media_item_id>[^/]+)/content\\.(?:once|m3u8|mp4)'
    _module = 'haruhi_dl.extractor.once'


class ESPNIE(OnceIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                (?:\n                                    (?:(?:\\w+\\.)+)?espn\\.go|\n                                    (?:www\\.)?espn\n                                )\\.com/\n                                (?:\n                                    (?:\n                                        video/(?:clip|iframe/twitter)|\n                                        watch/player\n                                    )\n                                    (?:\n                                        .*?\\?.*?\\bid=|\n                                        /_/id/\n                                    )|\n                                    [^/]+/video/\n                                )\n                            )|\n                            (?:www\\.)espnfc\\.(?:com|us)/(?:video/)?[^/]+/\\d+/video/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.espn'


class ESPNArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:espn\\.go|(?:www\\.)?espn)\\.com/(?:[^/]+/)*(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.espn'

    @classmethod
    def suitable(cls, url):
        return False if ESPNIE.suitable(url) else super(ESPNArticleIE, cls).suitable(url)


class FiveThirtyEightIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?fivethirtyeight\\.com/features/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.espn'


class EsriVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.esri\\.com/watch/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.esri'


class EuropaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://ec\\.europa\\.eu/avservices/(?:video/player|audio/audioDetails)\\.cfm\\?.*?\\bref=(?P<id>[A-Za-z0-9-]+)'
    _module = 'haruhi_dl.extractor.europa'


class EurozetArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[a-z]+\\.)*(?<!player\\.)(?:radiozet|chillizet|antyradio|planeta|meloradio)\\.pl/[^/\\s]+/(?P<id>[^/\\s]+)'
    _module = 'haruhi_dl.extractor.eurozet'


class EurozetPlayerStreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.(?P<id>radiozet|chillizet|antyradio|meloradio)\\.pl/?(?:\\?[^#]*)?(?:#.*)?$'
    _module = 'haruhi_dl.extractor.eurozet'


class EurozetPlayerPodcastIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.(?P<station>radiozet|chillizet|antyradio|meloradio)\\.pl/Podcasty/(?P<series>[^/\\s#\\?]+/)?(?P<id>[^/\\s#\\?]+)'
    _module = 'haruhi_dl.extractor.eurozet'


class EurozetPlayerMusicStreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.(?P<station>radiozet|chillizet|antyradio|meloradio)\\.pl/Kanaly-muzyczne/(?P<id>[^/\\s#\\?]+)'
    _module = 'haruhi_dl.extractor.eurozet'


class EveryonesMixtapeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?everyonesmixtape\\.com/#/mix/(?P<id>[0-9a-zA-Z]+)(?:/(?P<songnr>[0-9]))?$'
    _module = 'haruhi_dl.extractor.everyonesmixtape'


class ExpoTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?expotv\\.com/videos/[^?#]*/(?P<id>[0-9]+)($|[?#])'
    _module = 'haruhi_dl.extractor.expotv'


class ExpressenIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?:expressen|di)\\.se/\n                        (?:(?:tvspelare/video|videoplayer/embed)/)?\n                        tv/(?:[^/]+/)*\n                        (?P<id>[^/?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.expressen'


class EyedoTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?eyedo\\.tv/[^/]+/(?:#!/)?Live/Detail/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.eyedotv'


class FacebookIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                (?:\n                    https?://\n                        (?:[\\w-]+\\.)?(?:facebook\\.com|facebookcorewwwi\\.onion)/\n                        (?:[^#]*?\\#!/)?\n                        (?:\n                            (?:\n                                video/video\\.php|\n                                photo\\.php|\n                                video\\.php|\n                                video/embed|\n                                story\\.php\n                            )\\?(?:.*?)(?:v|video_id|story_fbid)=|\n                            [^/]+/videos/(?:[^/]+/)?|\n                            [^/]+/posts/|\n                            groups/[^/]+/permalink/\n                        )|\n                    facebook:\n                )\n                (?P<id>[0-9]+)\n                '
    _module = 'haruhi_dl.extractor.facebook'


class FacebookPluginsVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[\\w-]+\\.)?facebook\\.com/plugins/video\\.php\\?.*?\\bhref=(?P<id>https.+)'
    _module = 'haruhi_dl.extractor.facebook'


class FazIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?faz\\.net/(?:[^/]+/)*.*?-(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.faz'


class FC2IE(LazyLoadExtractor):
    _VALID_URL = '^(?:https?://video\\.fc2\\.com/(?:[^/]+/)*content/|fc2:)(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.fc2'


class FC2EmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.fc2\\.com/flv2\\.swf\\?(?P<query>.+)'
    _module = 'haruhi_dl.extractor.fc2'


class FczenitIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?fc-zenit\\.ru/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.fczenit'


class FilmOnIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://(?:www\\.)?filmon\\.com/vod/view/|filmon:)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.filmon'


class FilmOnChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?filmon\\.com/(?:tv|channel)/(?P<id>[a-z0-9-]+)'
    _module = 'haruhi_dl.extractor.filmon'


class FilmwebIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?filmweb\\.no/(?P<type>trailere|filmnytt)/article(?P<id>\\d+)\\.ece'
    _module = 'haruhi_dl.extractor.filmweb'


class FirstTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?1tv\\.ru/(?:[^/]+/)+(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.firsttv'


class FiveMinIE(LazyLoadExtractor):
    _VALID_URL = '(?:5min:|https?://(?:[^/]*?5min\\.com/|delivery\\.vidible\\.tv/aol)(?:(?:Scripts/PlayerSeed\\.js|playerseed/?)?\\?.*?playList=)?)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fivemin'


class FiveTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?5-tv\\.ru/\n                        (?:\n                            (?:[^/]+/)+(?P<id>\\d+)|\n                            (?P<path>[^/?#]+)(?:[/?#])?\n                        )\n                    '
    _module = 'haruhi_dl.extractor.fivetv'


class FlickrIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.|secure\\.)?flickr\\.com/photos/[\\w\\-_@]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.flickr'


class FolketingetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ft\\.dk/webtv/video/[^?#]*?\\.(?P<id>[0-9]+)\\.aspx'
    _module = 'haruhi_dl.extractor.folketinget'


class FootyRoomIE(LazyLoadExtractor):
    _VALID_URL = 'https?://footyroom\\.com/matches/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.footyroom'


class Formula1IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?formula1\\.com/(?:content/fom-website/)?en/video/\\d{4}/\\d{1,2}/(?P<id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.formula1'


class FourTubeBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.fourtube'


class FourTubeIE(FourTubeBaseIE):
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?4tube\\.com/(?:videos|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.fourtube'


class PornTubeIE(FourTubeBaseIE):
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?porntube\\.com/(?:videos/(?P<display_id>[^/]+)_|embed/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fourtube'


class PornerBrosIE(FourTubeBaseIE):
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?pornerbros\\.com/(?:videos/(?P<display_id>[^/]+)_|embed/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fourtube'


class FuxIE(FourTubeBaseIE):
    _VALID_URL = 'https?://(?:(?P<kind>www|m)\\.)?fux\\.com/(?:video|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.fourtube'


class FOXIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?fox\\.com/watch/(?P<id>[\\da-fA-F]+)'
    _module = 'haruhi_dl.extractor.fox'


class FOX9IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?fox9\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fox9'


class FOX9NewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?fox9\\.com/news/(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.fox9'


class FoxgayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?foxgay\\.com/videos/(?:\\S+-)?(?P<id>\\d+)\\.shtml'
    _module = 'haruhi_dl.extractor.foxgay'


class FoxNewsIE(AMPIE):
    _VALID_URL = 'https?://(?P<host>video\\.(?:insider\\.)?fox(?:news|business)\\.com)/v/(?:video-embed\\.html\\?video_id=)?(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.foxnews'


class FoxNewsArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:insider\\.)?foxnews\\.com/(?!v)([^/]+/)+(?P<id>[a-z-]+)'
    _module = 'haruhi_dl.extractor.foxnews'


class FoxSportsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?foxsports\\.com/(?:[^/]+/)*video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.foxsports'


class FranceCultureIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?franceculture\\.fr/emissions/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.franceculture'


class FranceInterIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?franceinter\\.fr/emissions/(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.franceinter'


class FranceTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?:\n                        https?://\n                            sivideo\\.webservices\\.francetelevisions\\.fr/tools/getInfosOeuvre/v2/\\?\n                            .*?\\bidDiffusion=[^&]+|\n                        (?:\n                            https?://videos\\.francetv\\.fr/video/|\n                            francetv:\n                        )\n                        (?P<id>[^@]+)(?:@(?P<catalog>.+))?\n                    )\n                    '
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVBaseInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVSiteIE(FranceTVBaseInfoExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?france\\.tv|mobile\\.france\\.tv)/(?:[^/]+/)*(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVEmbedIE(FranceTVBaseInfoExtractor):
    _VALID_URL = 'https?://embed\\.francetv\\.fr/*\\?.*?\\bue=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVInfoIE(FranceTVBaseInfoExtractor):
    _VALID_URL = 'https?://(?:www|mobile|france3-regions)\\.francetvinfo\\.fr/(?:[^/]+/)*(?P<id>[^/?#&.]+)'
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVInfoSportIE(FranceTVBaseInfoExtractor):
    _VALID_URL = 'https?://sport\\.francetvinfo\\.fr/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.francetv'


class FranceTVJeunesseIE(FranceTVBaseInfoExtractor):
    _VALID_URL = '(?P<url>https?://(?:www\\.)?(?:zouzous|ludo)\\.fr/heros/(?P<id>[^/?#&]+))'
    _module = 'haruhi_dl.extractor.francetv'


class GenerationWhatIE(LazyLoadExtractor):
    _VALID_URL = 'https?://generation-what\\.francetv\\.fr/[^/]+/video/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.francetv'


class CultureboxIE(FranceTVBaseInfoExtractor):
    _VALID_URL = 'https?://(?:m\\.)?culturebox\\.francetvinfo\\.fr/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.francetv'


class FreesoundIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?freesound\\.org/people/[^/]+/sounds/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.freesound'


class FreespeechIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?freespeech\\.org/stories/(?P<id>.+)'
    _module = 'haruhi_dl.extractor.freespeech'


class FreshLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://freshlive\\.tv/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.freshlive'


class FrontendMastersBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.frontendmasters'


class FrontendMastersIE(FrontendMastersBaseIE):
    _VALID_URL = '(?:frontendmasters:|https?://api\\.frontendmasters\\.com/v\\d+/kabuki/video/)(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.frontendmasters'


class FrontendMastersPageBaseIE(FrontendMastersBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.frontendmasters'


class FrontendMastersLessonIE(FrontendMastersPageBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?frontendmasters\\.com/courses/(?P<course_name>[^/]+)/(?P<lesson_name>[^/]+)'
    _module = 'haruhi_dl.extractor.frontendmasters'


class FrontendMastersCourseIE(FrontendMastersPageBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?frontendmasters\\.com/courses/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.frontendmasters'

    @classmethod
    def suitable(cls, url):
        return False if FrontendMastersLessonIE.suitable(url) else super(
            FrontendMastersBaseIE, cls).suitable(url)


class FunimationIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?funimation(?:\\.com|now\\.uk)/shows/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.funimation'


class FunkIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?funk\\.net/(?:channel|playlist)/[^/]+/(?P<display_id>[0-9a-z-]+)-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.funk'


class SelfhostedInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.common'

    _SH_VALID_URL = None
    _SH_VALID_CONTENT_STRINGS = None
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleBaseExtractor(LazyLoadSelfhostedExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = None
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleAlbumSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:album:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/library/albums/(?P<id>\\d+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleArtistSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:artist:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/library/artists/(?P<id>[\\w-]+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleChannelSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:channel:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/channels/(?P<id>[\\w-]+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhalePlaylistSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:playlist:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/library/playlists/(?P<id>\\d+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleTrackSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:track:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/library/tracks/(?P<id>\\d+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FunkwhaleRadioSHIE(FunkwhaleBaseExtractor):
    _VALID_URL = 'funkwhale:radio:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.funkwhale'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/library/radios/(?P<id>\\d+)'
    _SH_VALID_CONTENT_STRINGS = ("<noscript><strong>We're sorry but Funkwhale doesn't work", '<meta name=generator content=Funkwhale>')
    _SH_VALID_CONTENT_REGEXES = None


class FusionIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?fusion\\.(?:net|tv)/(?:video/|show/.+?\\bvideo=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fusion'


class FXNetworksIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:fxnetworks|simpsonsworld)\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.fxnetworks'


class GaiaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?gaia\\.com/video/(?P<id>[^/?]+).*?\\bfullplayer=(?P<type>feature|preview)'
    _module = 'haruhi_dl.extractor.gaia'


class GameInformerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?gameinformer\\.com/(?:[^/]+/)*(?P<id>[^.?&#]+)'
    _module = 'haruhi_dl.extractor.gameinformer'


class GameSpotIE(OnceIE):
    _VALID_URL = 'https?://(?:www\\.)?gamespot\\.com/(?:video|article|review)s/(?:[^/]+/\\d+-|embed/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.gamespot'


class GameStarIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?game(?P<site>pro|star)\\.de/videos/.*,(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.gamestar'


class GaskrankIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?gaskrank\\.tv/tv/(?P<categories>[^/]+)/(?P<id>[^/]+)\\.htm'
    _module = 'haruhi_dl.extractor.gaskrank'


class GazetaIE(LazyLoadExtractor):
    _VALID_URL = '(?P<url>https?://(?:www\\.)?gazeta\\.ru/(?:[^/]+/)?video/(?:main/)*(?:\\d{4}/\\d{2}/\\d{2}/)?(?P<id>[A-Za-z0-9-_.]+)\\.s?html)'
    _module = 'haruhi_dl.extractor.gazeta'


class GDCVaultIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?gdcvault\\.com/play/(?P<id>\\d+)(?:/(?P<name>[\\w-]+))?'
    _module = 'haruhi_dl.extractor.gdcvault'


class GfycatIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|giant|thumbs)\\.)?gfycat\\.com/(?:ru/|ifr/|gifs/detail/)?(?P<id>[^-/?#\\.]+)'
    _module = 'haruhi_dl.extractor.gfycat'


class GiantBombIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?giantbomb\\.com/(?:videos|shows)/(?P<display_id>[^/]+)/(?P<id>\\d+-\\d+)'
    _module = 'haruhi_dl.extractor.giantbomb'


class GigaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?giga\\.de/(?:[^/]+/)*(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.giga'


class GlideIE(LazyLoadExtractor):
    _VALID_URL = 'https?://share\\.glide\\.me/(?P<id>[A-Za-z0-9\\-=_+]+)'
    _module = 'haruhi_dl.extractor.glide'


class GloboIE(LazyLoadExtractor):
    _VALID_URL = '(?:globo:|https?://.+?\\.globo\\.com/(?:[^/]+/)*(?:v/(?:[^/]+/)?|videos/))(?P<id>\\d{7,})'
    _module = 'haruhi_dl.extractor.globo'


class GloboArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.+?\\.globo\\.com/(?:[^/]+/)*(?P<id>[^/.]+)(?:\\.html)?'
    _module = 'haruhi_dl.extractor.globo'

    @classmethod
    def suitable(cls, url):
        return False if GloboIE.suitable(url) else super(GloboArticleIE, cls).suitable(url)


class GoIE(AdobePassIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?P<sub_domain>abc|freeform|watchdisneychannel|watchdisneyjunior|watchdisneyxd|disneynow)\\.)?go|\n                            (?P<sub_domain_2>abc|freeform|disneynow)\n                        )\\.com/\n                        (?:\n                            (?:[^/]+/)*(?P<id>[Vv][Dd][Kk][Aa]\\w+)|\n                            (?:[^/]+/)*(?P<display_id>[^/?\\#]+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.go'


class GodTubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?godtube\\.com/watch/\\?v=(?P<id>[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.godtube'


class GolemIE(LazyLoadExtractor):
    _VALID_URL = '^https?://video\\.golem\\.de/.+?/(?P<id>.+?)/'
    _module = 'haruhi_dl.extractor.golem'


class GoogleDriveIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                (?:docs|drive)\\.google\\.com/\n                                (?:\n                                    (?:uc|open)\\?.*?id=|\n                                    file/d/\n                                )|\n                                video\\.google\\.com/get_player\\?.*?docid=\n                            )\n                            (?P<id>[a-zA-Z0-9_-]{28,})\n                    '
    _module = 'haruhi_dl.extractor.googledrive'


class GooglePlusIE(LazyLoadExtractor):
    _VALID_URL = 'https?://plus\\.google\\.com/(?:[^/]+/)*?posts/(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.googleplus'


class GoogleSearchIE(LazyLoadSearchExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.googlesearch'

    @classmethod
    def suitable(cls, url):
        return re.match(cls._make_valid_url(), url) is not None

    @classmethod
    def _make_valid_url(cls):
        return 'gvsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class GoshgayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?goshgay\\.com/video(?P<id>\\d+?)($|/)'
    _module = 'haruhi_dl.extractor.goshgay'


class GPUTechConfIE(LazyLoadExtractor):
    _VALID_URL = 'https?://on-demand\\.gputechconf\\.com/gtc/2015/video/S(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.gputechconf'


class GrouponIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?groupon\\.com/deals/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.groupon'


class GtvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?gtv\\.org/video/id=(?P<id>[a-f\\d]+)'
    _module = 'haruhi_dl.extractor.gtv'


class GuardianAudioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?theguardian\\.com/[^/]+/audio/\\d{4}/[a-z]{3}/\\d{2}/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.guardian'


class GuardianVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?theguardian\\.com/[^/]+/video/\\d{4}/[a-z]{3}/\\d{2}/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.guardian'


class HBOIE(HBOBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?hbo\\.com/(?:video|embed)(?:/[^/]+)*/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.hbo'


class HearThisAtIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hearthis\\.at/(?P<artist>[^/]+)/(?P<title>[A-Za-z0-9\\-]+)/?$'
    _module = 'haruhi_dl.extractor.hearthisat'


class HeiseIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?heise\\.de/(?:[^/]+/)*[^/]+-(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.heise'


class HellPornoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hellporno\\.(?:com/videos|net/v)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.hellporno'


class HelsinkiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.helsinki\\.fi/Arkisto/flash\\.php\\?id=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.helsinki'


class HentaiStigmaIE(LazyLoadExtractor):
    _VALID_URL = '^https?://hentai\\.animestigma\\.com/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.hentaistigma'


class HGTVComShowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hgtv\\.com/shows/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.hgtv'


class HKETVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hkedcity\\.net/etv/resource/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.hketv'


class HiDiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hidive\\.com/stream/(?P<title>[^/]+)/(?P<key>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.hidive'


class HistoricFilmsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?historicfilms\\.com/(?:tapes/|play)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.historicfilms'


class HitboxIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:hitbox|smashcast)\\.tv/(?:[^/]+/)*videos?/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.hitbox'


class HitboxLiveIE(HitboxIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:hitbox|smashcast)\\.tv/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.hitbox'

    @classmethod
    def suitable(cls, url):
        return False if HitboxIE.suitable(url) else super(HitboxLiveIE, cls).suitable(url)


class HitRecordIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hitrecord\\.org/records/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.hitrecord'


class HornBunnyIE(LazyLoadExtractor):
    _VALID_URL = 'http?://(?:www\\.)?hornbunny\\.com/videos/(?P<title_dash>[a-z-]+)-(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.hornbunny'


class HotNewHipHopIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hotnewhiphop\\.com/.*\\.(?P<id>.*)\\.html'
    _module = 'haruhi_dl.extractor.hotnewhiphop'


class HotStarBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.hotstar'


class HotStarIE(HotStarBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?hotstar\\.com/(?:.+?[/-])?(?P<id>\\d{10})'
    _module = 'haruhi_dl.extractor.hotstar'


class HotStarPlaylistIE(HotStarBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?hotstar\\.com/tv/[^/]+/s-\\w+/list/[^/]+/t-(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.hotstar'


class HowcastIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?howcast\\.com/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.howcast'


class HowStuffWorksIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[\\da-z-]+\\.(?:howstuffworks|stuff(?:(?:youshould|theydontwantyouto)know|toblowyourmind|momnevertoldyou)|(?:brain|car)stuffshow|fwthinking|geniusstuff)\\.com/(?:[^/]+/)*(?:\\d+-)?(?P<id>.+?)-video\\.htm'
    _module = 'haruhi_dl.extractor.howstuffworks'


class HRTiBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.hrti'


class HRTiIE(HRTiBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            hrti:(?P<short_id>[0-9]+)|\n                            https?://\n                                hrti\\.hrt\\.hr/(?:\\#/)?video/show/(?P<id>[0-9]+)/(?P<display_id>[^/]+)?\n                        )\n                    '
    _module = 'haruhi_dl.extractor.hrti'


class HRTiPlaylistIE(HRTiBaseIE):
    _VALID_URL = 'https?://hrti\\.hrt\\.hr/(?:#/)?video/list/category/(?P<id>[0-9]+)/(?P<display_id>[^/]+)?'
    _module = 'haruhi_dl.extractor.hrti'


class HuajiaoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?huajiao\\.com/l/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.huajiao'


class HuffPostIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(embed\\.)?live\\.huffingtonpost\\.com/\n        (?:\n            r/segment/[^/]+/|\n            HPLEmbedPlayer/\\?segmentId=\n        )\n        (?P<id>[0-9a-f]+)'
    _module = 'haruhi_dl.extractor.huffpost'


class HungamaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?hungama\\.com/\n                        (?:\n                            (?:video|movie)/[^/]+/|\n                            tv-show/(?:[^/]+/){2}\\d+/episode/[^/]+/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.hungama'


class HungamaSongIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hungama\\.com/song/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.hungama'


class HypemIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?hypem\\.com/track/(?P<id>[0-9a-z]{5})'
    _module = 'haruhi_dl.extractor.hypem'


class IGNIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.+?\\.ign\\.com/(?:[^/]+/)?(?P<type>videos|show_videos|articles|feature|(?:[^/]+/\\d+/video))(/.+)?/(?P<name_or_id>.+)'
    _module = 'haruhi_dl.extractor.ign'


class OneUPIE(IGNIE):
    _VALID_URL = 'https?://gamevideos\\.1up\\.com/(?P<type>video)/id/(?P<name_or_id>.+)\\.html'
    _module = 'haruhi_dl.extractor.ign'


class PCMagIE(IGNIE):
    _VALID_URL = 'https?://(?:www\\.)?pcmag\\.com/(?P<type>videos|article2)(/.+)?/(?P<name_or_id>.+)'
    _module = 'haruhi_dl.extractor.ign'


class ImdbIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www|m)\\.imdb\\.com/(?:video|title|list).*?[/-]vi(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.imdb'


class ImdbListIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?imdb\\.com/list/ls(?P<id>\\d{9})(?!/videoplayer/vi\\d+)'
    _module = 'haruhi_dl.extractor.imdb'


class ImgurIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/(?!(?:a|gallery|(?:t(?:opic)?|r)/[^/]+)/)(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.imgur'


class ImgurGalleryIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/(?:gallery|(?:t(?:opic)?|r)/[^/]+)/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.imgur'


class ImgurAlbumIE(ImgurGalleryIE):
    _VALID_URL = 'https?://(?:i\\.)?imgur\\.com/a/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.imgur'


class InaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ina\\.fr/(?:video|audio)/(?P<id>[A-Z0-9_]+)'
    _module = 'haruhi_dl.extractor.ina'


class IncIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?inc\\.com/(?:[^/]+/)+(?P<id>[^.]+).html'
    _module = 'haruhi_dl.extractor.inc'


class IndavideoEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:embed\\.)?indavideo\\.hu/player/video/|assets\\.indavideo\\.hu/swf/player\\.swf\\?.*\\b(?:v(?:ID|id))=)(?P<id>[\\da-f]+)'
    _module = 'haruhi_dl.extractor.indavideo'


class InfoQIE(BokeCCBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?infoq\\.com/(?:[^/]+/)+(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.infoq'


class InstagramIE(LazyLoadExtractor):
    _VALID_URL = '(?P<url>https?://(?:www\\.)?instagram\\.com/(?:p|tv)/(?P<id>[^/?#&]+))'
    _module = 'haruhi_dl.extractor.instagram'


class InstagramPlaylistIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.instagram'


class InstagramUserIE(InstagramPlaylistIE):
    _VALID_URL = 'https?://(?:www\\.)?instagram\\.com/(?P<id>[^/]{2,})/?(?:$|[?#])'
    _module = 'haruhi_dl.extractor.instagram'


class InstagramTagIE(InstagramPlaylistIE):
    _VALID_URL = 'https?://(?:www\\.)?instagram\\.com/explore/tags/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.instagram'


class InternazionaleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?internazionale\\.it/video/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.internazionale'


class InternetVideoArchiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.internetvideoarchive\\.net/(?:player|flash/players)/.*?\\?.*?publishedid.*?'
    _module = 'haruhi_dl.extractor.internetvideoarchive'


class IplaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ipla\\.tv/.+/(?P<id>[0-9a-fA-F]+)'
    _module = 'haruhi_dl.extractor.ipla'


class IPrimaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+)\\.iprima\\.cz/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.iprima'


class IqiyiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:[^.]+\\.)?iqiyi\\.com|www\\.pps\\.tv)/.+\\.html'
    _module = 'haruhi_dl.extractor.iqiyi'


class Ir90TvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?90tv\\.ir/video/(?P<id>[0-9]+)/.*'
    _module = 'haruhi_dl.extractor.ir90tv'


class ITVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?itv\\.com/hub/[^/]+/(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.itv'


class ITVBTCCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?itv\\.com/btcc/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.itv'


class IviIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ivi\\.(?:ru|tv)/(?:watch/(?:[^/]+/)?|video/player\\?.*?videoId=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ivi'


class IviCompilationIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ivi\\.ru/watch/(?!\\d+)(?P<compilationid>[a-z\\d_-]+)(?:/season(?P<seasonid>\\d+))?$'
    _module = 'haruhi_dl.extractor.ivi'


class IvideonIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ivideon\\.com/tv/(?:[^/]+/)*camera/(?P<id>\\d+-[\\da-f]+)/(?P<camera_id>\\d+)'
    _module = 'haruhi_dl.extractor.ivideon'


class IwaraIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.|ecchi\\.)?iwara\\.tv/videos/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.iwara'


class IzleseneIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?:(?:www|m)\\.)?izlesene\\.com/\n        (?:video|embedplayer)/(?:[^/]+/)?(?P<id>[0-9]+)\n        '
    _module = 'haruhi_dl.extractor.izlesene'


class JamendoIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            licensing\\.jamendo\\.com/[^/]+|\n                            (?:www\\.)?jamendo\\.com\n                        )\n                        /track/(?P<id>[0-9]+)(?:/(?P<display_id>[^/?#&]+))?\n                    '
    _module = 'haruhi_dl.extractor.jamendo'


class JamendoAlbumIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?jamendo\\.com/album/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.jamendo'


class JeuxVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.*?\\.jeuxvideo\\.com/.*/(.*?)\\.htm'
    _module = 'haruhi_dl.extractor.jeuxvideo'


class JoveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?jove\\.com/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.jove'


class JojIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?:\n                        joj:|\n                        https?://media\\.joj\\.sk/embed/\n                    )\n                    (?P<id>[^/?#^]+)\n                '
    _module = 'haruhi_dl.extractor.joj'


class JWPlatformIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://(?:content\\.jwplatform|cdn\\.jwplayer)\\.com/(?:(?:feed|player|thumb|preview)s|jw6|v2/media)/|jwplatform:)(?P<id>[a-zA-Z0-9]{8})'
    _module = 'haruhi_dl.extractor.jwplatform'


class KakaoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:play-)?tv\\.kakao\\.com/(?:channel/\\d+|embed/player)/cliplink/(?P<id>\\d+|[^?#&]+@my)'
    _module = 'haruhi_dl.extractor.kakao'


class KalturaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                (?:\n                    kaltura:(?P<partner_id>\\d+):(?P<id>[0-9a-z_]+)|\n                    https?://\n                        (:?(?:www|cdnapi(?:sec)?)\\.)?kaltura\\.com(?::\\d+)?/\n                        (?:\n                            (?:\n                                # flash player\n                                index\\.php/(?:kwidget|extwidget/preview)|\n                                # html5 player\n                                html5/html5lib/[^/]+/mwEmbedFrame\\.php\n                            )\n                        )(?:/(?P<path>[^?]+))?(?:\\?(?P<query>.*))?\n                )\n                '
    _module = 'haruhi_dl.extractor.kaltura'


class KanalPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kanal(?P<channel_id>5|9|11)play\\.se/(?:#!/)?(?:play/)?program/\\d+/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.kanalplay'


class KankanIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.*?\\.)?kankan\\.com/.+?/(?P<id>\\d+)\\.shtml'
    _module = 'haruhi_dl.extractor.kankan'


class KaraoketvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?karaoketv\\.co\\.il/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.karaoketv'


class KarriereVideosIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?karrierevideos\\.at(?:/[^/]+)+/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.karrierevideos'


class KeezMoviesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?keezmovies\\.com/video/(?:(?P<display_id>[^/]+)-)?(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.keezmovies'


class ExtremeTubeIE(KeezMoviesIE):
    _VALID_URL = 'https?://(?:www\\.)?extremetube\\.com/(?:[^/]+/)?video/(?P<id>[^/#?&]+)'
    _module = 'haruhi_dl.extractor.extremetube'


class KetnetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ketnet\\.be/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.ketnet'


class KhanAcademyIE(LazyLoadExtractor):
    _VALID_URL = '^https?://(?:(?:www|api)\\.)?khanacademy\\.org/(?P<key>[^/]+)/(?:[^/]+/){,2}(?P<id>[^?#/]+)(?:$|[?#])'
    _module = 'haruhi_dl.extractor.khanacademy'


class KickStarterIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kickstarter\\.com/projects/(?P<id>[^/]*)/.*'
    _module = 'haruhi_dl.extractor.kickstarter'


class KinjaEmbedIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:[^.]+\\.)?\n        (?:\n            avclub|\n            clickhole|\n            deadspin|\n            gizmodo|\n            jalopnik|\n            jezebel|\n            kinja|\n            kotaku|\n            lifehacker|\n            splinternews|\n            the(?:inventory|onion|root|takeout)\n        )\\.com/\n        (?:\n            ajax/inset|\n            embed/video\n        )/iframe\\?.*?\\bid=\n        (?P<type>\n            fb|\n            imgur|\n            instagram|\n            jwp(?:layer)?-video|\n            kinjavideo|\n            mcp|\n            megaphone|\n            ooyala|\n            soundcloud(?:-playlist)?|\n            tumblr-post|\n            twitch-stream|\n            twitter|\n            ustream-channel|\n            vimeo|\n            vine|\n            youtube-(?:list|video)\n        )-(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.kinja'


class KinoPoiskIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kinopoisk\\.ru/film/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.kinopoisk'


class KonserthusetPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:konserthusetplay|rspoplay)\\.se/\\?.*\\bm=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.konserthusetplay'


class KrasViewIE(LazyLoadExtractor):
    _VALID_URL = 'https?://krasview\\.ru/(?:video|embed)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.krasview'


class Ku6IE(LazyLoadExtractor):
    _VALID_URL = 'https?://v\\.ku6\\.com/show/(?P<id>[a-zA-Z0-9\\-\\_]+)(?:\\.)*html'
    _module = 'haruhi_dl.extractor.ku6'


class KUSIIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kusi\\.com/(?P<path>story/.+|video\\?clipId=(?P<clipId>\\d+))'
    _module = 'haruhi_dl.extractor.kusi'


class KuwoBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoIE(KuwoBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/yinyue/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoAlbumIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/album/(?P<id>\\d+?)/'
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoChartIE(LazyLoadExtractor):
    _VALID_URL = 'https?://yinyue\\.kuwo\\.cn/billboard_(?P<id>[^.]+).htm'
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoSingerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/mingxing/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoCategoryIE(LazyLoadExtractor):
    _VALID_URL = 'https?://yinyue\\.kuwo\\.cn/yy/cinfo_(?P<id>\\d+?).htm'
    _module = 'haruhi_dl.extractor.kuwo'


class KuwoMvIE(KuwoBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?kuwo\\.cn/mv/(?P<id>\\d+?)/'
    _module = 'haruhi_dl.extractor.kuwo'


class LA7IE(LazyLoadExtractor):
    _VALID_URL = '(?x)(https?://)?(?:\n        (?:www\\.)?la7\\.it/([^/]+)/(?:rivedila7|video)/|\n        tg\\.la7\\.it/repliche-tgla7\\?id=\n    )(?P<id>.+)'
    _module = 'haruhi_dl.extractor.la7'


class Laola1TvEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/titanplayer\\.php\\?.*?\\bvideoid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.laola1tv'


class Laola1TvBaseIE(Laola1TvEmbedIE):
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/titanplayer\\.php\\?.*?\\bvideoid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.laola1tv'


class Laola1TvIE(Laola1TvBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?laola1\\.tv/[a-z]+-[a-z]+/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.laola1tv'


class EHFTVIE(Laola1TvBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ehftv\\.com/[a-z]+(?:-[a-z]+)?/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.laola1tv'


class ITTFIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tv\\.ittf\\.com/video/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.laola1tv'


class LBRYIE(LazyLoadExtractor):
    _VALID_URL = 'lbry://(?:@[^#]+#[^/]+/)?(?P<id>[^@][^#]*)#[a-z0-9]+'
    _module = 'haruhi_dl.extractor.lbry'


class LCIIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lci\\.fr/[^/]+/[\\w-]+-(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.lci'


class LcpPlayIE(ArkenaIE):
    _VALID_URL = 'https?://play\\.lcp\\.fr/embed/(?P<id>[^/]+)/(?P<account_id>[^/]+)/[^/]+/[^/]+'
    _module = 'haruhi_dl.extractor.lcp'


class LcpIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lcp\\.fr/(?:[^/]+/)*(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.lcp'


class Lecture2GoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://lecture2go\\.uni-hamburg\\.de/veranstaltungen/-/v/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.lecture2go'


class LecturioBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.lecturio'


class LecturioIE(LecturioBaseIE):
    _VALID_URL = '(?x)\n                    https://\n                        (?:\n                            app\\.lecturio\\.com/([^/]+/(?P<nt>[^/?#&]+)\\.lecture|(?:\\#/)?lecture/c/\\d+/(?P<id>\\d+))|\n                            (?:www\\.)?lecturio\\.de/[^/]+/(?P<nt_de>[^/?#&]+)\\.vortrag\n                        )\n                    '
    _module = 'haruhi_dl.extractor.lecturio'


class LecturioCourseIE(LecturioBaseIE):
    _VALID_URL = 'https://app\\.lecturio\\.com/(?:[^/]+/(?P<nt>[^/?#&]+)\\.course|(?:#/)?course/c/(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.lecturio'


class LecturioDeCourseIE(LecturioBaseIE):
    _VALID_URL = 'https://(?:www\\.)?lecturio\\.de/[^/]+/(?P<id>[^/?#&]+)\\.kurs'
    _module = 'haruhi_dl.extractor.lecturio'


class LeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.le\\.com/ptv/vplay|(?:sports\\.le|(?:www\\.)?lesports)\\.com/(?:match|video))/(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.leeco'


class LePlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[a-z]+\\.le\\.com/(?!video)[a-z]+/(?P<id>[a-z0-9_]+)'
    _module = 'haruhi_dl.extractor.leeco'

    @classmethod
    def suitable(cls, url):
        return False if LeIE.suitable(url) else super(LePlaylistIE, cls).suitable(url)


class LetvCloudIE(LazyLoadExtractor):
    _VALID_URL = 'https?://yuntv\\.letv\\.com/bcloud.html\\?.+'
    _module = 'haruhi_dl.extractor.leeco'


class LEGOIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lego\\.com/(?P<locale>[a-z]{2}-[a-z]{2})/(?:[^/]+/)*videos/(?:[^/]+/)*[^/?#]+-(?P<id>[0-9a-f]{32})'
    _module = 'haruhi_dl.extractor.lego'


class LemondeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?lemonde\\.fr/(?:[^/]+/)*(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.lemonde'


class LentaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lenta\\.ru/[^/]+/\\d+/\\d+/\\d+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.lenta'


class LibraryOfCongressIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?loc\\.gov/(?:item/|today/cyberlc/feature_wdesc\\.php\\?.*\\brec=)(?P<id>[0-9a-z_.]+)'
    _module = 'haruhi_dl.extractor.libraryofcongress'


class LibsynIE(LazyLoadExtractor):
    _VALID_URL = '(?P<mainurl>https?://html5-player\\.libsyn\\.com/embed/episode/id/(?P<id>[0-9]+))'
    _module = 'haruhi_dl.extractor.libsyn'


class LifeNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://life\\.ru/t/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.lifenews'


class LifeEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://embed\\.life\\.ru/(?:embed|video)/(?P<id>[\\da-f]{32})'
    _module = 'haruhi_dl.extractor.lifenews'


class LimelightBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.limelight'


class LimelightMediaIE(LimelightBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:media:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bmediaId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '
    _module = 'haruhi_dl.extractor.limelight'


class LimelightChannelIE(LimelightBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:channel:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bchannelId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '
    _module = 'haruhi_dl.extractor.limelight'


class LimelightChannelListIE(LimelightBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            limelight:channel_list:|\n                            https?://\n                                (?:\n                                    link\\.videoplatform\\.limelight\\.com/media/|\n                                    assets\\.delvenetworks\\.com/player/loader\\.swf\n                                )\n                                \\?.*?\\bchannelListId=\n                        )\n                        (?P<id>[a-z0-9]{32})\n                    '
    _module = 'haruhi_dl.extractor.limelight'


class LineTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tv\\.line\\.me/v/(?P<id>\\d+)_[^/]+-(?P<segment>ep\\d+-\\d+)'
    _module = 'haruhi_dl.extractor.line'


class LinkedInPostIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n    https?://(?:www\\.)?linkedin\\.com/\n        (?:feed/update/urn:li:activity:\n        |posts/[^/]+?-)\n    (?P<id>\\d{19})\n    '
    _module = 'haruhi_dl.extractor.linkedin'


class LinkedInLearningBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.linkedin'


class LinkedInLearningIE(LinkedInLearningBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?linkedin\\.com/learning/(?P<course_slug>[^/]+)/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.linkedin'


class LinkedInLearningCourseIE(LinkedInLearningBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?linkedin\\.com/learning/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.linkedin'

    @classmethod
    def suitable(cls, url):
        return False if LinkedInLearningIE.suitable(url) else super(LinkedInLearningCourseIE, cls).suitable(url)


class LinuxAcademyIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?linuxacademy\\.com/cp/\n                        (?:\n                            courses/lesson/course/(?P<chapter_id>\\d+)/lesson/(?P<lesson_id>\\d+)|\n                            modules/view/id/(?P<course_id>\\d+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.linuxacademy'


class LiTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?litv\\.tv/(?:vod|promo)/[^/]+/(?:content\\.do)?\\?.*?\\b(?:content_)?id=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.litv'


class LiveJournalIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^.]+\\.)?livejournal\\.com/video/album/\\d+.+?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.livejournal'


class LiveLeakIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:\\w+\\.)?liveleak\\.com/view\\?.*?\\b[it]=(?P<id>[\\w_]+)'
    _module = 'haruhi_dl.extractor.liveleak'


class LiveLeakEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?liveleak\\.com/ll_embed\\?.*?\\b(?P<kind>[ift])=(?P<id>[\\w_]+)'
    _module = 'haruhi_dl.extractor.liveleak'


class LivestreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:new\\.)?livestream\\.com/(?:accounts/(?P<account_id>\\d+)|(?P<account_name>[^/]+))/(?:events/(?P<event_id>\\d+)|(?P<event_name>[^/]+))(?:/videos/(?P<id>\\d+))?'
    _module = 'haruhi_dl.extractor.livestream'


class LivestreamOriginalIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://original\\.livestream\\.com/\n        (?P<user>[^/\\?#]+)(?:/(?P<type>video|folder)\n        (?:(?:\\?.*?Id=|/)(?P<id>.*?)(&|$))?)?\n        '
    _module = 'haruhi_dl.extractor.livestream'


class LivestreamShortenerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://livestre\\.am/(?P<id>.+)'
    _module = 'haruhi_dl.extractor.livestream'


class LnkGoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lnk(?:go)?\\.(?:alfa\\.)?lt/(?:visi-video/[^/]+|video)/(?P<id>[A-Za-z0-9-]+)(?:/(?P<episode_id>\\d+))?'
    _module = 'haruhi_dl.extractor.lnkgo'


class LocalNews8IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?localnews8\\.com/(?:[^/]+/)*(?P<display_id>[^/]+)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.localnews8'


class NuevoBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nuevo'


class LoveHomePornIE(NuevoBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?lovehomeporn\\.com/video/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.lovehomeporn'


class LRTIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lrt\\.lt/mediateka/irasas/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.lrt'


class LurkerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?lurker\\.(?:pl|land)/post/(?P<id>[A-Za-z\\d]{9})'
    _module = 'haruhi_dl.extractor.lurker'


class LyndaBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.lynda'


class LyndaIE(LyndaBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?:lynda\\.com|educourse\\.ga)/\n                        (?:\n                            (?:[^/]+/){2,3}(?P<course_id>\\d+)|\n                            player/embed\n                        )/\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.lynda'


class LyndaCourseIE(LyndaBaseIE):
    _VALID_URL = 'https?://(?:www|m)\\.(?:lynda\\.com|educourse\\.ga)/(?P<coursepath>(?:[^/]+/){2,3}(?P<courseid>\\d+))-2\\.html'
    _module = 'haruhi_dl.extractor.lynda'


class M6IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?m6\\.fr/[^/]+/videos/(?P<id>\\d+)-[^\\.]+\\.html'
    _module = 'haruhi_dl.extractor.m6'


class MailRuIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|m)\\.)?my\\.mail\\.ru/+\n                        (?:\n                            video/.*\\#video=/?(?P<idv1>(?:[^/]+/){3}\\d+)|\n                            (?:(?P<idv2prefix>(?:[^/]+/+){2})video/(?P<idv2suffix>[^/]+/\\d+))\\.html|\n                            (?:video/embed|\\+/video/meta)/(?P<metaid>\\d+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.mailru'


class MailRuMusicSearchBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.mailru'


class MailRuMusicIE(MailRuMusicSearchBaseIE):
    _VALID_URL = 'https?://my\\.mail\\.ru/+music/+songs/+[^/?#&]+-(?P<id>[\\da-f]+)'
    _module = 'haruhi_dl.extractor.mailru'


class MailRuMusicSearchIE(MailRuMusicSearchBaseIE):
    _VALID_URL = 'https?://my\\.mail\\.ru/+music/+search/+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.mailru'


class MallTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|sk)\\.)?mall\\.tv/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.malltv'


class MangomoloBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.mangomolo'


class MangomoloVideoIE(MangomoloBaseIE):
    _VALID_URL = 'https?://(?:admin\\.mangomolo\\.com/analytics/index\\.php/customers/embed/|player\\.mangomolo\\.com/v1/)video\\?.*?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.mangomolo'


class MangomoloLiveIE(MangomoloBaseIE):
    _VALID_URL = 'https?://(?:admin\\.mangomolo\\.com/analytics/index\\.php/customers/embed/|player\\.mangomolo\\.com/v1/)(live|index)\\?.*?\\bchannelid=(?P<id>(?:[A-Za-z0-9+/=]|%2B|%2F|%3D)+)'
    _module = 'haruhi_dl.extractor.mangomolo'


class ManyVidsIE(LazyLoadExtractor):
    _VALID_URL = '(?i)https?://(?:www\\.)?manyvids\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.manyvids'


class MarkizaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?videoarchiv\\.markiza\\.sk/(?:video/(?:[^/]+/)*|embed/)(?P<id>\\d+)(?:[_/]|$)'
    _module = 'haruhi_dl.extractor.markiza'


class MarkizaPageIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:[^/]+\\.)?markiza|tvnoviny)\\.sk/(?:[^/]+/)*(?P<id>\\d+)_'
    _module = 'haruhi_dl.extractor.markiza'

    @classmethod
    def suitable(cls, url):
        return False if MarkizaIE.suitable(url) else super(MarkizaPageIE, cls).suitable(url)


class MastodonSHIE(LazyLoadSelfhostedExtractor):
    _VALID_URL = 'mastodon:(?P<host>[^:]+):(?P<id>.+)'
    _module = 'haruhi_dl.extractor.mastodon'

    _SH_VALID_URL = '(?x)\n        https?://\n            (?P<host>[^/\\s]+)/\n                (?:\n                    # mastodon\n                    @[a-zA-Z0-9_]+\n                    # gab social\n                    |[a-zA-Z0-9_]+/posts\n                    # mastodon legacy (?)\n                    |users/[a-zA-Z0-9_]+/statuses\n                    # pleroma\n                    |notice\n                    # pleroma (OStatus standard?) - https://git.pleroma.social/pleroma/pleroma/-/blob/e9859b68fcb9c38b2ec27a45ffe0921e8d78b5e1/lib/pleroma/web/router.ex#L607\n                    |objects\n                    |activities\n                )/(?P<id>[0-9a-zA-Z-]+)\n    '
    _SH_VALID_CONTENT_STRINGS = (',"settings":{"known_fediverse":', '<li><a href="https://docs.joinmastodon.org/">Documentation</a></li>', '<title>Pleroma</title>', '<noscript>To use Pleroma, please enable JavaScript.</noscript>', 'Alternatively, try one of the <a href="https://apps.gab.com">native apps</a> for Gab Social for your platform.')
    _SH_VALID_CONTENT_REGEXES = ('<script id=[\\\'"]initial-state[\\\'"] type=[\\\'"]application/json[\\\'"]>{"meta":{"streaming_api_base_url":"wss://',)


class MassengeschmackTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?massengeschmack\\.tv/play/(?P<id>[^?&#]+)'
    _module = 'haruhi_dl.extractor.massengeschmacktv'


class MatchTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://matchtv\\.ru(?:/on-air|/?#live-player)'
    _module = 'haruhi_dl.extractor.matchtv'


class MDRIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:mdr|kika)\\.de/(?:.*)/[a-z-]+-?(?P<id>\\d+)(?:_.+?)?\\.html'
    _module = 'haruhi_dl.extractor.mdr'


class ThePlatformBaseIE(OnceIE):
    _VALID_URL = 'https?://.+?\\.unicornmedia\\.com/now/(?:ads/vmap/)?[^/]+/[^/]+/(?P<domain_id>[^/]+)/(?P<application_id>[^/]+)/(?:[^/]+/)?(?P<media_item_id>[^/]+)/content\\.(?:once|m3u8|mp4)'
    _module = 'haruhi_dl.extractor.theplatform'


class MediasetIE(ThePlatformBaseIE):
    _VALID_URL = '(?x)\n                    (?:\n                        mediaset:|\n                        https?://\n                            (?:(?:www|static3)\\.)?mediasetplay\\.mediaset\\.it/\n                            (?:\n                                (?:video|on-demand)/(?:[^/]+/)+[^/]+_|\n                                player/index\\.html\\?.*?\\bprogramGuid=\n                            )\n                    )(?P<id>[0-9A-Z]{16,})\n                    '
    _module = 'haruhi_dl.extractor.mediaset'


class MediasiteIE(LazyLoadExtractor):
    _VALID_URL = '(?xi)https?://[^/]+/Mediasite/(?:Play|Showcase/(?:default|livebroadcast)/Presentation)/(?P<id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))(?P<query>\\?[^#]+|)'
    _module = 'haruhi_dl.extractor.mediasite'


class MediasiteCatalogIE(LazyLoadExtractor):
    _VALID_URL = '(?xi)\n                        (?P<url>https?://[^/]+/Mediasite)\n                        /Catalog/Full/\n                        (?P<catalog_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                        (?:\n                            /(?P<current_folder_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                            /(?P<root_dynamic_folder_id>(?:[0-9a-f]{32,34}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12,14}))\n                        )?\n                    '
    _module = 'haruhi_dl.extractor.mediasite'


class MediasiteNamedCatalogIE(LazyLoadExtractor):
    _VALID_URL = '(?xi)(?P<url>https?://[^/]+/Mediasite)/Catalog/catalogs/(?P<catalog_name>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.mediasite'


class MediciIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?medici\\.tv/#!/(?P<id>[^?#&]+)'
    _module = 'haruhi_dl.extractor.medici'


class MegaphoneIE(LazyLoadExtractor):
    _VALID_URL = 'https://player\\.megaphone\\.fm/(?P<id>[A-Z0-9]+)'
    _module = 'haruhi_dl.extractor.megaphone'


class MeipaiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?meipai\\.com/media/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.meipai'


class MelonVODIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vod\\.melon\\.com/video/detail2\\.html?\\?.*?mvId=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.melonvod'


class METAIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.meta\\.ua/(?:iframe/)?(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.meta'


class MetacafeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?metacafe\\.com/watch/(?P<video_id>[^/]+)/(?P<display_id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.metacafe'


class MetacriticIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?metacritic\\.com/.+?/trailers/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.metacritic'


class MgoonIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?\n    (?:(:?m\\.)?mgoon\\.com/(?:ch/(?:.+)/v|play/view)|\n        video\\.mgoon\\.com)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.mgoon'


class MGTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mgtv\\.com/(v|b)/(?:[^/]+/)*(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.mgtv'


class MiaoPaiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?miaopai\\.com/show/(?P<id>[-A-Za-z0-9~_]+)'
    _module = 'haruhi_dl.extractor.miaopai'


class MicrosoftVirtualAcademyBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.microsoftvirtualacademy'


class MicrosoftVirtualAcademyIE(MicrosoftVirtualAcademyBaseIE):
    _VALID_URL = '(?:mva:|https?://(?:mva\\.microsoft|(?:www\\.)?microsoftvirtualacademy)\\.com/[^/]+/training-courses/[^/?#&]+-)(?P<course_id>\\d+)(?::|\\?l=)(?P<id>[\\da-zA-Z]+_\\d+)'
    _module = 'haruhi_dl.extractor.microsoftvirtualacademy'


class MicrosoftVirtualAcademyCourseIE(MicrosoftVirtualAcademyBaseIE):
    _VALID_URL = '(?:mva:course:|https?://(?:mva\\.microsoft|(?:www\\.)?microsoftvirtualacademy)\\.com/[^/]+/training-courses/(?P<display_id>[^/?#&]+)-)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.microsoftvirtualacademy'

    @classmethod
    def suitable(cls, url):
        return False if MicrosoftVirtualAcademyIE.suitable(url) else super(
            MicrosoftVirtualAcademyCourseIE, cls).suitable(url)


class MinistryGridIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ministrygrid\\.com/([^/?#]*/)*(?P<id>[^/#?]+)/?(?:$|[?#])'
    _module = 'haruhi_dl.extractor.ministrygrid'


class MinotoIE(LazyLoadExtractor):
    _VALID_URL = '(?:minoto:|https?://(?:play|iframe|embed)\\.minoto-video\\.com/(?P<player_id>[0-9]+)/)(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.minoto'


class MioMioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?miomio\\.tv/watch/cc(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.miomio'


class TechTVMITIE(LazyLoadExtractor):
    _VALID_URL = 'https?://techtv\\.mit\\.edu/(?:videos|embeds)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.mit'


class OCWMITIE(LazyLoadExtractor):
    _VALID_URL = '^https?://ocw\\.mit\\.edu/courses/(?P<topic>[a-z0-9\\-]+)'
    _module = 'haruhi_dl.extractor.mit'


class MiTeleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mitele\\.es/(?:[^/]+/)+(?P<id>[^/]+)/player'
    _module = 'haruhi_dl.extractor.mitele'


class MixcloudBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.mixcloud'


class MixcloudIE(MixcloudBaseIE):
    _VALID_URL = 'https?://(?:(?:www|beta|m)\\.)?mixcloud\\.com/([^/]+)/(?!stream|uploads|favorites|listens|playlists)([^/]+)'
    _module = 'haruhi_dl.extractor.mixcloud'


class MixcloudPlaylistBaseIE(MixcloudBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.mixcloud'


class MixcloudUserIE(MixcloudPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?mixcloud\\.com/(?P<id>[^/]+)/(?P<type>uploads|favorites|listens|stream)?/?$'
    _module = 'haruhi_dl.extractor.mixcloud'


class MixcloudPlaylistIE(MixcloudPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?mixcloud\\.com/(?P<user>[^/]+)/playlists/(?P<playlist>[^/]+)/?$'
    _module = 'haruhi_dl.extractor.mixcloud'


class NHLBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nhl'


class MLBIE(NHLBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[\\da-z_-]+\\.)*(?P<site>mlb)\\.com/\n                        (?:\n                            (?:\n                                (?:[^/]+/)*c-|\n                                (?:\n                                    shared/video/embed/(?:embed|m-internal-embed)\\.html|\n                                    (?:[^/]+/)+(?:play|index)\\.jsp|\n                                )\\?.*?\\bcontent_id=\n                            )\n                            (?P<id>\\d+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.mlb'


class MnetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mnet\\.(?:com|interest\\.me)/tv/vod/(?:.*?\\bclip_id=)?(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.mnet'


class MoeVideoIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?P<host>(?:www\\.)?\n        (?:(?:moevideo|playreplay|videochart)\\.net|thesame\\.tv))/\n        (?:video|framevideo|embed)/(?P<id>[0-9a-z]+\\.[0-9A-Za-z]+)'
    _module = 'haruhi_dl.extractor.moevideo'


class MofosexIE(KeezMoviesIE):
    _VALID_URL = 'https?://(?:www\\.)?mofosex\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/?#&.]+)\\.html'
    _module = 'haruhi_dl.extractor.mofosex'


class MofosexEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mofosex\\.com/embed/?\\?.*?\\bvideoid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.mofosex'


class MojvideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mojvideo\\.com/video-(?P<display_id>[^/]+)/(?P<id>[a-f0-9]+)'
    _module = 'haruhi_dl.extractor.mojvideo'


class MorningstarIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|news)\\.)morningstar\\.com/[cC]over/video[cC]enter\\.aspx\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.morningstar'


class MotherlessIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?motherless\\.com/(?:g/[a-z0-9_]+/)?(?P<id>[A-Z0-9]+)'
    _module = 'haruhi_dl.extractor.motherless'


class MotherlessGroupIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?motherless\\.com/gv?/(?P<id>[a-z0-9_]+)'
    _module = 'haruhi_dl.extractor.motherless'

    @classmethod
    def suitable(cls, url):
        return (False if MotherlessIE.suitable(url)
                else super(MotherlessGroupIE, cls).suitable(url))


class MotorsportIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?motorsport\\.com/[^/?#]+/video/(?:[^/?#]+/)(?P<id>[^/]+)/?(?:$|[?#])'
    _module = 'haruhi_dl.extractor.motorsport'


class MovieClipsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?movieclips\\.com/videos/.+-(?P<id>\\d+)(?:\\?|$)'
    _module = 'haruhi_dl.extractor.movieclips'


class MoviezineIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?moviezine\\.se/video/(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.moviezine'


class MovingImageIE(LazyLoadExtractor):
    _VALID_URL = 'https?://movingimage\\.nls\\.uk/film/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.movingimage'


class MSNIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|preview)\\.)?msn\\.com/(?:[^/]+/)+(?P<display_id>[^/]+)/[a-z]{2}-(?P<id>[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.msn'


class MTVIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.com/(?:video-clips|(?:full-)?episodes)/(?P<id>[^/?#.]+)'
    _module = 'haruhi_dl.extractor.mtv'


class CMTIE(MTVIE):
    _VALID_URL = 'https?://(?:www\\.)?cmt\\.com/(?:videos|shows|(?:full-)?episodes|video-clips)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.cmt'


class MTVVideoIE(MTVServicesInfoExtractor):
    _VALID_URL = '(?x)^https?://\n        (?:(?:www\\.)?mtv\\.com/videos/.+?/(?P<videoid>[0-9]+)/[^/]+$|\n           m\\.mtv\\.com/videos/video\\.rbml\\?.*?id=(?P<mgid>[^&]+))'
    _module = 'haruhi_dl.extractor.mtv'


class MTVServicesEmbeddedIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://media\\.mtvnservices\\.com/embed/(?P<mgid>.+?)(\\?|/|$)'
    _module = 'haruhi_dl.extractor.mtv'


class MTVDEIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mtv\\.de/(?:musik/videoclips|folgen|news)/(?P<id>[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.mtv'


class MTVJapanIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mtvjapan\\.com/videos/(?P<id>[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.mtv'


class MuenchenTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?muenchen\\.tv/livestream'
    _module = 'haruhi_dl.extractor.muenchentv'


class MwaveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://mwave\\.interest\\.me/(?:[^/]+/)?mnettv/videodetail\\.m\\?searchVideoDetailVO\\.clip_id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.mwave'


class MwaveMeetGreetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://mwave\\.interest\\.me/(?:[^/]+/)?meetgreet/view/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.mwave'


class MyChannelsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?mychannels\\.com/.*(?P<id_type>video|production)_id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.mychannels'


class MySpaceIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        myspace\\.com/[^/]+/\n                        (?P<mediatype>\n                            video/[^/]+/(?P<video_id>\\d+)|\n                            music/song/[^/?#&]+-(?P<song_id>\\d+)-\\d+(?:[/?#&]|$)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.myspace'


class MySpaceAlbumIE(LazyLoadExtractor):
    _VALID_URL = 'https?://myspace\\.com/([^/]+)/music/album/(?P<title>.*-)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.myspace'


class MySpassIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?myspass\\.de/([^/]+/)*(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.myspass'


class SprutoBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vimple'


class MyviIE(SprutoBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            https?://\n                                (?:www\\.)?\n                                myvi\\.\n                                (?:\n                                    (?:ru/player|tv)/\n                                    (?:\n                                        (?:\n                                            embed/html|\n                                            flash|\n                                            api/Video/Get\n                                        )/|\n                                        content/preloader\\.swf\\?.*\\bid=\n                                    )|\n                                    ru/watch/\n                                )|\n                            myvi:\n                        )\n                        (?P<id>[\\da-zA-Z_-]+)\n                    '
    _module = 'haruhi_dl.extractor.myvi'


class MyviEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?myvi\\.tv/(?:[^?]+\\?.*?\\bv=|embed/)(?P<id>[\\da-z]+)'
    _module = 'haruhi_dl.extractor.myvi'

    @classmethod
    def suitable(cls, url):
        return False if MyviIE.suitable(url) else super(MyviEmbedIE, cls).suitable(url)


class MyVidsterIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?myvidster\\.com/video/(?P<id>\\d+)/'
    _module = 'haruhi_dl.extractor.myvidster'


class NationalGeographicVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.nationalgeographic\\.com/.*?'
    _module = 'haruhi_dl.extractor.nationalgeographic'


class NationalGeographicTVIE(FOXIE):
    _VALID_URL = 'https?://(?:www\\.)?nationalgeographic\\.com/tv/watch/(?P<id>[\\da-fA-F]+)'
    _module = 'haruhi_dl.extractor.nationalgeographic'


class NaverBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.naver'


class NaverIE(NaverBaseIE):
    _VALID_URL = 'https?://(?:m\\.)?tv(?:cast)?\\.naver\\.com/(?:v|embed)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.naver'


class NBAIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:watch\\.|www\\.)?nba\\.com/(?P<path>(?:[^/]+/)+(?P<id>[^?]*?))/?(?:/index\\.html)?(?:\\?.*)?$'
    _module = 'haruhi_dl.extractor.nba'


class CSNNEIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?csnne\\.com/video/(?P<id>[0-9a-z-]+)'
    _module = 'haruhi_dl.extractor.nbc'


class NBCIE(AdobePassIE):
    _VALID_URL = 'https?(?P<permalink>://(?:www\\.)?nbc\\.com/(?:classic-tv/)?[^/]+/video/[^/]+/(?P<id>n?\\d+))'
    _module = 'haruhi_dl.extractor.nbc'


class NBCOlympicsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://www\\.nbcolympics\\.com/video/(?P<id>[a-z-]+)'
    _module = 'haruhi_dl.extractor.nbc'


class NBCOlympicsStreamIE(AdobePassIE):
    _VALID_URL = 'https?://stream\\.nbcolympics\\.com/(?P<id>[0-9a-z-]+)'
    _module = 'haruhi_dl.extractor.nbc'


class NBCSportsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nbcsports\\.com//?(?:[^/]+/)+(?P<id>[0-9a-z-]+)'
    _module = 'haruhi_dl.extractor.nbc'


class NBCSportsStreamIE(AdobePassIE):
    _VALID_URL = 'https?://stream\\.nbcsports\\.com/.+?\\bpid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nbc'


class NBCSportsVPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vplayer\\.nbcsports\\.com/(?:[^/]+/)+(?P<id>[0-9a-zA-Z_]+)'
    _module = 'haruhi_dl.extractor.nbc'


class NDRBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ndr'


class NDRIE(NDRBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ndr\\.de/(?:[^/]+/)*(?P<id>[^/?#]+),[\\da-z]+\\.html'
    _module = 'haruhi_dl.extractor.ndr'


class NJoyIE(NDRBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?n-joy\\.de/(?:[^/]+/)*(?:(?P<display_id>[^/?#]+),)?(?P<id>[\\da-z]+)\\.html'
    _module = 'haruhi_dl.extractor.ndr'


class NDREmbedBaseIE(LazyLoadExtractor):
    _VALID_URL = '(?:ndr:(?P<id_s>[\\da-z]+)|https?://www\\.ndr\\.de/(?P<id>[\\da-z]+)-ppjson\\.json)'
    _module = 'haruhi_dl.extractor.ndr'


class NDREmbedIE(NDREmbedBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?ndr\\.de/(?:[^/]+/)*(?P<id>[\\da-z]+)-(?:player|externalPlayer)\\.html'
    _module = 'haruhi_dl.extractor.ndr'


class NJoyEmbedIE(NDREmbedBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?n-joy\\.de/(?:[^/]+/)*(?P<id>[\\da-z]+)-(?:player|externalPlayer)_[^/]+\\.html'
    _module = 'haruhi_dl.extractor.ndr'


class NDTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?ndtv\\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ndtv'


class NetzkinoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?netzkino\\.de/\\#!/(?P<category>[^/]+)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.netzkino'


class NerdCubedFeedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nerdcubed\\.co\\.uk/feed\\.json'
    _module = 'haruhi_dl.extractor.nerdcubed'


class NetEaseMusicBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?song\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicAlbumIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?album\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicSingerIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?artist\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicListIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?(playlist|discover/toplist)\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicMvIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?mv\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicProgramIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/?)program\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NetEaseMusicDjRadioIE(NetEaseMusicBaseIE):
    _VALID_URL = 'https?://music\\.163\\.com/(#/)?djradio\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.neteasemusic'


class NewgroundsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?newgrounds\\.com/(?:audio/listen|portal/view)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.newgrounds'


class NewgroundsPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?newgrounds\\.com/(?:collection|[^/]+/search/[^/]+)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.newgrounds'


class NewstubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?newstube\\.ru/media/(?P<id>.+)'
    _module = 'haruhi_dl.extractor.newstube'


class NextMediaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://hk\\.apple\\.nextmedia\\.com/[^/]+/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nextmedia'


class NextMediaActionNewsIE(NextMediaIE):
    _VALID_URL = 'https?://hk\\.dv\\.nextmedia\\.com/actionnews/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)/\\d+'
    _module = 'haruhi_dl.extractor.nextmedia'


class AppleDailyIE(NextMediaIE):
    _VALID_URL = 'https?://(www|ent)\\.appledaily\\.com\\.tw/[^/]+/[^/]+/[^/]+/(?P<date>\\d+)/(?P<id>\\d+)(/.*)?'
    _module = 'haruhi_dl.extractor.nextmedia'


class NextTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nexttv\\.com\\.tw/(?:[^/]+/)+(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nextmedia'


class NexxIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        (?:\n                            https?://api\\.nexx(?:\\.cloud|cdn\\.com)/v3/(?P<domain_id>\\d+)/videos/byid/|\n                            nexx:(?:(?P<domain_id_s>\\d+):)?|\n                            https?://arc\\.nexx\\.cloud/api/video/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.nexx'


class NexxEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://embed\\.nexx(?:\\.cloud|cdn\\.com)/\\d+/(?:video/)?(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nexx'


class NFLIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<host>\n                            (?:www\\.)?\n                            (?:\n                                (?:\n                                    nfl|\n                                    buffalobills|\n                                    miamidolphins|\n                                    patriots|\n                                    newyorkjets|\n                                    baltimoreravens|\n                                    bengals|\n                                    clevelandbrowns|\n                                    steelers|\n                                    houstontexans|\n                                    colts|\n                                    jaguars|\n                                    titansonline|\n                                    denverbroncos|\n                                    kcchiefs|\n                                    raiders|\n                                    chargers|\n                                    dallascowboys|\n                                    giants|\n                                    philadelphiaeagles|\n                                    redskins|\n                                    chicagobears|\n                                    detroitlions|\n                                    packers|\n                                    vikings|\n                                    atlantafalcons|\n                                    panthers|\n                                    neworleanssaints|\n                                    buccaneers|\n                                    azcardinals|\n                                    stlouisrams|\n                                    49ers|\n                                    seahawks\n                                )\\.com|\n                                .+?\\.clubs\\.nfl\\.com\n                            )\n                        )/\n                        (?:.+?/)*\n                        (?P<id>[^/#?&]+)\n                    '
    _module = 'haruhi_dl.extractor.nfl'


class NhkVodIE(LazyLoadExtractor):
    _VALID_URL = 'https?://www3\\.nhk\\.or\\.jp/nhkworld/(?P<lang>[a-z]{2})/ondemand/(?P<type>video|audio)/(?P<id>\\d{7}|[^/]+?-\\d{8}-\\d+)'
    _module = 'haruhi_dl.extractor.nhk'


class NHLIE(NHLBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>nhl|wch2016)\\.com/(?:[^/]+/)*c-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nhl'


class NickIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?P<domain>(?:(?:www|beta)\\.)?nick(?:jr)?\\.com)/(?:[^/]+/)?(?:videos/clip|[^/]+/videos)/(?P<id>[^/?#.]+)'
    _module = 'haruhi_dl.extractor.nick'


class NickBrIE(MTVServicesInfoExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?P<domain>(?:www\\.)?nickjr|mundonick\\.uol)\\.com\\.br|\n                            (?:www\\.)?nickjr\\.[a-z]{2}|\n                            (?:www\\.)?nickelodeonjunior\\.fr\n                        )\n                        /(?:programas/)?[^/]+/videos/(?:episodios/)?(?P<id>[^/?\\#.]+)\n                    '
    _module = 'haruhi_dl.extractor.nick'


class NickDeIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>nick\\.(?:de|com\\.pl|ch)|nickelodeon\\.(?:nl|be|at|dk|no|se))/[^/]+/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nick'


class NickNightIE(NickDeIE):
    _VALID_URL = 'https?://(?:www\\.)(?P<host>nicknight\\.(?:de|at|tv))/(?:playlist|shows)/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nick'


class NickRuIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)nickelodeon\\.(?:ru|fr|es|pt|ro|hu|com\\.tr)/[^/]+/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nick'


class NiconicoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.|secure\\.|sp\\.)?nicovideo\\.jp/watch/(?P<id>(?:[a-z]{2})?[0-9]+)'
    _module = 'haruhi_dl.extractor.niconico'


class NiconicoPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nicovideo\\.jp/mylist/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.niconico'


class NinatekaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://ninateka\\.pl/(?:film|audio)/(?P<id>[^/\\?#]+)'
    _module = 'haruhi_dl.extractor.ninateka'


class NineCNineMediaIE(LazyLoadExtractor):
    _VALID_URL = '9c9media:(?P<destination_code>[^:]+):(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ninecninemedia'


class NineGagIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?9gag(?:\\.com/tv|\\.tv)/(?:p|embed)/(?P<id>[a-zA-Z0-9]+)(?:/(?P<display_id>[^?#/]+))?'
    _module = 'haruhi_dl.extractor.ninegag'


class NineNowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?9now\\.com\\.au/(?:[^/]+/){2}(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.ninenow'


class NintendoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nintendo\\.com/(?:games/detail|nintendo-direct)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nintendo'


class NJPWWorldIE(LazyLoadExtractor):
    _VALID_URL = 'https?://njpwworld\\.com/p/(?P<id>[a-z0-9_]+)'
    _module = 'haruhi_dl.extractor.njpwworld'


class NobelPrizeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nobelprize\\.org/mediaplayer.*?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nobelprize'


class NocoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?noco\\.tv/emission/|player\\.noco\\.tv/\\?idvideo=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.noco'


class NonkTubeIE(NuevoBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?nonktube\\.com/(?:(?:video|embed)/|media/nuevo/embed\\.php\\?.*?\\bid=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nonktube'


class NoovoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?noovo\\.ca/videos/(?P<id>[^/]+/[^/?#&]+)'
    _module = 'haruhi_dl.extractor.noovo'


class NormalbootsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?normalboots\\.com/video/(?P<id>[0-9a-z-]*)/?$'
    _module = 'haruhi_dl.extractor.normalboots'


class NosVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nosvideo\\.com/(?:embed/|\\?v=)(?P<id>[A-Za-z0-9]{12})/?'
    _module = 'haruhi_dl.extractor.nosvideo'


class NovaEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://media\\.cms\\.nova\\.cz/embed/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nova'


class NovaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^.]+\\.)?(?P<site>tv(?:noviny)?|tn|novaplus|vymena|fanda|krasna|doma|prask)\\.nova\\.cz/(?:[^/]+/)+(?P<id>[^/]+?)(?:\\.html|/|$)'
    _module = 'haruhi_dl.extractor.nova'


class NownessBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nowness'


class NownessIE(NownessBaseIE):
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/(?:story|(?:series|category)/[^/]+)/(?P<id>[^/]+?)(?:$|[?#])'
    _module = 'haruhi_dl.extractor.nowness'


class NownessPlaylistIE(NownessBaseIE):
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/playlist/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nowness'


class NownessSeriesIE(NownessBaseIE):
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/series/(?P<id>[^/]+?)(?:$|[?#])'
    _module = 'haruhi_dl.extractor.nowness'


class NozIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?noz\\.de/video/(?P<id>[0-9]+)/'
    _module = 'haruhi_dl.extractor.noz'


class NPOBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.npo'


class NPOIE(NPOBaseIE):
    _VALID_URL = '(?x)\n                    (?:\n                        npo:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                npo\\.nl/(?:[^/]+/)*|\n                                (?:ntr|npostart)\\.nl/(?:[^/]+/){2,}|\n                                omroepwnl\\.nl/video/fragment/[^/]+__|\n                                (?:zapp|npo3)\\.nl/(?:[^/]+/){2,}\n                            )\n                        )\n                        (?P<id>[^/?#]+)\n                '
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NPOPlaylistBaseIE(NPOIE):
    _VALID_URL = '(?x)\n                    (?:\n                        npo:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                npo\\.nl/(?:[^/]+/)*|\n                                (?:ntr|npostart)\\.nl/(?:[^/]+/){2,}|\n                                omroepwnl\\.nl/video/fragment/[^/]+__|\n                                (?:zapp|npo3)\\.nl/(?:[^/]+/){2,}\n                            )\n                        )\n                        (?P<id>[^/?#]+)\n                '
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class AndereTijdenIE(NPOPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?anderetijden\\.nl/programma/(?:[^/]+/)+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NPOLiveIE(NPOBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?npo(?:start)?\\.nl/live(?:/(?P<id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.npo'


class NPORadioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?npo\\.nl/radio/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return False if NPORadioFragmentIE.suitable(url) else super(NPORadioIE, cls).suitable(url)


class NPORadioFragmentIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?npo\\.nl/radio/[^/]+/fragment/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.npo'


class NPODataMidEmbedIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.npo'


class SchoolTVIE(NPODataMidEmbedIE):
    _VALID_URL = 'https?://(?:www\\.)?schooltv\\.nl/video/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.npo'


class HetKlokhuisIE(NPODataMidEmbedIE):
    _VALID_URL = 'https?://(?:www\\.)?hetklokhuis\\.nl/[^/]+/\\d+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.npo'


class VPROIE(NPOPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:tegenlicht\\.)?vpro|2doc)\\.nl/(?:[^/]+/)*(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class WNLIE(NPOPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?omroepwnl\\.nl/video/detail/(?P<id>[^/]+)__\\d+'
    _module = 'haruhi_dl.extractor.npo'

    @classmethod
    def suitable(cls, url):
        return (False if any(ie.suitable(url)
                for ie in (NPOLiveIE, NPORadioIE, NPORadioFragmentIE))
                else super(NPOIE, cls).suitable(url))


class NprIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?npr\\.org/(?:sections/[^/]+/)?\\d{4}/\\d{2}/\\d{2}/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.npr'


class NRKBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nrk'


class NRKIE(NRKBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            nrk:|\n                            https?://\n                                (?:\n                                    (?:www\\.)?nrk\\.no/video/PS\\*|\n                                    v8[-.]psapi\\.nrk\\.no/mediaelement/\n                                )\n                            )\n                            (?P<id>[^?#&]+)\n                        '
    _module = 'haruhi_dl.extractor.nrk'


class NRKPlaylistBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nrk'


class NRKPlaylistIE(NRKPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?nrk\\.no/(?!video|skole)(?:[^/]+/)+(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.nrk'


class NRKSkoleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nrk\\.no/skole/?\\?.*\\bmediaId=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVIE(NRKBaseIE):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:tv|radio)\\.nrk(?:super)?\\.no/\n                            (?:serie(?:/[^/]+){1,2}|program)/\n                            (?![Ee]pisodes)(?P<id>[a-zA-Z]{4}\\d{8})\n                            (?:/\\d{2}-\\d{2}-\\d{4})?\n                            (?:\\#del=(?P<part_id>\\d+))?\n                    '
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVDirekteIE(NRKTVIE):
    _VALID_URL = 'https?://(?:tv|radio)\\.nrk\\.no/direkte/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVEpisodeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tv\\.nrk\\.no/serie/(?P<id>[^/]+/sesong/\\d+/episode/\\d+)'
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVEpisodesIE(NRKPlaylistBaseIE):
    _VALID_URL = 'https?://tv\\.nrk\\.no/program/[Ee]pisodes/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVSerieBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nrk'


class NRKTVSeasonIE(NRKTVSerieBaseIE):
    _VALID_URL = 'https?://tv\\.nrk\\.no/serie/[^/]+/sesong/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nrk'

    @classmethod
    def suitable(cls, url):
        return (False if NRKTVIE.suitable(url) or NRKTVEpisodeIE.suitable(url)
                else super(NRKTVSeasonIE, cls).suitable(url))


class NRKTVSeriesIE(NRKTVSerieBaseIE):
    _VALID_URL = 'https?://(?:tv|radio)\\.nrk(?:super)?\\.no/serie/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.nrk'

    @classmethod
    def suitable(cls, url):
        return (
            False if any(ie.suitable(url)
                         for ie in (NRKTVIE, NRKTVEpisodeIE, NRKTVSeasonIE))
            else super(NRKTVSeriesIE, cls).suitable(url))


class NRLTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nrl\\.com/tv(/[^/]+)*/(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.nrl'


class NTVCoJpCUIE(LazyLoadExtractor):
    _VALID_URL = 'https?://cu\\.ntv\\.co\\.jp/(?!program)(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.ntvcojp'


class NTVDeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?n-tv\\.de/mediathek/videos/[^/?#]+/[^/?#]+-article(?P<id>.+)\\.html'
    _module = 'haruhi_dl.extractor.ntvde'


class NTVRuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ntv\\.ru/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.ntvru'


class NYTimesBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.nytimes'


class NYTimesIE(NYTimesBaseIE):
    _VALID_URL = 'https?://(?:(?:www\\.)?nytimes\\.com/video/(?:[^/]+/)+?|graphics8\\.nytimes\\.com/bcvideo/\\d+(?:\\.\\d+)?/iframe/embed\\.html\\?videoId=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nytimes'


class NYTimesArticleIE(NYTimesBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?nytimes\\.com/(.(?<!video))*?/(?:[^/]+/)*(?P<id>[^.]+)(?:\\.html)?'
    _module = 'haruhi_dl.extractor.nytimes'


class NuvidIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www|m)\\.nuvid\\.com/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.nuvid'


class NZZIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?nzz\\.ch/(?:[^/]+/)*[^/?#]+-ld\\.(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.nzz'


class OdaTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?odatv\\.com/(?:mob|vid)_video\\.php\\?.*\\bid=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.odatv'


class OdnoklassnikiIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                https?://\n                    (?:(?:www|m|mobile)\\.)?\n                    (?:odnoklassniki|ok)\\.ru/\n                    (?:\n                        video(?:embed)?/|\n                        web-api/video/moviePlayer/|\n                        live/|\n                        dk\\?.*?st\\.mvId=\n                    )\n                    (?P<id>[\\d-]+)\n                '
    _module = 'haruhi_dl.extractor.odnoklassniki'


class OKOPressIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?oko\\.press/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.okopress'


class OktoberfestTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?oktoberfest-tv\\.de/[^/]+/[^/]+/video/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.oktoberfesttv'


class OnDemandKoreaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ondemandkorea\\.com/(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.ondemandkorea'


class OnetPlIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?:onet|businessinsider\\.com|plejada)\\.pl/(?:[^/]+/)+(?P<id>[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.onet'


class OnionStudiosIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?onionstudios\\.com/(?:video(?:s/[^/]+-|/)|embed\\?.*\\bid=)(?P<id>\\d+)(?!-)'
    _module = 'haruhi_dl.extractor.onionstudios'


class OnNetworkLoaderIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.onnetwork\\.tv/embed\\.php\\?(?:mid=(?P<mid>[^&]+))?(?:&?sid=(?P<sid>[^&\\s]+))?(?:&?cId=onn-cid-(?P<cid>\\d+))?(?:.+)?'
    _module = 'haruhi_dl.extractor.onnetwork'


class OnNetworkFrameIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.onnetwork\\.tv/frame84\\.php\\?(?:[^&]+&)*?mid=(?P<mid>[^&]+)&(?:[^&]+&)*?id=(?P<vid>[^&]+)'
    _module = 'haruhi_dl.extractor.onnetwork'


class OoyalaBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ooyala'


class OoyalaIE(OoyalaBaseIE):
    _VALID_URL = '(?:ooyala:|https?://.+?\\.ooyala\\.com/.*?(?:embedCode|ec)=)(?P<id>.+?)(&|$)'
    _module = 'haruhi_dl.extractor.ooyala'


class OoyalaExternalIE(OoyalaBaseIE):
    _VALID_URL = '(?x)\n                    (?:\n                        ooyalaexternal:|\n                        https?://.+?\\.ooyala\\.com/.*?\\bexternalId=\n                    )\n                    (?P<partner_id>[^:]+)\n                    :\n                    (?P<id>.+)\n                    (?:\n                        :|\n                        .*?&pcode=\n                    )\n                    (?P<pcode>.+?)\n                    (?:&|$)\n                    '
    _module = 'haruhi_dl.extractor.ooyala'


class OpenFMIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?open\\.fm/stacja/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.openfm'


class OraTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:ora\\.tv|unsafespeech\\.com)/([^/]+/)*(?P<id>[^/\\?#]+)'
    _module = 'haruhi_dl.extractor.ora'


class ORFTVthekIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tvthek\\.orf\\.at/(?:[^/]+/)+(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFRadioIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.orf'


class ORFFM4IE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>fm4)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>4\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFFM4StoryIE(LazyLoadExtractor):
    _VALID_URL = 'https?://fm4\\.orf\\.at/stories/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFOE1IE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>oe1)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFOE3IE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>oe3)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFNOEIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>noe)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFWIEIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>wien)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFBGLIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>burgenland)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFOOEIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>ooe)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFSTMIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>steiermark)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFKTNIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>kaernten)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFSBGIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>salzburg)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFTIRIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>tirol)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFVBGIE(ORFRadioIE):
    _VALID_URL = 'https?://(?P<station>vorarlberg)\\.orf\\.at/player/(?P<date>[0-9]+)/(?P<show>\\w+)'
    _module = 'haruhi_dl.extractor.orf'


class ORFIPTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://iptv\\.orf\\.at/(?:#/)?stories/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.orf'


class OutsideTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?outsidetv\\.com/(?:[^/]+/)*?play/[a-zA-Z0-9]{8}/\\d+/\\d+/(?P<id>[a-zA-Z0-9]{8})'
    _module = 'haruhi_dl.extractor.outsidetv'


class PacktPubBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.packtpub'


class PacktPubIE(PacktPubBaseIE):
    _VALID_URL = 'https?://(?:(?:www\\.)?packtpub\\.com/mapt|subscription\\.packtpub\\.com)/video/[^/]+/(?P<course_id>\\d+)/(?P<chapter_id>[^/]+)/(?P<id>[^/]+)(?:/(?P<display_id>[^/?&#]+))?'
    _module = 'haruhi_dl.extractor.packtpub'


class PacktPubCourseIE(PacktPubBaseIE):
    _VALID_URL = '(?P<url>https?://(?:(?:www\\.)?packtpub\\.com/mapt|subscription\\.packtpub\\.com)/video/[^/]+/(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.packtpub'

    @classmethod
    def suitable(cls, url):
        return False if PacktPubIE.suitable(url) else super(
            PacktPubCourseIE, cls).suitable(url)


class PandoraTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:\n                                (?:www\\.)?pandora\\.tv/view/(?P<user_id>[^/]+)/(?P<id>\\d+)|  # new format\n                                (?:.+?\\.)?channel\\.pandora\\.tv/channel/video\\.ptv\\?|        # old format\n                                m\\.pandora\\.tv/?\\?                                          # mobile\n                            )\n                    '
    _module = 'haruhi_dl.extractor.pandoratv'


class ParliamentLiveUKIE(LazyLoadExtractor):
    _VALID_URL = '(?i)https?://(?:www\\.)?parliamentlive\\.tv/Event/Index/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.parliamentliveuk'


class PatreonIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?patreon\\.com/(?:creation\\?hid=|posts/(?:[\\w-]+-)?)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.patreon'


class PBSIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://\n        (?:\n           # Direct video URL\n           (?:(?:video|www|player)\\.pbs\\.org|video\\.aptv\\.org|video\\.gpb\\.org|video\\.mpbonline\\.org|video\\.wnpt\\.org|video\\.wfsu\\.org|video\\.wsre\\.org|video\\.wtcitv\\.org|video\\.pba\\.org|video\\.alaskapublic\\.org|video\\.azpbs\\.org|portal\\.knme\\.org|video\\.vegaspbs\\.org|watch\\.aetn\\.org|video\\.ket\\.org|video\\.wkno\\.org|video\\.lpb\\.org|videos\\.oeta\\.tv|video\\.optv\\.org|watch\\.wsiu\\.org|video\\.keet\\.org|pbs\\.kixe\\.org|video\\.kpbs\\.org|video\\.kqed\\.org|vids\\.kvie\\.org|video\\.pbssocal\\.org|video\\.valleypbs\\.org|video\\.cptv\\.org|watch\\.knpb\\.org|video\\.soptv\\.org|video\\.rmpbs\\.org|video\\.kenw\\.org|video\\.kued\\.org|video\\.wyomingpbs\\.org|video\\.cpt12\\.org|video\\.kbyueleven\\.org|video\\.thirteen\\.org|video\\.wgbh\\.org|video\\.wgby\\.org|watch\\.njtvonline\\.org|watch\\.wliw\\.org|video\\.mpt\\.tv|watch\\.weta\\.org|video\\.whyy\\.org|video\\.wlvt\\.org|video\\.wvpt\\.net|video\\.whut\\.org|video\\.wedu\\.org|video\\.wgcu\\.org|video\\.wpbt2\\.org|video\\.wucftv\\.org|video\\.wuft\\.org|watch\\.wxel\\.org|video\\.wlrn\\.org|video\\.wusf\\.usf\\.edu|video\\.scetv\\.org|video\\.unctv\\.org|video\\.pbshawaii\\.org|video\\.idahoptv\\.org|video\\.ksps\\.org|watch\\.opb\\.org|watch\\.nwptv\\.org|video\\.will\\.illinois\\.edu|video\\.networkknowledge\\.tv|video\\.wttw\\.com|video\\.iptv\\.org|video\\.ninenet\\.org|video\\.wfwa\\.org|video\\.wfyi\\.org|video\\.mptv\\.org|video\\.wnin\\.org|video\\.wnit\\.org|video\\.wpt\\.org|video\\.wvut\\.org|video\\.weiu\\.net|video\\.wqpt\\.org|video\\.wycc\\.org|video\\.wipb\\.org|video\\.indianapublicmedia\\.org|watch\\.cetconnect\\.org|video\\.thinktv\\.org|video\\.wbgu\\.org|video\\.wgvu\\.org|video\\.netnebraska\\.org|video\\.pioneer\\.org|watch\\.sdpb\\.org|video\\.tpt\\.org|watch\\.ksmq\\.org|watch\\.kpts\\.org|watch\\.ktwu\\.org|watch\\.easttennesseepbs\\.org|video\\.wcte\\.tv|video\\.wljt\\.org|video\\.wosu\\.org|video\\.woub\\.org|video\\.wvpublic\\.org|video\\.wkyupbs\\.org|video\\.kera\\.org|video\\.mpbn\\.net|video\\.mountainlake\\.org|video\\.nhptv\\.org|video\\.vpt\\.org|video\\.witf\\.org|watch\\.wqed\\.org|video\\.wmht\\.org|video\\.deltabroadcasting\\.org|video\\.dptv\\.org|video\\.wcmu\\.org|video\\.wkar\\.org|wnmuvideo\\.nmu\\.edu|video\\.wdse\\.org|video\\.wgte\\.org|video\\.lptv\\.org|video\\.kmos\\.org|watch\\.montanapbs\\.org|video\\.krwg\\.org|video\\.kacvtv\\.org|video\\.kcostv\\.org|video\\.wcny\\.org|video\\.wned\\.org|watch\\.wpbstv\\.org|video\\.wskg\\.org|video\\.wxxi\\.org|video\\.wpsu\\.org|on-demand\\.wvia\\.org|video\\.wtvi\\.org|video\\.westernreservepublicmedia\\.org|video\\.ideastream\\.org|video\\.kcts9\\.org|video\\.basinpbs\\.org|video\\.houstonpbs\\.org|video\\.klrn\\.org|video\\.klru\\.tv|video\\.wtjx\\.org|video\\.ideastations\\.org|video\\.kbtc\\.org)/(?:(?:vir|port)alplayer|video)/(?P<id>[0-9]+)(?:[?/]|$) |\n           # Article with embedded player (or direct video)\n           (?:www\\.)?pbs\\.org/(?:[^/]+/){1,5}(?P<presumptive_id>[^/]+?)(?:\\.html)?/?(?:$|[?\\#]) |\n           # Player\n           (?:video|player)\\.pbs\\.org/(?:widget/)?partnerplayer/(?P<player_id>[^/]+)/\n        )\n    '
    _module = 'haruhi_dl.extractor.pbs'


class PearVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pearvideo\\.com/video_(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.pearvideo'


class PeerTubeSHIE(LazyLoadSelfhostedExtractor):
    _VALID_URL = 'peertube:(?P<host>[^:]+):(?P<id>[\\da-fA-F]{8}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{12})'
    _module = 'haruhi_dl.extractor.peertube'

    _SH_VALID_URL = 'https?://(?P<host>[^/]+)/(?:videos/(?:watch|embed)|api/v\\d/videos)/(?P<id>[\\da-fA-F]{8}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{4}-[\\da-fA-F]{12})'
    _SH_VALID_CONTENT_STRINGS = ('<title>PeerTube<', 'There will be other non JS-based clients to access PeerTube', '>We are sorry but it seems that PeerTube is not compatible with your web browser.<')
    _SH_VALID_CONTENT_REGEXES = None


class PeopleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?people\\.com/people/videos/0,,(?P<id>\\d+),00\\.html'
    _module = 'haruhi_dl.extractor.people'


class PerformGroupIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.performgroup\\.com/eplayer(?:/eplayer\\.html|\\.js)#/?(?P<id>[0-9a-f]{26})\\.(?P<auth_token>[0-9a-z]{26})'
    _module = 'haruhi_dl.extractor.performgroup'


class PeriscopeBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.periscope'


class PeriscopeIE(PeriscopeBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:periscope|pscp)\\.tv/[^/]+/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.periscope'


class PeriscopeUserIE(PeriscopeBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:periscope|pscp)\\.tv/(?P<id>[^/]+)/?$'
    _module = 'haruhi_dl.extractor.periscope'


class PhilharmonieDeParisIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            live\\.philharmoniedeparis\\.fr/(?:[Cc]oncert/|embed(?:app)?/|misc/Playlist\\.ashx\\?id=)|\n                            pad\\.philharmoniedeparis\\.fr/doc/CIMU/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.philharmoniedeparis'


class PhoenixIE(DreiSatIE):
    _VALID_URL = '(?x)https?://(?:www\\.)?phoenix\\.de/content/\n        (?:\n            phoenix/die_sendungen/(?:[^/]+/)?\n        )?\n        (?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.phoenix'


class PhotobucketIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[a-z0-9]+\\.)?photobucket\\.com/.*(([\\?\\&]current=)|_)(?P<id>.*)\\.(?P<ext>(flv)|(mp4))'
    _module = 'haruhi_dl.extractor.photobucket'


class PicartoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/(?P<id>[a-zA-Z0-9]+)(?:/(?P<token>[a-zA-Z0-9]+))?'
    _module = 'haruhi_dl.extractor.picarto'

    @classmethod
    def suitable(cls, url):
        return False if PicartoVodIE.suitable(url) else super(PicartoIE, cls).suitable(url)


class PicartoVodIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/videopopout/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.picarto'


class PikselIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.piksel\\.com/v/(?:refid/[^/]+/prefid/)?(?P<id>[a-z0-9_]+)'
    _module = 'haruhi_dl.extractor.piksel'


class PinkbikeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?pinkbike\\.com/video/|es\\.pinkbike\\.org/i/kvid/kvid-y5\\.swf\\?id=)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.pinkbike'


class PladformIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                out\\.pladform\\.ru/player|\n                                static\\.pladform\\.ru/player\\.swf\n                            )\n                            \\?.*\\bvideoid=|\n                            video\\.pladform\\.ru/catalog/video/videoid/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.pladform'


class PlatziBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.platzi'


class PlatziIE(PlatziBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            platzi\\.com/clases|           # es version\n                            courses\\.platzi\\.com/classes  # en version\n                        )/[^/]+/(?P<id>\\d+)-[^/?\\#&]+\n                    '
    _module = 'haruhi_dl.extractor.platzi'


class PlatziCourseIE(PlatziBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            platzi\\.com/clases|           # es version\n                            courses\\.platzi\\.com/classes  # en version\n                        )/(?P<id>[^/?\\#&]+)\n                    '
    _module = 'haruhi_dl.extractor.platzi'

    @classmethod
    def suitable(cls, url):
        return False if PlatziIE.suitable(url) else super(PlatziCourseIE, cls).suitable(url)


class PlayFMIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?play\\.fm/(?P<slug>(?:[^/]+/)+(?P<id>[^/]+))/?(?:$|[?#])'
    _module = 'haruhi_dl.extractor.playfm'


class PlayPlusTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?playplus\\.(?:com|tv)/VOD/(?P<project_id>[0-9]+)/(?P<id>[0-9a-f]{32})'
    _module = 'haruhi_dl.extractor.playplustv'


class PlaysTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?plays\\.tv/(?:video|embeds)/(?P<id>[0-9a-f]{18})'
    _module = 'haruhi_dl.extractor.plays'


class PlaytvakIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?(?:playtvak|idnes|lidovky|metro)\\.cz/.*\\?(?:c|idvideo)=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.playtvak'


class PlayvidIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?playvid\\.com/watch(\\?v=|/)(?P<id>.+?)(?:#|$)'
    _module = 'haruhi_dl.extractor.playvid'


class PlaywireIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:config|cdn)\\.playwire\\.com(?:/v2)?/(?P<publisher_id>\\d+)/(?:videos/v2|embed|config)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.playwire'


class PluralsightBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.pluralsight'


class PluralsightIE(PluralsightBaseIE):
    _VALID_URL = 'https?://(?:(?:www|app)\\.)?pluralsight\\.com/(?:training/)?player\\?'
    _module = 'haruhi_dl.extractor.pluralsight'


class PluralsightCourseIE(PluralsightBaseIE):
    _VALID_URL = 'https?://(?:(?:www|app)\\.)?pluralsight\\.com/(?:library/)?courses/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.pluralsight'


class PodomaticIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?P<proto>https?)://\n                        (?:\n                            (?P<channel>[^.]+)\\.podomatic\\.com/entry|\n                            (?:www\\.)?podomatic\\.com/podcasts/(?P<channel_2>[^/]+)/episodes\n                        )/\n                        (?P<id>[^/?#&]+)\n                '
    _module = 'haruhi_dl.extractor.podomatic'


class PokemonIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pokemon\\.com/[a-z]{2}(?:.*?play=(?P<id>[a-z0-9]{32})|/(?:[^/]+/)+(?P<display_id>[^/?#&]+))'
    _module = 'haruhi_dl.extractor.pokemon'


class PolskieRadioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?polskieradio(?:24)?\\.pl/\\d+/\\d+/Artykul/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.polskieradio'


class PolskieRadioCategoryIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?polskieradio\\.pl/\\d+(?:,[^/]+)?/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.polskieradio'

    @classmethod
    def suitable(cls, url):
        return False if PolskieRadioIE.suitable(url) else super(PolskieRadioCategoryIE, cls).suitable(url)


class PolskieRadioPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.polskieradio\\.pl/anteny/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.polskieradio'


class PopcorntimesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://popcorntimes\\.tv/[^/]+/m/(?P<id>[^/]+)/(?P<display_id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.popcorntimes'


class PopcornTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[^/]+\\.popcorntv\\.it/guarda/(?P<display_id>[^/]+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.popcorntv'


class Porn91IE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://)(?:www\\.|)91porn\\.com/.+?\\?viewkey=(?P<id>[\\w\\d]+)'
    _module = 'haruhi_dl.extractor.porn91'


class PornComIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[a-zA-Z]+\\.)?porn\\.com/videos/(?:(?P<display_id>[^/]+)-)?(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.porncom'


class PornHdIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pornhd\\.com/(?:[a-z]{2,4}/)?videos/(?P<id>\\d+)(?:/(?P<display_id>.+))?'
    _module = 'haruhi_dl.extractor.pornhd'


class PornHubBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.pornhub'


class PornHubIE(PornHubBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:[^/]+\\.)?(?P<host>pornhub(?:premium)?\\.(?:com|net|org))/(?:(?:view_video\\.php|video/show)\\?viewkey=|embed/)|\n                            (?:www\\.)?thumbzilla\\.com/video/\n                        )\n                        (?P<id>[\\da-z]+)\n                    '
    _module = 'haruhi_dl.extractor.pornhub'


class PornHubPlaylistBaseIE(PornHubBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.pornhub'


class PornHubUserIE(PornHubPlaylistBaseIE):
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?(?P<host>pornhub(?:premium)?\\.(?:com|net|org))/(?:(?:user|channel)s|model|pornstar)/(?P<id>[^/?#&]+))(?:[?#&]|/(?!videos)|$)'
    _module = 'haruhi_dl.extractor.pornhub'


class PornHubPagedPlaylistBaseIE(PornHubPlaylistBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.pornhub'


class PornHubPagedVideoListIE(PornHubPagedPlaylistBaseIE):
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?P<host>pornhub(?:premium)?\\.(?:com|net))/(?P<id>(?:[^/]+/)*[^/?#&]+)'
    _module = 'haruhi_dl.extractor.pornhub'

    @classmethod
    def suitable(cls, url):
        return (False
                if PornHubIE.suitable(url) or PornHubUserIE.suitable(url) or PornHubUserVideosUploadIE.suitable(url)
                else super(PornHubPagedVideoListIE, cls).suitable(url))


class PornHubUserVideosUploadIE(PornHubPagedPlaylistBaseIE):
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?(?P<host>pornhub(?:premium)?\\.(?:com|net|org))/(?:(?:user|channel)s|model|pornstar)/(?P<id>[^/]+)/videos/upload)'
    _module = 'haruhi_dl.extractor.pornhub'


class PornotubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:\\w+\\.)?pornotube\\.com/(?:[^?#]*?)/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.pornotube'


class PornoVoisinesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pornovoisines\\.com/videos/show/(?P<id>\\d+)/(?P<display_id>[^/.]+)'
    _module = 'haruhi_dl.extractor.pornovoisines'


class PornoXOIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pornoxo\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.pornoxo'


class PuhuTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-izle'
    _module = 'haruhi_dl.extractor.puhutv'


class PuhuTVSerieIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-detay'
    _module = 'haruhi_dl.extractor.puhutv'


class PulsEmbedIE(LazyLoadExtractor):
    _VALID_URL = '(?:(?:https?:)?//pulsembed\\.eu/p2em/|pulsembed:)(?P<id>[\\da-zA-Z_-]+)'
    _module = 'haruhi_dl.extractor.pulsembed'


class PulseVideoIE(LazyLoadExtractor):
    _VALID_URL = '(?:pulsevideo|onetmvp):(?P<id>\\d+\\.\\d+)'
    _module = 'haruhi_dl.extractor.pulsembed'


class PressTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?presstv\\.ir/[^/]+/(?P<y>\\d+)/(?P<m>\\d+)/(?P<d>\\d+)/(?P<id>\\d+)/(?P<display_id>[^/]+)?'
    _module = 'haruhi_dl.extractor.presstv'


class ProSiebenSat1BaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.prosiebensat1'


class ProSiebenSat1IE(ProSiebenSat1BaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            (?:beta\\.)?\n                            (?:\n                                prosieben(?:maxx)?|sixx|sat1(?:gold)?|kabeleins(?:doku)?|the-voice-of-germany|advopedia\n                            )\\.(?:de|at|ch)|\n                            ran\\.de|fem\\.com|advopedia\\.de|galileo\\.tv/video\n                        )\n                        /(?P<id>.+)\n                    '
    _module = 'haruhi_dl.extractor.prosiebensat1'


class Puls4IE(ProSiebenSat1BaseIE):
    _VALID_URL = 'https?://(?:www\\.)?puls4\\.com/(?P<id>[^?#&]+)'
    _module = 'haruhi_dl.extractor.puls4'


class PyvideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?pyvideo\\.org/(?P<category>[^/]+)/(?P<id>[^/?#&.]+)'
    _module = 'haruhi_dl.extractor.pyvideo'


class QQMusicIE(LazyLoadExtractor):
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/song/(?P<id>[0-9A-Za-z]+)\\.html'
    _module = 'haruhi_dl.extractor.qqmusic'


class QQPlaylistBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.qqmusic'


class QQMusicSingerIE(QQPlaylistBaseIE):
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/singer/(?P<id>[0-9A-Za-z]+)\\.html'
    _module = 'haruhi_dl.extractor.qqmusic'


class QQMusicAlbumIE(QQPlaylistBaseIE):
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/album/(?P<id>[0-9A-Za-z]+)\\.html'
    _module = 'haruhi_dl.extractor.qqmusic'


class QQMusicToplistIE(QQPlaylistBaseIE):
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/toplist/(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.qqmusic'


class QQMusicPlaylistIE(QQPlaylistBaseIE):
    _VALID_URL = 'https?://y\\.qq\\.com/n/yqq/playlist/(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.qqmusic'


class R7IE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        https?://\n                        (?:\n                            (?:[a-zA-Z]+)\\.r7\\.com(?:/[^/]+)+/idmedia/|\n                            noticias\\.r7\\.com(?:/[^/]+)+/[^/]+-|\n                            player\\.r7\\.com/video/i/\n                        )\n                        (?P<id>[\\da-f]{24})\n                    '
    _module = 'haruhi_dl.extractor.r7'


class R7ArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[a-zA-Z]+)\\.r7\\.com/(?:[^/]+/)+[^/?#&]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.r7'

    @classmethod
    def suitable(cls, url):
        return False if R7IE.suitable(url) else super(R7ArticleIE, cls).suitable(url)


class RadioCanadaIE(LazyLoadExtractor):
    _VALID_URL = '(?:radiocanada:|https?://ici\\.radio-canada\\.ca/widgets/mediaconsole/)(?P<app_code>[^:/]+)[:/](?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.radiocanada'


class RadioCanadaAudioVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://ici\\.radio-canada\\.ca/([^/]+/)*media-(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.radiocanada'


class RadioDeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<id>.+?)\\.(?:radio\\.(?:de|at|fr|pt|es|pl|it)|rad\\.io)'
    _module = 'haruhi_dl.extractor.radiode'


class RadioJavanIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?radiojavan\\.com/videos/video/(?P<id>[^/]+)/?'
    _module = 'haruhi_dl.extractor.radiojavan'


class RadioBremenIE(LazyLoadExtractor):
    _VALID_URL = 'http?://(?:www\\.)?radiobremen\\.de/mediathek/(?:index\\.html)?\\?id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.radiobremen'


class RadioFranceIE(LazyLoadExtractor):
    _VALID_URL = '^https?://maison\\.radiofrance\\.fr/radiovisions/(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.radiofrance'


class RaiBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.rai'


class RaiPlayIE(RaiBaseIE):
    _VALID_URL = '(?P<url>https?://(?:www\\.)?raiplay\\.it/.+?-(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})\\.html)'
    _module = 'haruhi_dl.extractor.rai'


class RaiPlayLiveIE(RaiBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?raiplay\\.it/dirette/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.rai'


class RaiPlayPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?raiplay\\.it/programmi/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.rai'


class RaiIE(RaiBaseIE):
    _VALID_URL = 'https?://[^/]+\\.(?:rai\\.(?:it|tv)|rainews\\.it)/.+?-(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})(?:-.+?)?\\.html'
    _module = 'haruhi_dl.extractor.rai'


class RayWenderlichIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            videos\\.raywenderlich\\.com/courses|\n                            (?:www\\.)?raywenderlich\\.com\n                        )/\n                        (?P<course_id>[^/]+)/lessons/(?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.raywenderlich'


class RayWenderlichCourseIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            videos\\.raywenderlich\\.com/courses|\n                            (?:www\\.)?raywenderlich\\.com\n                        )/\n                        (?P<id>[^/]+)\n                    '
    _module = 'haruhi_dl.extractor.raywenderlich'

    @classmethod
    def suitable(cls, url):
        return False if RayWenderlichIE.suitable(url) else super(
            RayWenderlichCourseIE, cls).suitable(url)


class RBMARadioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:rbmaradio|redbullradio)\\.com/shows/(?P<show_id>[^/]+)/episodes/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.rbmaradio'


class RDSIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rds\\.ca/vid(?:[eé]|%C3%A9)os/(?:[^/]+/)*(?P<id>[^/]+)-\\d+\\.\\d+'
    _module = 'haruhi_dl.extractor.rds'


class RedBullTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?redbull(?:\\.tv|\\.com(?:/[^/]+)?(?:/tv)?)(?:/events/[^/]+)?/(?:videos?|live|(?:film|episode)s)/(?P<id>AP-\\w+)'
    _module = 'haruhi_dl.extractor.redbulltv'


class RedBullEmbedIE(RedBullTVIE):
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/embed/(?P<id>rrn:content:[^:]+:[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}:[a-z]{2}-[A-Z]{2,3})'
    _module = 'haruhi_dl.extractor.redbulltv'


class RedBullTVRrnContentIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/(?P<region>[a-z]{2,3})-(?P<lang>[a-z]{2})/tv/(?:video|live|film)/(?P<id>rrn:content:[^:]+:[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.redbulltv'


class RedBullIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?redbull\\.com/(?P<region>[a-z]{2,3})-(?P<lang>[a-z]{2})/(?P<type>(?:episode|film|(?:(?:recap|trailer)-)?video)s|live)/(?!AP-|rrn:content:)(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.redbulltv'


class RedditIE(LazyLoadExtractor):
    _VALID_URL = 'https?://v\\.redd\\.it/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.reddit'


class RedditRIE(LazyLoadExtractor):
    _VALID_URL = '(?P<url>https?://(?:[^/]+\\.)?reddit\\.com/r/[^/]+/comments/(?P<id>[^/?#&]+))'
    _module = 'haruhi_dl.extractor.reddit'


class RedTubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:\\w+\\.)?redtube\\.com/|embed\\.redtube\\.com/\\?.*?\\bid=)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.redtube'


class RegioTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?regio-tv\\.de/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.regiotv'


class RENTVIE(LazyLoadExtractor):
    _VALID_URL = '(?:rentv:|https?://(?:www\\.)?ren\\.tv/(?:player|video/epizod)/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rentv'


class RENTVArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ren\\.tv/novosti/\\d{4}-\\d{2}-\\d{2}/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.rentv'


class RestudyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|portal)\\.)?restudy\\.dk/video/[^/]+/id/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.restudy'


class ReutersIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?reuters\\.com/.*?\\?.*?videoId=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.reuters'


class ReverbNationIE(LazyLoadExtractor):
    _VALID_URL = '^https?://(?:www\\.)?reverbnation\\.com/.*?/song/(?P<id>\\d+).*?$'
    _module = 'haruhi_dl.extractor.reverbnation'


class RICEIE(LazyLoadExtractor):
    _VALID_URL = 'https?://mediahub\\.rice\\.edu/app/[Pp]ortal/video\\.aspx\\?(?P<query>.+)'
    _module = 'haruhi_dl.extractor.rice'


class RMCDecouverteIE(LazyLoadExtractor):
    _VALID_URL = 'https?://rmcdecouverte\\.bfmtv\\.com/(?:(?:[^/]+/)*program_(?P<id>\\d+)|(?P<live_id>mediaplayer-direct))'
    _module = 'haruhi_dl.extractor.rmcdecouverte'


class RMFonPodcastsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rmfon\\.pl/podcasty/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.rmf'


class RMFonStreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rmfon\\.pl/play,(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rmf'


class RMF24IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rmf24\\.pl(?:/[^/?#,]+)+,nId,(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rmf'


class Ro220IE(LazyLoadExtractor):
    _VALID_URL = '(?x)(?:https?://)?(?:www\\.)?220\\.ro/(?P<category>[^/]+)/(?P<shorttitle>[^/]+)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.ro220'


class RockstarGamesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rockstargames\\.com/videos(?:/video/|#?/?\\?.*\\bvideo=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rockstargames'


class RoosterTeethIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?roosterteeth\\.com/(?:episode|watch)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.roosterteeth'


class RottenTomatoesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rottentomatoes\\.com/m/[^/]+/trailers/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rottentomatoes'


class RoxwelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?roxwel\\.com/player/(?P<filename>.+?)(\\.|\\?|$)'
    _module = 'haruhi_dl.extractor.roxwel'


class RozhlasIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?prehravac\\.rozhlas\\.cz/audio/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.rozhlas'


class RTBFIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?rtbf\\.be/\n        (?:\n            video/[^?]+\\?.*\\bid=|\n            ouftivi/(?:[^/]+/)*[^?]+\\?.*\\bvideoId=|\n            auvio/[^/]+\\?.*\\b(?P<live>l)?id=\n        )(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rtbf'


class RteBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.rte'


class RteIE(RteBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?rte\\.ie/player/[^/]{2,3}/show/[^/]+/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.rte'


class RteRadioIE(RteBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?rte\\.ie/radio/utils/radioplayer/rteradioweb\\.html#!rii=(?:b?[0-9]*)(?:%3A|:|%5F|_)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.rte'


class RtlNlIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?:(?:www|static)\\.)?\n        (?:\n            rtlxl\\.nl/(?:[^\\#]*\\#!|programma)/[^/]+/|\n            rtl\\.nl/(?:(?:system/videoplayer/(?:[^/]+/)+(?:video_)?embed\\.html|embed)\\b.+?\\buuid=|video/)|\n            embed\\.rtl\\.nl/\\#uuid=\n        )\n        (?P<id>[0-9a-f-]+)'
    _module = 'haruhi_dl.extractor.rtlnl'


class RTL2IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtl2\\.de/sendung/[^/]+/(?:video/(?P<vico_id>\\d+)[^/]+/(?P<vivi_id>\\d+)-|folge/)(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.rtl2'


class RTL2YouBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.rtl2'


class RTL2YouIE(RTL2YouBaseIE):
    _VALID_URL = 'http?://you\\.rtl2\\.de/(?:video/\\d+/|youplayer/index\\.html\\?.*?\\bvid=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rtl2'


class RTL2YouSeriesIE(RTL2YouBaseIE):
    _VALID_URL = 'http?://you\\.rtl2\\.de/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rtl2'


class RTPIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtp\\.pt/play/p(?P<program_id>[0-9]+)/(?P<id>[^/?#]+)/?'
    _module = 'haruhi_dl.extractor.rtp'


class RTVEALaCartaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/(m/)?(alacarta/videos|filmoteca)/[^/]+/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rtve'


class RTVELiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/directo/(?P<id>[a-zA-Z0-9-]+)'
    _module = 'haruhi_dl.extractor.rtve'


class RTVEInfantilIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/infantil/serie/(?P<show>[^/]*)/video/(?P<short_title>[^/]*)/(?P<id>[0-9]+)/'
    _module = 'haruhi_dl.extractor.rtve'


class RTVETelevisionIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtve\\.es/television/[^/]+/[^/]+/(?P<id>\\d+).shtml'
    _module = 'haruhi_dl.extractor.rtve'


class RTVNHIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtvnh\\.nl/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.rtvnh'


class RTVSIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?rtvs\\.sk/(?:radio|televizia)/archiv/\\d+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rtvs'


class RUHDIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ruhd\\.ru/play\\.php\\?vid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ruhd'


class RutubeBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.rutube'


class RutubeIE(RutubeBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/(?:video|(?:play/)?embed)/(?P<id>[\\da-z]{32})'
    _module = 'haruhi_dl.extractor.rutube'

    @classmethod
    def suitable(cls, url):
        return False if RutubePlaylistIE.suitable(url) else super(RutubeIE, cls).suitable(url)


class RutubePlaylistBaseIE(RutubeBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.rutube'


class RutubeChannelIE(RutubePlaylistBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/tags/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rutube'


class RutubeEmbedIE(RutubeBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/(?:video|play)/embed/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.rutube'


class RutubeMovieIE(RutubePlaylistBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/metainfo/tv/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rutube'


class RutubePersonIE(RutubePlaylistBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/video/person/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rutube'


class RutubePlaylistIE(RutubePlaylistBaseIE):
    _VALID_URL = 'https?://rutube\\.ru/(?:video|(?:play/)?embed)/[\\da-z]{32}/\\?.*?\\bpl_id=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.rutube'

    @classmethod
    def suitable(cls, url):
        if not super(RutubePlaylistIE, cls).suitable(url):
            return False
        params = compat_parse_qs(compat_urllib_parse_urlparse(url).query)
        return params.get('pl_type', [None])[0] and int_or_none(params.get('pl_id', [None])[0])


class RUTVIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:test)?player\\.(?:rutv\\.ru|vgtrk\\.com)/\n                        (?P<path>\n                            flash\\d+v/container\\.swf\\?id=|\n                            iframe/(?P<type>swf|video|live)/id/|\n                            index/iframe/cast_id/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.rutv'


class RuutuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:ruutu|supla)\\.fi/(?:video|supla)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ruutu'


class RuvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ruv\\.is/(?:sarpurinn/[^/]+|node)/(?P<id>[^/]+(?:/\\d+)?)'
    _module = 'haruhi_dl.extractor.ruv'


class SafariBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.safari'


class SafariIE(SafariBaseIE):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/\n                            (?:\n                                library/view/[^/]+/(?P<course_id>[^/]+)/(?P<part>[^/?\\#&]+)\\.html|\n                                videos/[^/]+/[^/]+/(?P<reference_id>[^-]+-[^/?\\#&]+)\n                            )\n                    '
    _module = 'haruhi_dl.extractor.safari'


class SafariApiIE(SafariBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/api/v1/book/(?P<course_id>[^/]+)/chapter(?:-content)?/(?P<part>[^/?#&]+)\\.html'
    _module = 'haruhi_dl.extractor.safari'


class SafariCourseIE(SafariBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?(?:safaribooksonline|(?:learning\\.)?oreilly)\\.com/\n                            (?:\n                                library/view/[^/]+|\n                                api/v1/book|\n                                videos/[^/]+\n                            )|\n                            techbus\\.safaribooksonline\\.com\n                        )\n                        /(?P<id>[^/]+)\n                    '
    _module = 'haruhi_dl.extractor.safari'

    @classmethod
    def suitable(cls, url):
        return (False if SafariIE.suitable(url) or SafariApiIE.suitable(url)
                else super(SafariCourseIE, cls).suitable(url))


class SapoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:v2|www)\\.)?videos\\.sapo\\.(?:pt|cv|ao|mz|tl)/(?P<id>[\\da-zA-Z]{20})'
    _module = 'haruhi_dl.extractor.sapo'


class SaveFromIE(LazyLoadExtractor):
    _VALID_URL = 'https?://[^.]+\\.savefrom\\.net/\\#url=(?P<url>.*)$'
    _module = 'haruhi_dl.extractor.savefrom'


class SBSIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?sbs\\.com\\.au/(?:ondemand|news)/video/(?:single/)?(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sbs'


class ScreencastIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?screencast\\.com/t/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.screencast'


class ScreencastOMaticIE(LazyLoadExtractor):
    _VALID_URL = 'https?://screencast-o-matic\\.com/watch/(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.screencastomatic'


class AWSIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.aws'


class ScrippsNetworksWatchIE(AWSIE):
    _VALID_URL = '(?x)\n                    https?://\n                        watch\\.\n                        (?P<site>geniuskitchen)\\.com/\n                        (?:\n                            player\\.[A-Z0-9]+\\.html\\#|\n                            show/(?:[^/]+/){2}|\n                            player/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.scrippsnetworks'


class ScrippsNetworksIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>cookingchanneltv|discovery|(?:diy|food)network|hgtv|travelchannel)\\.com/videos/[0-9a-z-]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.scrippsnetworks'


class SCTEBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.scte'


class SCTEIE(SCTEBaseIE):
    _VALID_URL = 'https?://learning\\.scte\\.org/mod/scorm/view\\.php?.*?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.scte'


class SCTECourseIE(SCTEBaseIE):
    _VALID_URL = 'https?://learning\\.scte\\.org/(?:mod/sub)?course/view\\.php?.*?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.scte'


class SeekerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?seeker\\.com/(?P<display_id>.*)-(?P<article_id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.seeker'


class SenateISVPIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?senate\\.gov/isvp/?\\?(?P<qs>.+)'
    _module = 'haruhi_dl.extractor.senateisvp'


class SendtoNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://embed\\.sendtonews\\.com/player2/embedplayer\\.php\\?.*\\bSC=(?P<id>[0-9A-Za-z-]+)'
    _module = 'haruhi_dl.extractor.sendtonews'


class ServusIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            servus\\.com/(?:(?:at|de)/p/[^/]+|tv/videos)|\n                            servustv\\.com/videos\n                        )\n                        /(?P<id>[aA]{2}-\\w+|\\d+-\\d+)\n                    '
    _module = 'haruhi_dl.extractor.servus'


class SevenPlusIE(BrightcoveNewIE):
    _VALID_URL = 'https?://(?:www\\.)?7plus\\.com\\.au/(?P<path>[^?]+\\?.*?\\bepisode-id=(?P<id>[^&#]+))'
    _module = 'haruhi_dl.extractor.sevenplus'


class SexuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?sexu\\.com/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.sexu'


class SeznamZpravyIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?seznamzpravy\\.cz/iframe/player\\?.*\\bsrc='
    _module = 'haruhi_dl.extractor.seznamzpravy'


class SeznamZpravyArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:seznam\\.cz/zpravy|seznamzpravy\\.cz)/clanek/(?:[^/?#&]+)-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.seznamzpravy'


class ShahidBaseIE(AWSIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.shahid'


class ShahidIE(ShahidBaseIE):
    _VALID_URL = 'https?://shahid\\.mbc\\.net/ar/(?:serie|show|movie)s/[^/]+/(?P<type>episode|clip|movie)-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.shahid'


class ShahidShowIE(ShahidBaseIE):
    _VALID_URL = 'https?://shahid\\.mbc\\.net/ar/(?:show|serie)s/[^/]+/(?:show|series)-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.shahid'


class SharedBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.shared'


class SharedIE(SharedBaseIE):
    _VALID_URL = 'https?://shared\\.sx/(?P<id>[\\da-z]{10})'
    _module = 'haruhi_dl.extractor.shared'


class VivoIE(SharedBaseIE):
    _VALID_URL = 'https?://vivo\\.sx/(?P<id>[\\da-z]{10})'
    _module = 'haruhi_dl.extractor.shared'


class ShowRoomLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?showroom-live\\.com/(?!onlive|timetable|event|campaign|news|ranking|room)(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.showroomlive'


class SinaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:.*?\\.)?video\\.sina\\.com\\.cn/\n                        (?:\n                            (?:view/|.*\\#)(?P<video_id>\\d+)|\n                            .+?/(?P<pseudo_id>[^/?#]+)(?:\\.s?html)|\n                            # This is used by external sites like Weibo\n                            api/sinawebApi/outplay.php/(?P<token>.+?)\\.swf\n                        )\n                  '
    _module = 'haruhi_dl.extractor.sina'


class SixPlayIE(LazyLoadExtractor):
    _VALID_URL = '(?:6play:|https?://(?:www\\.)?(?P<domain>6play\\.fr|rtlplay\\.be|play\\.rtl\\.hr|rtlmost\\.hu)/.+?-c_)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sixplay'


class SkylineWebcamsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?skylinewebcams\\.com/[^/]+/webcam/(?:[^/]+/)+(?P<id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.skylinewebcams'


class SkyNewsArabiaBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.skynewsarabia'


class SkyNewsArabiaIE(SkyNewsArabiaBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?skynewsarabia\\.com/web/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.skynewsarabia'


class SkyNewsArabiaArticleIE(SkyNewsArabiaBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?skynewsarabia\\.com/web/article/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.skynewsarabia'


class SkyBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.sky'


class SkyNewsIE(SkyBaseIE):
    _VALID_URL = 'https?://news\\.sky\\.com/video/[0-9a-z-]+-(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sky'


class SkySportsIE(SkyBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?skysports\\.com/watch/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sky'


class SlideshareIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?slideshare\\.net/[^/]+?/(?P<title>.+?)($|\\?)'
    _module = 'haruhi_dl.extractor.slideshare'


class SlidesLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://slideslive\\.com/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.slideslive'


class SlutloadIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:\\w+\\.)?slutload\\.com/(?:video/[^/]+|embed_player|watch)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.slutload'


class SmotriIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:smotri\\.com/video/view/\\?id=|pics\\.smotri\\.com/(?:player|scrubber_custom8)\\.swf\\?file=)(?P<id>v(?P<realvideoid>[0-9]+)[a-z0-9]{4})'
    _module = 'haruhi_dl.extractor.smotri'


class SmotriCommunityIE(LazyLoadExtractor):
    _VALID_URL = "https?://(?:www\\.)?smotri\\.com/community/video/(?P<id>[0-9A-Za-z_\\'-]+)"
    _module = 'haruhi_dl.extractor.smotri'


class SmotriUserIE(LazyLoadExtractor):
    _VALID_URL = "https?://(?:www\\.)?smotri\\.com/user/(?P<id>[0-9A-Za-z_\\'-]+)"
    _module = 'haruhi_dl.extractor.smotri'


class SmotriBroadcastIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>smotri\\.com/live/(?P<id>[^/]+))/?.*'
    _module = 'haruhi_dl.extractor.smotri'


class SnotrIE(LazyLoadExtractor):
    _VALID_URL = 'http?://(?:www\\.)?snotr\\.com/video/(?P<id>\\d+)/([\\w]+)'
    _module = 'haruhi_dl.extractor.snotr'


class SohuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<mytv>my\\.)?tv\\.sohu\\.com/.+?/(?(mytv)|n)(?P<id>\\d+)\\.shtml.*?'
    _module = 'haruhi_dl.extractor.sohu'


class SonyLIVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?sonyliv\\.com/details/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.sonyliv'


class SoundcloudEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:w|player|p)\\.soundcloud\\.com/player/?.*?\\burl=(?P<id>.+)'
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudIE(LazyLoadExtractor):
    _VALID_URL = '(?x)^(?:https?://)?\n                    (?:(?:(?:www\\.|m\\.)?soundcloud\\.com/\n                            (?!stations/track)\n                            (?P<uploader>[\\w\\d-]+)/\n                            (?!(?:tracks|albums|sets(?:/.+?)?|reposts|likes|spotlight)/?(?:$|[?#]))\n                            (?P<title>[\\w\\d-]+)/?\n                            (?P<token>[^?]+?)?(?:[?].*)?$)\n                       |(?:api(?:-v2)?\\.soundcloud\\.com/tracks/(?P<track_id>\\d+)\n                          (?:/?\\?secret_token=(?P<secret_token>[^&]+))?)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudPlaylistBaseIE(SoundcloudIE):
    _VALID_URL = '(?x)^(?:https?://)?\n                    (?:(?:(?:www\\.|m\\.)?soundcloud\\.com/\n                            (?!stations/track)\n                            (?P<uploader>[\\w\\d-]+)/\n                            (?!(?:tracks|albums|sets(?:/.+?)?|reposts|likes|spotlight)/?(?:$|[?#]))\n                            (?P<title>[\\w\\d-]+)/?\n                            (?P<token>[^?]+?)?(?:[?].*)?$)\n                       |(?:api(?:-v2)?\\.soundcloud\\.com/tracks/(?P<track_id>\\d+)\n                          (?:/?\\?secret_token=(?P<secret_token>[^&]+))?)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudSetIE(SoundcloudPlaylistBaseIE):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?soundcloud\\.com/(?P<uploader>[\\w\\d-]+)/sets/(?P<slug_title>[\\w\\d-]+)(?:/(?P<token>[^?/]+))?'
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudPagedPlaylistBaseIE(SoundcloudIE):
    _VALID_URL = '(?x)^(?:https?://)?\n                    (?:(?:(?:www\\.|m\\.)?soundcloud\\.com/\n                            (?!stations/track)\n                            (?P<uploader>[\\w\\d-]+)/\n                            (?!(?:tracks|albums|sets(?:/.+?)?|reposts|likes|spotlight)/?(?:$|[?#]))\n                            (?P<title>[\\w\\d-]+)/?\n                            (?P<token>[^?]+?)?(?:[?].*)?$)\n                       |(?:api(?:-v2)?\\.soundcloud\\.com/tracks/(?P<track_id>\\d+)\n                          (?:/?\\?secret_token=(?P<secret_token>[^&]+))?)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudUserIE(SoundcloudPagedPlaylistBaseIE):
    _VALID_URL = '(?x)\n                        https?://\n                            (?:(?:www|m)\\.)?soundcloud\\.com/\n                            (?P<user>[^/]+)\n                            (?:/\n                                (?P<rsrc>tracks|albums|sets|reposts|likes|spotlight)\n                            )?\n                            /?(?:[?#].*)?$\n                    '
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudTrackStationIE(SoundcloudPagedPlaylistBaseIE):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?soundcloud\\.com/stations/track/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudPlaylistIE(SoundcloudPlaylistBaseIE):
    _VALID_URL = 'https?://api(?:-v2)?\\.soundcloud\\.com/playlists/(?P<id>[0-9]+)(?:/?\\?secret_token=(?P<token>[^&]+?))?$'
    _module = 'haruhi_dl.extractor.soundcloud'


class SoundcloudSearchIE(LazyLoadSearchExtractor, SoundcloudIE):
    _VALID_URL = '(?x)^(?:https?://)?\n                    (?:(?:(?:www\\.|m\\.)?soundcloud\\.com/\n                            (?!stations/track)\n                            (?P<uploader>[\\w\\d-]+)/\n                            (?!(?:tracks|albums|sets(?:/.+?)?|reposts|likes|spotlight)/?(?:$|[?#]))\n                            (?P<title>[\\w\\d-]+)/?\n                            (?P<token>[^?]+?)?(?:[?].*)?$)\n                       |(?:api(?:-v2)?\\.soundcloud\\.com/tracks/(?P<track_id>\\d+)\n                          (?:/?\\?secret_token=(?P<secret_token>[^&]+))?)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.soundcloud'

    @classmethod
    def suitable(cls, url):
        return re.match(cls._make_valid_url(), url) is not None

    @classmethod
    def _make_valid_url(cls):
        return 'scsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class SoundgasmIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?soundgasm\\.net/u/(?P<user>[0-9a-zA-Z_-]+)/(?P<display_id>[0-9a-zA-Z_-]+)'
    _module = 'haruhi_dl.extractor.soundgasm'


class SoundgasmProfileIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?soundgasm\\.net/u/(?P<id>[^/]+)/?(?:\\#.*)?$'
    _module = 'haruhi_dl.extractor.soundgasm'


class SouthParkIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.cc\\.com/(?:clips|(?:full-)?episodes|collections)/(?P<id>.+?)(\\?|#|$))'
    _module = 'haruhi_dl.extractor.southpark'


class SouthParkDeIE(SouthParkIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.de/(?:clips|alle-episoden|collections)/(?P<id>.+?)(\\?|#|$))'
    _module = 'haruhi_dl.extractor.southpark'


class SouthParkDkIE(SouthParkIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southparkstudios\\.(?:dk|nu)/(?:clips|full-episodes|collections)/(?P<id>.+?)(\\?|#|$))'
    _module = 'haruhi_dl.extractor.southpark'


class SouthParkEsIE(SouthParkIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.cc\\.com/episodios-en-espanol/(?P<id>.+?)(\\?|#|$))'
    _module = 'haruhi_dl.extractor.southpark'


class SouthParkNlIE(SouthParkIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<url>southpark\\.nl/(?:clips|(?:full-)?episodes|collections)/(?P<id>.+?)(\\?|#|$))'
    _module = 'haruhi_dl.extractor.southpark'


class SpankBangIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?spankbang\\.com/(?P<id>[\\da-z]+)/(?:video|play|embed)\\b'
    _module = 'haruhi_dl.extractor.spankbang'


class SpankBangPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?spankbang\\.com/(?P<id>[\\da-z]+)/playlist/[^/]+'
    _module = 'haruhi_dl.extractor.spankbang'


class SpankwireIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?spankwire\\.com/\n                        (?:\n                            [^/]+/video|\n                            EmbedPlayer\\.aspx/?\\?.*?\\bArticleId=\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.spankwire'


class SpiegelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?spiegel\\.de/video/[^/]*-(?P<id>[0-9]+)(?:-embed|-iframe)?(?:\\.html)?(?:#.*)?$'
    _module = 'haruhi_dl.extractor.spiegel'


class SpiegelArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?spiegel\\.de/(?!video/)[^?#]*?-(?P<id>[0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.spiegel'


class SpiegeltvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?spiegel\\.tv/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.spiegeltv'


class BellatorIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bellator\\.com/[^/]+/[\\da-z]{6}(?:[/?#&]|$)'
    _module = 'haruhi_dl.extractor.spike'


class ParamountNetworkIE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?paramountnetwork\\.com/[^/]+/[\\da-z]{6}(?:[/?#&]|$)'
    _module = 'haruhi_dl.extractor.spike'


class StitcherIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?stitcher\\.com/podcast/(?:[^/]+/)+e/(?:(?P<display_id>[^/#?&]+?)-)?(?P<id>\\d+)(?:[/#?&]|$)'
    _module = 'haruhi_dl.extractor.stitcher'


class Sport5IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www|vod)?\\.sport5\\.co\\.il/.*\\b(?:Vi|docID)=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.sport5'


class SportBoxIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:news\\.sportbox|matchtv)\\.ru/vdl/player(?:/[^/]+/|\\?.*?\\bn?id=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.sportbox'


class SportDeutschlandIE(LazyLoadExtractor):
    _VALID_URL = 'https?://sportdeutschland\\.tv/(?P<sport>[^/?#]+)/(?P<id>[^?#/]+)(?:$|[?#])'
    _module = 'haruhi_dl.extractor.sportdeutschland'


class SpringboardPlatformIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        cms\\.springboardplatform\\.com/\n                        (?:\n                            (?:previews|embed_iframe)/(?P<index>\\d+)/video/(?P<id>\\d+)|\n                            xml_feeds_advanced/index/(?P<index_2>\\d+)/rss3/(?P<id_2>\\d+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.springboardplatform'


class SproutIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?sproutonline\\.com/watch/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.sprout'


class SRGSSRIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://tp\\.srgssr\\.ch/p(?:/[^/]+)+\\?urn=urn|srgssr):(?P<bu>srf|rts|rsi|rtr|swi):(?:[^:]+:)?(?P<type>video|audio):(?P<id>[0-9a-f\\-]{36}|\\d+)'
    _module = 'haruhi_dl.extractor.srgssr'


class RTSIE(SRGSSRIE):
    _VALID_URL = 'rts:(?P<rts_id>\\d+)|https?://(?:.+?\\.)?rts\\.ch/(?:[^/]+/){2,}(?P<id>[0-9]+)-(?P<display_id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.rts'


class SRGSSRPlayIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|play)\\.)?\n                        (?P<bu>srf|rts|rsi|rtr|swissinfo)\\.ch/play/(?:tv|radio)/\n                        (?:\n                            [^/]+/(?P<type>video|audio)/[^?]+|\n                            popup(?P<type_2>video|audio)player\n                        )\n                        \\?.*?\\b(?:id=|urn=urn:[^:]+:video:)(?P<id>[0-9a-f\\-]{36}|\\d+)\n                    '
    _module = 'haruhi_dl.extractor.srgssr'


class SRMediathekIE(ARDMediathekBaseIE):
    _VALID_URL = 'https?://sr-mediathek(?:\\.sr-online)?\\.de/index\\.php\\?.*?&id=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.srmediathek'


class StanfordOpenClassroomIE(LazyLoadExtractor):
    _VALID_URL = 'https?://openclassroom\\.stanford\\.edu(?P<path>/?|(/MainFolder/(?:HomePage|CoursePage|VideoPage)\\.php([?]course=(?P<course>[^&]+)(&video=(?P<video>[^&]+))?(&.*)?)?))$'
    _module = 'haruhi_dl.extractor.stanfordoc'


class SteamIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://store\\.steampowered\\.com/\n            (agecheck/)?\n            (?P<urltype>video|app)/ #If the page is only for videos or for a game\n            (?P<gameID>\\d+)/?\n            (?P<videoID>\\d*)(?P<extra>\\??) # For urltype == video we sometimes get the videoID\n        |\n        https?://(?:www\\.)?steamcommunity\\.com/sharedfiles/filedetails/\\?id=(?P<fileID>[0-9]+)\n    '
    _module = 'haruhi_dl.extractor.steam'


class StreamableIE(LazyLoadExtractor):
    _VALID_URL = 'https?://streamable\\.com/(?:[es]/)?(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.streamable'


class StreamcloudIE(LazyLoadExtractor):
    _VALID_URL = 'https?://streamcloud\\.eu/(?P<id>[a-zA-Z0-9_-]+)(?:/(?P<fname>[^#?]*)\\.html)?'
    _module = 'haruhi_dl.extractor.streamcloud'


class StreamCZIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?stream\\.cz/.+/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.streamcz'


class StreetVoiceIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?streetvoice\\.com/[^/]+/songs/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.streetvoice'


class StretchInternetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://portal\\.stretchinternet\\.com/[^/]+/(?:portal|full)\\.htm\\?.*?\\beventId=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.stretchinternet'


class STVPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.stv\\.tv/(?P<type>episode|video)/(?P<id>[a-z0-9]{4})'
    _module = 'haruhi_dl.extractor.stv'


class SunPornoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?sunporno\\.com/videos|embeds\\.sunporno\\.com/embed)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.sunporno'


class SverigesRadioBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.sverigesradio'


class SverigesRadioEpisodeIE(SverigesRadioBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?sverigesradio\\.se/(?:sida/)?avsnitt/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sverigesradio'


class SverigesRadioPublicationIE(SverigesRadioBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?sverigesradio\\.se/sida/(?:artikel|gruppsida)\\.aspx\\?.*?\\bartikel=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sverigesradio'


class SVTBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.svt'


class SVTIE(SVTBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?svt\\.se/wd\\?(?:.*?&)?widgetId=(?P<widget_id>\\d+)&.*?\\barticleId=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.svt'


class SVTPageIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?svt\\.se/(?P<path>(?:[^/]+/)*(?P<id>[^/?&#]+))'
    _module = 'haruhi_dl.extractor.svt'

    @classmethod
    def suitable(cls, url):
        return False if SVTIE.suitable(url) else super(SVTPageIE, cls).suitable(url)


class SVTPlayBaseIE(SVTBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.svt'


class SVTPlayIE(SVTPlayBaseIE):
    _VALID_URL = '(?x)\n                    (?:\n                        svt:(?P<svt_id>[^/?#&]+)|\n                        https?://(?:www\\.)?(?:svtplay|oppetarkiv)\\.se/(?:video|klipp|kanaler)/(?P<id>[^/?#&]+)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.svt'


class SVTSeriesIE(SVTPlayBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?svtplay\\.se/(?P<id>[^/?&#]+)(?:.+?\\btab=(?P<season_slug>[^&#]+))?'
    _module = 'haruhi_dl.extractor.svt'

    @classmethod
    def suitable(cls, url):
        return False if SVTIE.suitable(url) or SVTPlayIE.suitable(url) else super(SVTSeriesIE, cls).suitable(url)


class SWRMediathekIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?swrmediathek\\.de/(?:content/)?player\\.htm\\?show=(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.swrmediathek'


class SyfyIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?syfy\\.com/(?:[^/]+/)?videos/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.syfy'


class SztvHuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?sztv\\.hu|www\\.tvszombathely\\.hu)/(?:[^/]+)/.+-(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.sztvhu'


class TagesschauPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tagesschau\\.de/multimedia/(?P<kind>audio|video)/(?P=kind)-(?P<id>\\d+)~player(?:_[^/?#&]+)?\\.html'
    _module = 'haruhi_dl.extractor.tagesschau'


class TagesschauIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tagesschau\\.de/(?P<path>[^/]+/(?:[^/]+/)*?(?P<id>[^/#?]+?(?:-?[0-9]+)?))(?:~_?[^/#?]+?)?\\.html'
    _module = 'haruhi_dl.extractor.tagesschau'

    @classmethod
    def suitable(cls, url):
        return False if TagesschauPlayerIE.suitable(url) else super(TagesschauIE, cls).suitable(url)


class TassIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:tass\\.ru|itar-tass\\.com)/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tass'


class TastyTradeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tastytrade\\.com/tt/shows/[^/]+/episodes/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.tastytrade'


class TBSIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>tbs|tntdrama)\\.com(?P<path>/(?:movies|shows/[^/]+/(?:clips|season-\\d+/episode-\\d+))/(?P<id>[^/?#]+))'
    _module = 'haruhi_dl.extractor.tbs'


class TDSLifewayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tds\\.lifeway\\.com/v1/trainingdeliverysystem/courses/(?P<id>\\d+)/index\\.html'
    _module = 'haruhi_dl.extractor.tdslifeway'


class TeachableBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.teachable'


class TeachableIE(TeachableBaseIE):
    _VALID_URL = '(?x)\n                    (?:\n                        teachable:https?://(?P<site_t>[^/]+)|\n                        https?://(?:www\\.)?(?P<site>v1\\.upskillcourses\\.com|gns3\\.teachable\\.com|academyhacker\\.com|stackskills\\.com|market\\.saleshacker\\.com|learnability\\.org|edurila\\.com|courses\\.workitdaily\\.com)\n                    )\n                    /courses/[^/]+/lectures/(?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.teachable'


class TeachableCourseIE(TeachableBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            teachable:https?://(?P<site_t>[^/]+)|\n                            https?://(?:www\\.)?(?P<site>v1\\.upskillcourses\\.com|gns3\\.teachable\\.com|academyhacker\\.com|stackskills\\.com|market\\.saleshacker\\.com|learnability\\.org|edurila\\.com|courses\\.workitdaily\\.com)\n                        )\n                        /(?:courses|p)/(?:enrolled/)?(?P<id>[^/?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.teachable'

    @classmethod
    def suitable(cls, url):
        return False if TeachableIE.suitable(url) else super(
            TeachableCourseIE, cls).suitable(url)


class TeacherTubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?teachertube\\.com/(viewVideo\\.php\\?video_id=|music\\.php\\?music_id=|video/(?:[\\da-z-]+-)?|audio/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.teachertube'


class TeacherTubeUserIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?teachertube\\.com/(user/profile|collection)/(?P<user>[0-9a-zA-Z]+)/?'
    _module = 'haruhi_dl.extractor.teachertube'


class TeachingChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?teachingchannel\\.org/videos?/(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.teachingchannel'


class TeamcocoIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:\\w+\\.)?teamcoco\\.com/(?P<id>([^/]+/)*[^/?#]+)'
    _module = 'haruhi_dl.extractor.teamcoco'


class TeamTreeHouseIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?teamtreehouse\\.com/library/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.teamtreehouse'


class TechTalksIE(LazyLoadExtractor):
    _VALID_URL = 'https?://techtalks\\.tv/talks/(?:[^/]+/)?(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.techtalks'


class TEDIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        (?P<proto>https?://)\n        (?P<type>www|embed(?:-ssl)?)(?P<urlmain>\\.ted\\.com/\n        (\n            (?P<type_playlist>playlists(?:/(?P<playlist_id>\\d+))?) # We have a playlist\n            |\n            ((?P<type_talk>talks)) # We have a simple talk\n            |\n            (?P<type_watch>watch)/[^/]+/[^/]+\n        )\n        (/lang/(.*?))? # The url may contain the language\n        /(?P<name>[\\w-]+) # Here goes the name and then ".html"\n        .*)$\n        '
    _module = 'haruhi_dl.extractor.ted'


class Tele5IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tele5\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.tele5'


class Tele13IE(LazyLoadExtractor):
    _VALID_URL = '^https?://(?:www\\.)?t13\\.cl/videos(?:/[^/]+)+/(?P<id>[\\w-]+)'
    _module = 'haruhi_dl.extractor.tele13'


class TeleBruxellesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:telebruxelles|bx1)\\.be/(?:[^/]+/)*(?P<id>[^/#?]+)'
    _module = 'haruhi_dl.extractor.telebruxelles'


class TelecincoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:telecinco\\.es|cuatro\\.com|mediaset\\.es)/(?:[^/]+/)+(?P<id>.+?)\\.html'
    _module = 'haruhi_dl.extractor.telecinco'


class TelegraafIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?telegraaf\\.nl/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.telegraaf'


class TeleMBIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?telemb\\.be/(?P<display_id>.+?)_d_(?P<id>\\d+)\\.html'
    _module = 'haruhi_dl.extractor.telemb'


class TeleQuebecBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.telequebec'


class TeleQuebecIE(TeleQuebecBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            zonevideo\\.telequebec\\.tv/media|\n                            coucou\\.telequebec\\.tv/videos\n                        )/(?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.telequebec'


class TeleQuebecSquatIE(LazyLoadExtractor):
    _VALID_URL = 'https://squat\\.telequebec\\.tv/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.telequebec'


class TeleQuebecEmissionIE(TeleQuebecBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            [^/]+\\.telequebec\\.tv/emissions/|\n                            (?:www\\.)?telequebec\\.tv/\n                        )\n                        (?P<id>[^?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.telequebec'


class TeleQuebecLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://zonevideo\\.telequebec\\.tv/(?P<id>endirect)'
    _module = 'haruhi_dl.extractor.telequebec'


class TeleTaskIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tele-task\\.de/archive/video/html5/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.teletask'


class TelewebionIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?telewebion\\.com/#!/episode/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.telewebion'


class TennisTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tennistv\\.com/videos/(?P<id>[-a-z0-9]+)'
    _module = 'haruhi_dl.extractor.tennistv'


class TenPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?10play\\.com\\.au/(?:[^/]+/)+(?P<id>tpv\\d{6}[a-z]{5})'
    _module = 'haruhi_dl.extractor.tenplay'


class TestURLIE(LazyLoadExtractor):
    _VALID_URL = 'test(?:url)?:(?P<id>(?P<extractor>.+?)(?:_(?P<num>[0-9]+))?)$'
    _module = 'haruhi_dl.extractor.testurl'


class TF1IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:videos|www|lci)\\.tf1|(?:www\\.)?(?:tfou|ushuaiatv|histoire|tvbreizh))\\.fr/(?:[^/]+/)*(?P<id>[^/?#.]+)'
    _module = 'haruhi_dl.extractor.tf1'


class TFOIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tfo\\.org/(?:en|fr)/(?:[^/]+/){2}(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tfo'


class TheInterceptIE(LazyLoadExtractor):
    _VALID_URL = 'https?://theintercept\\.com/fieldofvision/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.theintercept'


class ThePlatformIE(ThePlatformBaseIE, AdobePassIE):
    _VALID_URL = '(?x)\n        (?:https?://(?:link|player)\\.theplatform\\.com/[sp]/(?P<provider_id>[^/]+)/\n           (?:(?:(?:[^/]+/)+select/)?(?P<media>media/(?:guid/\\d+/)?)?|(?P<config>(?:[^/\\?]+/(?:swf|config)|onsite)/select/))?\n         |theplatform:)(?P<id>[^/\\?&]+)'
    _module = 'haruhi_dl.extractor.theplatform'


class AENetworksBaseIE(ThePlatformIE):
    _VALID_URL = '(?x)\n        (?:https?://(?:link|player)\\.theplatform\\.com/[sp]/(?P<provider_id>[^/]+)/\n           (?:(?:(?:[^/]+/)+select/)?(?P<media>media/(?:guid/\\d+/)?)?|(?P<config>(?:[^/\\?]+/(?:swf|config)|onsite)/select/))?\n         |theplatform:)(?P<id>[^/\\?&]+)'
    _module = 'haruhi_dl.extractor.aenetworks'


class AENetworksIE(AENetworksBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?P<domain>\n                            (?:history(?:vault)?|aetv|mylifetime|lifetimemovieclub)\\.com|\n                            fyi\\.tv\n                        )/\n                        (?:\n                            shows/(?P<show_path>[^/]+(?:/[^/]+){0,2})|\n                            movies/(?P<movie_display_id>[^/]+)(?:/full-movie)?|\n                            specials/(?P<special_display_id>[^/]+)/(?:full-special|preview-)|\n                            collections/[^/]+/(?P<collection_display_id>[^/]+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.aenetworks'


class HistoryTopicIE(AENetworksBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?history\\.com/topics/[^/]+/(?P<id>[\\w+-]+?)-video'
    _module = 'haruhi_dl.extractor.aenetworks'


class AMCNetworksIE(ThePlatformIE):
    _VALID_URL = 'https?://(?:www\\.)?(?:amc|bbcamerica|ifc|(?:we|sundance)tv)\\.com/(?:movies|shows(?:/[^/]+)+)/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.amcnetworks'


class NBCNewsIE(ThePlatformIE):
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:nbcnews|today|msnbc)\\.com/([^/]+/)*(?:.*-)?(?P<id>[^/?]+)'
    _module = 'haruhi_dl.extractor.nbc'


class ThePlatformFeedIE(ThePlatformBaseIE):
    _VALID_URL = 'https?://feed\\.theplatform\\.com/f/(?P<provider_id>[^/]+)/(?P<feed_id>[^?/]+)\\?(?:[^&]+&)*(?P<filter>by(?:Gui|I)d=(?P<id>[^&]+))'
    _module = 'haruhi_dl.extractor.theplatform'


class CBSBaseIE(ThePlatformFeedIE):
    _VALID_URL = 'https?://feed\\.theplatform\\.com/f/(?P<provider_id>[^/]+)/(?P<feed_id>[^?/]+)\\?(?:[^&]+&)*(?P<filter>by(?:Gui|I)d=(?P<id>[^&]+))'
    _module = 'haruhi_dl.extractor.cbs'


class CBSIE(CBSBaseIE):
    _VALID_URL = '(?:cbs:|https?://(?:www\\.)?(?:cbs\\.com/shows/[^/]+/video|colbertlateshow\\.com/(?:video|podcasts))/)(?P<id>[\\w-]+)'
    _module = 'haruhi_dl.extractor.cbs'


class CBSInteractiveIE(CBSIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>cnet|zdnet)\\.com/(?:videos|video(?:/share)?)/(?P<id>[^/?]+)'
    _module = 'haruhi_dl.extractor.cbsinteractive'


class CBSNewsEmbedIE(CBSIE):
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/embed/video[^#]*#(?P<id>.+)'
    _module = 'haruhi_dl.extractor.cbsnews'


class CBSNewsIE(CBSIE):
    _VALID_URL = 'https?://(?:www\\.)?cbsnews\\.com/(?:news|video)/(?P<id>[\\da-z_-]+)'
    _module = 'haruhi_dl.extractor.cbsnews'


class CBSSportsIE(CBSBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?cbssports\\.com/[^/]+/(?:video|news)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.cbssports'


class CorusIE(ThePlatformFeedIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?P<domain>\n                            (?:\n                                globaltv|\n                                etcanada|\n                                seriesplus|\n                                wnetwork|\n                                ytv\n                            )\\.com|\n                            (?:\n                                hgtv|\n                                foodnetwork|\n                                slice|\n                                history|\n                                showcase|\n                                bigbrothercanada|\n                                abcspark|\n                                disney(?:channel|lachaine)\n                            )\\.ca\n                        )\n                        /(?:[^/]+/)*\n                        (?:\n                            video\\.html\\?.*?\\bv=|\n                            videos?/(?:[^/]+/)*(?:[a-z0-9-]+-)?\n                        )\n                        (?P<id>\n                            [\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12}|\n                            (?:[A-Z]{4})?\\d{12,20}\n                        )\n                    '
    _module = 'haruhi_dl.extractor.corus'


class TheSceneIE(LazyLoadExtractor):
    _VALID_URL = 'https?://thescene\\.com/watch/[^/]+/(?P<id>[^/#?]+)'
    _module = 'haruhi_dl.extractor.thescene'


class TheStarIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?thestar\\.com/(?:[^/]+/)*(?P<id>.+)\\.html'
    _module = 'haruhi_dl.extractor.thestar'


class TheSunIE(LazyLoadExtractor):
    _VALID_URL = 'https://(?:www\\.)?thesun\\.co\\.uk/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.thesun'


class TheWeatherChannelIE(ThePlatformIE):
    _VALID_URL = 'https?://(?:www\\.)?weather\\.com/(?:[^/]+/)*video/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.theweatherchannel'


class ThisAmericanLifeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?thisamericanlife\\.org/(?:radio-archives/episode/|play_full\\.php\\?play=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.thisamericanlife'


class ThisAVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?thisav\\.com/video/(?P<id>[0-9]+)/.*'
    _module = 'haruhi_dl.extractor.thisav'


class ThisOldHouseIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?thisoldhouse\\.com/(?:watch|how-to|tv-episode|(?:[^/]+/)?\\d+)/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.thisoldhouse'


class ThreeQSDNIE(LazyLoadExtractor):
    _VALID_URL = 'https?://playout\\.3qsdn\\.com/(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.threeqsdn'


class TikTokBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tiktok'


class TikTokIE(TikTokBaseIE):
    _VALID_URL = '(?x)\n                        (?:\n                            https?://\n                                (?:\n                                    (?:m\\.)?tiktok\\.com/v|\n                                    (?:www\\.)?tiktok\\.com/(?:share|@[\\w.]+)/video\n                                )/\n                            |tiktok:\n                            )(?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.tiktok'


class TikTokUserIE(TikTokBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tiktok\\.com/@(?P<id>[\\w.]+)/?(?:\\?.+)?$'
    _module = 'haruhi_dl.extractor.tiktok'


class TinyPicIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?tinypic\\.com/player\\.php\\?v=(?P<id>[^&]+)&s=\\d+'
    _module = 'haruhi_dl.extractor.tinypic'


class TMZIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tmz\\.com/videos/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.tmz'


class TMZArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tmz\\.com/\\d{4}/\\d{2}/\\d{2}/(?P<id>[^/]+)/?'
    _module = 'haruhi_dl.extractor.tmz'


class TNAFlixNetworkBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tnaflix'


class TNAFlixNetworkEmbedIE(TNAFlixNetworkBaseIE):
    _VALID_URL = 'https?://player\\.(?:tna|emp)flix\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tnaflix'


class TNAEMPFlixBaseIE(TNAFlixNetworkBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tnaflix'


class TNAFlixIE(TNAEMPFlixBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tnaflix\\.com/[^/]+/(?P<display_id>[^/]+)/video(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tnaflix'


class EMPFlixIE(TNAEMPFlixBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?empflix\\.com/(?:videos/(?P<display_id>.+?)-|[^/]+/(?P<display_id_2>[^/]+)/video)(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.tnaflix'


class MovieFapIE(TNAFlixNetworkBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?moviefap\\.com/videos/(?P<id>[0-9a-f]+)/(?P<display_id>[^/]+)\\.html'
    _module = 'haruhi_dl.extractor.tnaflix'


class ToggleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?mewatch|video\\.toggle)\\.sg/(?:en|zh)/(?:[^/]+/){2,}(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.toggle'


class TOnlineIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?t-online\\.de/tv/(?:[^/]+/)*id_(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tonline'


class ToonGogglesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?toongoggles\\.com/shows/(?P<show_id>\\d+)(?:/[^/]+/episodes/(?P<episode_id>\\d+))?'
    _module = 'haruhi_dl.extractor.toongoggles'


class TouTvIE(RadioCanadaIE):
    _VALID_URL = 'https?://ici\\.tou\\.tv/(?P<id>[a-zA-Z0-9_-]+(?:/S[0-9]+[EC][0-9]+)?)'
    _module = 'haruhi_dl.extractor.toutv'


class ToypicsUserIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videos\\.toypics\\.net/(?!view)(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.toypics'


class ToypicsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videos\\.toypics\\.net/view/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.toypics'


class TrailerAddictIE(LazyLoadExtractor):
    _VALID_URL = '(?:https?://)?(?:www\\.)?traileraddict\\.com/(?:trailer|clip)/(?P<movie>.+?)/(?P<trailer_name>.+)'
    _module = 'haruhi_dl.extractor.traileraddict'


class TriluliluIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?trilulilu\\.ro/(?:[^/]+/)?(?P<id>[^/#\\?]+)'
    _module = 'haruhi_dl.extractor.trilulilu'


class TruNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?trunews\\.com/stream/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.trunews'


class TruTVIE(TurnerBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?trutv\\.com/(?:shows|full-episodes)/(?P<series_slug>[0-9A-Za-z-]+)/(?:videos/(?P<clip_slug>[0-9A-Za-z-]+)|(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.trutv'


class TubaFMIE(LazyLoadExtractor):
    _VALID_URL = 'https?://fm\\.tuba\\.pl/play/(?P<id>\\d+/\\d+)/'
    _module = 'haruhi_dl.extractor.tubafm'


class TubaFMPageIE(LazyLoadExtractor):
    _VALID_URL = 'https://fm\\.tuba\\.pl/radio/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.tubafm'


class Tube8IE(KeezMoviesIE):
    _VALID_URL = 'https?://(?:www\\.)?tube8\\.com/(?:[^/]+/)+(?P<display_id>[^/]+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tube8'


class TubiTvIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tubitv\\.com/(?:video|movies|tv-shows)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.tubitv'


class TumblrIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<blog_name>[^/?#&]+)\\.tumblr\\.com/(?:post|video)/(?P<id>[0-9]+)(?:$|[/?#])'
    _module = 'haruhi_dl.extractor.tumblr'


class TuneInBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tunein'


class TuneInClipIE(TuneInBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/station/.*?audioClipId\\=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tunein'


class TuneInStationIE(TuneInBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:radio/.*?-s|station/.*?StationId=|embed/player/s)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tunein'

    @classmethod
    def suitable(cls, url):
        return False if TuneInClipIE.suitable(url) else super(TuneInStationIE, cls).suitable(url)


class TuneInProgramIE(TuneInBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:radio/.*?-p|program/.*?ProgramId=|embed/player/p)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tunein'


class TuneInTopicIE(TuneInBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?tunein\\.com/(?:topic/.*?TopicId=|embed/player/t)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tunein'


class TuneInShortenerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tun\\.in/(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.tunein'


class TunePkIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:www\\.)?tune\\.pk/(?:video/|player/embed_player.php?.*?\\bvid=)|\n                            embed\\.tune\\.pk/play/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.tunepk'


class TurboIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?turbo\\.fr/videos-voiture/(?P<id>[0-9]+)-'
    _module = 'haruhi_dl.extractor.turbo'


class TV2IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tv2\\.no/v/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tv2'


class TV2ArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tv2\\.no/(?:a|\\d{4}/\\d{2}/\\d{2}(/[^/]+)+)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tv2'


class KatsomoIE(TV2IE):
    _VALID_URL = 'https?://(?:www\\.)?(?:katsomo|mtv)\\.fi/(?:#!/)?(?:[^/]+/[0-9a-z-]+-\\d+/[0-9a-z-]+-|[^/]+/\\d+/[^/]+/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tv2'


class TV2DKIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        (?:\n                            tvsyd|\n                            tv2ostjylland|\n                            tvmidtvest|\n                            tv2fyn|\n                            tv2east|\n                            tv2lorry|\n                            tv2nord\n                        )\\.dk/\n                        (:[^/]+/)*\n                        (?P<id>[^/?\\#&]+)\n                    '
    _module = 'haruhi_dl.extractor.tv2dk'


class TV2DKBornholmPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://play\\.tv2bornholm\\.dk/\\?.*?\\bid=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tv2dk'


class TV2HuIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tv2\\.hu/(?:[^/]+/)+(?P<id>\\d+)_[^/?#]+?\\.html'
    _module = 'haruhi_dl.extractor.tv2hu'


class TV4IE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?\n        (?:\n            tv4\\.se/(?:[^/]+)/klipp/(?:.*)-|\n            tv4play\\.se/\n            (?:\n                (?:program|barn)/(?:[^/]+/|(?:[^\\?]+)\\?video_id=)|\n                iframe/video/|\n                film/|\n                sport/|\n            )\n        )(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.tv4'


class TV5MondePlusIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:tv5mondeplus|revoir\\.tv5monde)\\.com/toutes-les-videos/[^/]+/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.tv5mondeplus'


class TVAIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videos?\\.tva\\.ca/details/_(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tva'


class TVANouvellesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvanouvelles\\.ca/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvanouvelles'


class TVANouvellesArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvanouvelles\\.ca/(?:[^/]+/)+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.tvanouvelles'

    @classmethod
    def suitable(cls, url):
        return False if TVANouvellesIE.suitable(url) else super(TVANouvellesArticleIE, cls).suitable(url)


class TVCIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvc\\.ru/video/iframe/id/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvc'


class TVCArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvc\\.ru/(?!video/iframe/id/)(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.tvc'


class TvigleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:tvigle\\.ru/(?:[^/]+/)+(?P<display_id>[^/]+)/$|cloud\\.tvigle\\.ru/video/(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.tvigle'


class TVLandIE(ParamountNetworkIE):
    _VALID_URL = 'https?://(?:www\\.)?tvland\\.com/(?:video-clips|(?:full-)?episodes)/(?P<id>[^/?#.]+)'
    _module = 'haruhi_dl.extractor.tvland'


class TVN24IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:(?:[^/]+)\\.)?tvn24\\.pl)/(?:[^/]+/)*[^/?#\\s]+[,-](?P<id>\\d+)(?:\\.html)?'
    _module = 'haruhi_dl.extractor.tvn24'


class TVNPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.pl/(?:programy|seriale)-online/[^/,]+,([0-9]+)/(?:[^/,]+,){2}(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvnplayer'


class TVNPlayerSeriesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.pl/(?:programy|seriale)-online/[^/,]+,(?P<id>[0-9]+)/?(?:\\?.+)?(?:#.+)?$'
    _module = 'haruhi_dl.extractor.tvnplayer'


class TVNetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+)\\.tvnet\\.gov\\.vn/[^/]+/(?:\\d+/)?(?P<id>\\d+)(?:/|$)'
    _module = 'haruhi_dl.extractor.tvnet'


class TVNoeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvnoe\\.cz/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.tvnoe'


class TVNowBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tvnow'


class TVNowIE(TVNowBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/(?P<station>[^/]+)/\n                        (?P<show_id>[^/]+)/\n                        (?!(?:list|jahr)(?:/|$))(?P<id>[^/?\\#&]+)\n                    '
    _module = 'haruhi_dl.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url) or TVNowSeasonIE.suitable(url) or TVNowAnnualIE.suitable(url) or TVNowShowIE.suitable(url)
                else super(TVNowIE, cls).suitable(url))


class TVNowNewIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?P<base_url>https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/\n                        (?:shows|serien))/\n                        (?P<show>[^/]+)-\\d+/\n                        [^/]+/\n                        episode-\\d+-(?P<episode>[^/?$&]+)-(?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.tvnow'


class TVNowNewBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tvnow'


class TVNowListBaseIE(TVNowNewBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowSeasonIE(TVNowListBaseIE):
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    /staffel-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowAnnualIE(TVNowListBaseIE):
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    /(?P<year>\\d{4})-(?P<month>\\d{2})'
    _module = 'haruhi_dl.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url)
                else super(TVNowListBaseIE, cls).suitable(url))


class TVNowShowIE(TVNowListBaseIE):
    _VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    '
    _module = 'haruhi_dl.extractor.tvnow'

    @classmethod
    def suitable(cls, url):
        return (False if TVNowNewIE.suitable(url) or TVNowSeasonIE.suitable(url) or TVNowAnnualIE.suitable(url)
                else super(TVNowShowIE, cls).suitable(url))


class TVPEmbedIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        (?:\n            tvp:\n            |https?://\n                (?:[^/]+\\.)?\n                (?:tvp(?:parlament)?\\.pl|tvp\\.info|polandin\\.com)/\n                (?:sess/\n                        (?:tvplayer\\.php\\?.*?object_id\n                        |TVPlayer2/(?:embed|api)\\.php\\?.*[Ii][Dd])\n                    |shared/details\\.php\\?.*?object_id)\n                =)\n        (?P<id>\\d+)\n    '
    _module = 'haruhi_dl.extractor.tvp'


class TVPIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?(?:tvp(?:parlament)?\\.(?:pl|info)|polandin\\.com)/(?:video/(?:[^,\\s]*,)*|(?:(?!\\d+/)[^/]+/)*)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvp'


class TVPStreamIE(LazyLoadExtractor):
    _VALID_URL = '(?:tvpstream:|https?://tvpstream\\.vod\\.tvp\\.pl/(?:\\?(?:[^&]+[&;])*channel_id=)?)(?P<id>\\d*)'
    _module = 'haruhi_dl.extractor.tvp'


class TVPWebsiteIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vod\\.tvp\\.pl/website/(?P<display_id>[^,]+),(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvp'


class TVPlayIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?:\n                        mtg:|\n                        https?://\n                            (?:www\\.)?\n                            (?:\n                                tvplay(?:\\.skaties)?\\.lv(?:/parraides)?|\n                                (?:tv3play|play\\.tv3)\\.lt(?:/programos)?|\n                                tv3play(?:\\.tv3)?\\.ee/sisu|\n                                (?:tv(?:3|6|8|10)play|viafree)\\.se/program|\n                                (?:(?:tv3play|viasat4play|tv6play|viafree)\\.no|(?:tv3play|viafree)\\.dk)/programmer|\n                                play\\.nova(?:tv)?\\.bg/programi\n                            )\n                            /(?:[^/]+/)+\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.tvplay'


class ViafreeIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?\n                        viafree\\.(?P<country>dk|no|se)\n                        /(?P<id>program(?:mer)?/(?:[^/]+/)+[^/?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.tvplay'

    @classmethod
    def suitable(cls, url):
        return False if TVPlayIE.suitable(url) else super(ViafreeIE, cls).suitable(url)


class TVPlayHomeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tvplay\\.(?:tv3\\.lt|skaties\\.lv|tv3\\.ee)/[^/]+/[^/?#&]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tvplay'


class TVPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?tvplayer\\.com/watch/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.tvplayer'


class TweakersIE(LazyLoadExtractor):
    _VALID_URL = 'https?://tweakers\\.net/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.tweakers'


class TwentyFourVideoIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?P<host>\n                            (?:(?:www|porno?)\\.)?24video\\.\n                            (?:net|me|xxx|sexy?|tube|adult|site|vip)\n                        )/\n                        (?:\n                            video/(?:(?:view|xml)/)?|\n                            player/new24_play\\.swf\\?id=\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.twentyfourvideo'


class TwentyMinutenIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?20min\\.ch/\n                        (?:\n                            videotv/*\\?.*?\\bvid=|\n                            videoplayer/videoplayer\\.html\\?.*?\\bvideoId@\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.twentymin'


class TwentyThreeVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<domain>[^.]+\\.(?:twentythree\\.net|23video\\.com|filmweb\\.no))/v\\.ihtml/player\\.html\\?(?P<query>.*?\\bphoto(?:_|%5f)id=(?P<id>\\d+).*)'
    _module = 'haruhi_dl.extractor.twentythreevideo'


class TwitCastingIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:[^/]+\\.)?twitcasting\\.tv/(?P<uploader_id>[^/]+)/movie/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.twitcasting'


class TwitchBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.twitch'


class TwitchVodIE(TwitchBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/(?:[^/]+/v(?:ideo)?|videos)/|\n                            player\\.twitch\\.tv/\\?.*?\\bvideo=v?\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.twitch'


class TwitchGraphQLBaseIE(TwitchBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.twitch'


class TwitchCollectionIE(TwitchGraphQLBaseIE):
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/collections/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.twitch'


class TwitchPlaylistBaseIE(TwitchGraphQLBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.twitch'


class TwitchVideosIE(TwitchPlaylistBaseIE):
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/(?:videos|profile)'
    _module = 'haruhi_dl.extractor.twitch'

    @classmethod
    def suitable(cls, url):
        return (False
                if any(ie.suitable(url) for ie in (
                    TwitchVideosClipsIE,
                    TwitchVideosCollectionsIE))
                else super(TwitchVideosIE, cls).suitable(url))


class TwitchVideosClipsIE(TwitchPlaylistBaseIE):
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/(?:clips|videos/*?\\?.*?\\bfilter=clips)'
    _module = 'haruhi_dl.extractor.twitch'


class TwitchVideosCollectionsIE(TwitchPlaylistBaseIE):
    _VALID_URL = 'https?://(?:(?:www|go|m)\\.)?twitch\\.tv/(?P<id>[^/]+)/videos/*?\\?.*?\\bfilter=collections'
    _module = 'haruhi_dl.extractor.twitch'


class TwitchStreamIE(TwitchGraphQLBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/|\n                            player\\.twitch\\.tv/\\?.*?\\bchannel=\n                        )\n                        (?P<id>[^/#?]+)\n                    '
    _module = 'haruhi_dl.extractor.twitch'

    @classmethod
    def suitable(cls, url):
        return (False
                if any(ie.suitable(url) for ie in (
                    TwitchVodIE,
                    TwitchCollectionIE,
                    TwitchVideosIE,
                    TwitchVideosClipsIE,
                    TwitchVideosCollectionsIE,
                    TwitchClipsIE))
                else super(TwitchStreamIE, cls).suitable(url))


class TwitchClipsIE(TwitchBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            clips\\.twitch\\.tv/(?:embed\\?.*?\\bclip=|(?:[^/]+/)*)|\n                            (?:(?:www|go|m)\\.)?twitch\\.tv/[^/]+/clip/\n                        )\n                        (?P<id>[^/?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.twitch'


class TwitterCardIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/i/(?:cards/tfw/v1|videos(?:/tweet)?)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.twitter'


class TwitterBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.twitter'


class TwitterIE(TwitterBaseIE):
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/(?:(?:i/web|[^/]+)/status|statuses)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.twitter'


class TwitterAmplifyIE(TwitterBaseIE):
    _VALID_URL = 'https?://amp\\.twimg\\.com/v/(?P<id>[0-9a-f\\-]{36})'
    _module = 'haruhi_dl.extractor.twitter'


class TwitterBroadcastIE(TwitterBaseIE, PeriscopeBaseIE):
    _VALID_URL = 'https?://(?:(?:www|m(?:obile)?)\\.)?twitter\\.com/i/broadcasts/(?P<id>[0-9a-zA-Z]{13})'
    _module = 'haruhi_dl.extractor.twitter'


class UdemyIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[^/]+\\.)?udemy\\.com/\n                        (?:\n                            [^#]+\\#/lecture/|\n                            lecture/view/?\\?lectureId=|\n                            [^/]+/learn/v4/t/lecture/\n                        )\n                        (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.udemy'


class UdemyCourseIE(UdemyIE):
    _VALID_URL = 'https?://(?:[^/]+\\.)?udemy\\.com/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.udemy'

    @classmethod
    def suitable(cls, url):
        return False if UdemyIE.suitable(url) else super(UdemyCourseIE, cls).suitable(url)


class UDNEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://video\\.udn\\.com/(?:embed|play)/news/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.udn'


class ImgGamingBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.imggaming'


class UFCTVIE(ImgGamingBaseIE):
    _VALID_URL = 'https?://(?P<domain>(?:(?:app|www)\\.)?(?:ufc\\.tv|(?:ufc)?fightpass\\.com)|ufcfightpass\\.img(?:dge|gaming)\\.com)/(?P<type>live|playlist|video)/(?P<id>\\d+)(?:\\?.*?\\bplaylistId=(?P<playlist_id>\\d+))?'
    _module = 'haruhi_dl.extractor.ufctv'


class UFCArabiaIE(ImgGamingBaseIE):
    _VALID_URL = 'https?://(?P<domain>(?:(?:app|www)\\.)?ufcarabia\\.(?:ae|com))/(?P<type>live|playlist|video)/(?P<id>\\d+)(?:\\?.*?\\bplaylistId=(?P<playlist_id>\\d+))?'
    _module = 'haruhi_dl.extractor.ufctv'


class UKTVPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://uktvplay\\.uktv\\.co\\.uk/.+?\\?.*?\\bvideo=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.uktvplay'


class DigitekaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://(?:www\\.)?(?:digiteka\\.net|ultimedia\\.com)/\n        (?:\n            deliver/\n            (?P<embed_type>\n                generic|\n                musique\n            )\n            (?:/[^/]+)*/\n            (?:\n                src|\n                article\n            )|\n            default/index/video\n            (?P<site_type>\n                generic|\n                music\n            )\n            /id\n        )/(?P<id>[\\d+a-z]+)'
    _module = 'haruhi_dl.extractor.digiteka'


class DLiveVODIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dlive\\.tv/p/(?P<uploader_id>.+?)\\+(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.dlive'


class DLiveStreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?dlive\\.tv/(?!p/)(?P<id>[\\w.-]+)'
    _module = 'haruhi_dl.extractor.dlive'


class UMGDeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?universal-music\\.de/[^/]+/videos/[^/?#]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.umg'


class UnistraIE(LazyLoadExtractor):
    _VALID_URL = 'https?://utv\\.unistra\\.fr/(?:index|video)\\.php\\?id_video\\=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.unistra'


class UnityIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?unity3d\\.com/learn/tutorials/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.unity'


class UOLIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?uol\\.com\\.br/.*?(?:(?:mediaId|v)=|view/(?:[a-z0-9]+/)?|video(?:=|/(?:\\d{4}/\\d{2}/\\d{2}/)?))(?P<id>\\d+|[\\w-]+-[A-Z0-9]+)'
    _module = 'haruhi_dl.extractor.uol'


class UplynkIE(LazyLoadExtractor):
    _VALID_URL = 'https?://.*?\\.uplynk\\.com/(?P<path>ext/[0-9a-f]{32}/(?P<external_id>[^/?&]+)|(?P<id>[0-9a-f]{32}))\\.(?:m3u8|json)(?:.*?\\bpbs=(?P<session_id>[^&]+))?'
    _module = 'haruhi_dl.extractor.uplynk'


class UplynkPreplayIE(UplynkIE):
    _VALID_URL = 'https?://.*?\\.uplynk\\.com/preplay2?/(?P<path>ext/[0-9a-f]{32}/(?P<external_id>[^/?&]+)|(?P<id>[0-9a-f]{32}))\\.json'
    _module = 'haruhi_dl.extractor.uplynk'


class UrortIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?urort\\.p3\\.no/#!/Band/(?P<id>[^/]+)$'
    _module = 'haruhi_dl.extractor.urort'


class URPlayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ur(?:play|skola)\\.se/(?:program|Produkter)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.urplay'


class USANetworkIE(AdobePassIE):
    _VALID_URL = 'https?://(?:www\\.)?usanetwork\\.com/(?:[^/]+/videos|movies)/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.usanetwork'


class USATodayIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?usatoday\\.com/(?:[^/]+/)*(?P<id>[^?/#]+)'
    _module = 'haruhi_dl.extractor.usatoday'


class UstreamIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:ustream\\.tv|video\\.ibm\\.com)/(?P<type>recorded|embed|embed/recorded)/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.ustream'


class UstreamChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?ustream\\.tv/channel/(?P<slug>.+)'
    _module = 'haruhi_dl.extractor.ustream'


class UstudioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|v1)\\.)?ustudio\\.com/video/(?P<id>[^/]+)/(?P<display_id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.ustudio'


class UstudioEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:app|embed)\\.)?ustudio\\.com/embed/(?P<uid>[^/]+)/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.ustudio'


class Varzesh3IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?video\\.varzesh3\\.com/(?:[^/]+/)+(?P<id>[^/]+)/?'
    _module = 'haruhi_dl.extractor.varzesh3'


class Vbox7IE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:[^/]+\\.)?vbox7\\.com/\n                        (?:\n                            play:|\n                            (?:\n                                emb/external\\.php|\n                                player/ext\\.swf\n                            )\\?.*?\\bvid=\n                        )\n                        (?P<id>[\\da-fA-F]+)\n                    '
    _module = 'haruhi_dl.extractor.vbox7'


class VeeHDIE(LazyLoadExtractor):
    _VALID_URL = 'https?://veehd\\.com/video/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.veehd'


class VeohIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?veoh\\.com/(?:watch|embed|iphone/#_Watch)/(?P<id>(?:v|e|yapi-)[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.veoh'


class VestiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?vesti\\.ru/(?P<id>.+)'
    _module = 'haruhi_dl.extractor.vesti'


class VevoBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vevo'


class VevoIE(VevoBaseIE):
    _VALID_URL = '(?x)\n        (?:https?://(?:www\\.)?vevo\\.com/watch/(?!playlist|genre)(?:[^/]+/(?:[^/]+/)?)?|\n           https?://cache\\.vevo\\.com/m/html/embed\\.html\\?video=|\n           https?://videoplayer\\.vevo\\.com/embed/embedded\\?videoId=|\n           https?://embed\\.vevo\\.com/.*?[?&]isrc=|\n           vevo:)\n        (?P<id>[^&?#]+)'
    _module = 'haruhi_dl.extractor.vevo'


class VevoPlaylistIE(VevoBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?vevo\\.com/watch/(?P<kind>playlist|genre)/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.vevo'


class BTArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bt\\.no/(?:[^/]+/)+(?P<id>[^/]+)-\\d+\\.html'
    _module = 'haruhi_dl.extractor.vgtv'


class BTVestlendingenIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bt\\.no/spesial/vestlendingen/#!/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.vgtv'


class VH1IE(MTVServicesInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vh1\\.com/(?:video-clips|episodes)/(?P<id>[^/?#.]+)'
    _module = 'haruhi_dl.extractor.vh1'


class ViceBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vice'


class ViceIE(ViceBaseIE, AdobePassIE):
    _VALID_URL = 'https?://(?:(?:video|vms)\\.vice|(?:www\\.)?vice(?:land|tv))\\.com/(?P<locale>[^/]+)/(?:video/[^/]+|embed)/(?P<id>[\\da-f]{24})'
    _module = 'haruhi_dl.extractor.vice'


class ViceArticleIE(ViceBaseIE):
    _VALID_URL = 'https://(?:www\\.)?vice\\.com/(?P<locale>[^/]+)/article/(?:[0-9a-z]{6}/)?(?P<id>[^?#]+)'
    _module = 'haruhi_dl.extractor.vice'


class ViceShowIE(ViceBaseIE):
    _VALID_URL = 'https?://(?:video\\.vice|(?:www\\.)?vice(?:land|tv))\\.com/(?P<locale>[^/]+)/show/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.vice'


class VidbitIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vidbit\\.co/(?:watch|embed)\\?.*?\\bv=(?P<id>[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.vidbit'


class ViddlerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?viddler\\.com/(?:v|embed|player)/(?P<id>[a-z0-9]+)(?:.+?\\bsecret=(\\d+))?'
    _module = 'haruhi_dl.extractor.viddler'


class VideaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        videa(?:kid)?\\.hu/\n                        (?:\n                            videok/(?:[^/]+/)*[^?#&]+-|\n                            player\\?.*?\\bv=|\n                            player/v/\n                        )\n                        (?P<id>[^?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.videa'


class VideoDetectiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?videodetective\\.com/[^/]+/[^/]+/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.videodetective'


class VideofyMeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.videofy\\.me/.+?|p\\.videofy\\.me/v)/(?P<id>\\d+)(&|#|$)'
    _module = 'haruhi_dl.extractor.videofyme'


class VideomoreIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    videomore:(?P<sid>\\d+)$|\n                    https?://(?:player\\.)?videomore\\.ru/\n                        (?:\n                            (?:\n                                embed|\n                                [^/]+/[^/]+\n                            )/|\n                            [^/]*\\?.*?\\btrack_id=\n                        )\n                        (?P<id>\\d+)\n                        (?:[/?#&]|\\.(?:xml|json)|$)\n                    '
    _module = 'haruhi_dl.extractor.videomore'


class VideomoreVideoIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videomore\\.ru/(?:(?:[^/]+/){2})?(?P<id>[^/?#&]+)(?:/*|[?#&].*?)$'
    _module = 'haruhi_dl.extractor.videomore'

    @classmethod
    def suitable(cls, url):
        return False if VideomoreIE.suitable(url) else super(VideomoreVideoIE, cls).suitable(url)


class VideomoreSeasonIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videomore\\.ru/(?!embed)(?P<id>[^/]+/[^/?#&]+)(?:/*|[?#&].*?)$'
    _module = 'haruhi_dl.extractor.videomore'

    @classmethod
    def suitable(cls, url):
        return (False if (VideomoreIE.suitable(url) or VideomoreVideoIE.suitable(url))
                else super(VideomoreSeasonIE, cls).suitable(url))


class VideoPressIE(LazyLoadExtractor):
    _VALID_URL = 'https?://videopress\\.com/embed/(?P<id>[\\da-zA-Z]+)'
    _module = 'haruhi_dl.extractor.videopress'


class VidioIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vidio\\.com/watch/(?P<id>\\d+)-(?P<display_id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.vidio'


class VidLiiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vidlii\\.com/(?:watch|embed)\\?.*?\\bv=(?P<id>[0-9A-Za-z_-]{11})'
    _module = 'haruhi_dl.extractor.vidlii'


class VidmeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vid\\.me/(?:e/)?(?P<id>[\\da-zA-Z]{,5})(?:[^\\da-zA-Z]|$)'
    _module = 'haruhi_dl.extractor.vidme'


class VidmeListBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vidme'


class VidmeUserIE(VidmeListBaseIE):
    _VALID_URL = 'https?://vid\\.me/(?:e/)?(?P<id>[\\da-zA-Z_-]{6,})(?!/likes)(?:[^\\da-zA-Z_-]|$)'
    _module = 'haruhi_dl.extractor.vidme'


class VidmeUserLikesIE(VidmeListBaseIE):
    _VALID_URL = 'https?://vid\\.me/(?:e/)?(?P<id>[\\da-zA-Z_-]{6,})/likes'
    _module = 'haruhi_dl.extractor.vidme'


class VidziIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vidzi\\.(?:tv|cc|si|nu)/(?:embed-)?(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.vidzi'


class VierIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?(?P<site>vier|vijf)\\.be/\n                        (?:\n                            (?:\n                                [^/]+/videos|\n                                video(?:/[^/]+)*\n                            )/\n                            (?P<display_id>[^/]+)(?:/(?P<id>\\d+))?|\n                            (?:\n                                video/v3/embed|\n                                embed/video/public\n                            )/(?P<embed_id>\\d+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.vier'


class VierVideosIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>vier|vijf)\\.be/(?P<program>[^/]+)/videos(?:\\?.*\\bpage=(?P<page>\\d+)|$)'
    _module = 'haruhi_dl.extractor.vier'


class ViewLiftBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.viewlift'


class ViewLiftIE(ViewLiftBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?(?P<domain>(?:(?:main\\.)?snagfilms|snagxtreme|funnyforfree|kiddovid|winnersview|(?:monumental|lax)sportsnetwork|vayafilm|failarmy|ftfnext|lnppass\\.legapallacanestro|moviespree|app\\.myoutdoortv|neoufitness|pflmma|theidentitytb)\\.com|(?:hoichoi|app\\.horseandcountry|kronon|marquee|supercrosslive)\\.tv)(?P<path>(?:/(?:films/title|show|(?:news/)?videos?|watch))?/(?P<id>[^?#]+))'
    _module = 'haruhi_dl.extractor.viewlift'

    @classmethod
    def suitable(cls, url):
        return False if ViewLiftEmbedIE.suitable(url) else super(ViewLiftIE, cls).suitable(url)


class ViewLiftEmbedIE(ViewLiftBaseIE):
    _VALID_URL = 'https?://(?:(?:www|embed)\\.)?(?P<domain>(?:(?:main\\.)?snagfilms|snagxtreme|funnyforfree|kiddovid|winnersview|(?:monumental|lax)sportsnetwork|vayafilm|failarmy|ftfnext|lnppass\\.legapallacanestro|moviespree|app\\.myoutdoortv|neoufitness|pflmma|theidentitytb)\\.com|(?:hoichoi|app\\.horseandcountry|kronon|marquee|supercrosslive)\\.tv)/embed/player\\?.*\\bfilmId=(?P<id>[\\da-f]{8}-(?:[\\da-f]{4}-){3}[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.viewlift'


class ViideaIE(LazyLoadExtractor):
    _VALID_URL = '(?x)https?://(?:www\\.)?(?:\n            videolectures\\.net|\n            flexilearn\\.viidea\\.net|\n            presentations\\.ocwconsortium\\.org|\n            video\\.travel-zoom\\.si|\n            video\\.pomp-forum\\.si|\n            tv\\.nil\\.si|\n            video\\.hekovnik.com|\n            video\\.szko\\.si|\n            kpk\\.viidea\\.com|\n            inside\\.viidea\\.net|\n            video\\.kiberpipa\\.org|\n            bvvideo\\.si|\n            kongres\\.viidea\\.net|\n            edemokracija\\.viidea\\.com\n        )(?:/lecture)?/(?P<id>[^/]+)(?:/video/(?P<part>\\d+))?/*(?:[#?].*)?$'
    _module = 'haruhi_dl.extractor.viidea'


class VimeoBaseInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoIE(VimeoBaseInfoExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                www|\n                                player\n                            )\n                            \\.\n                        )?\n                        vimeo(?:pro)?\\.com/\n                        (?!(?:channels|album|showcase)/[^/?#]+/?(?:$|[?#])|[^/]+/review/|ondemand/)\n                        (?:.*?/)?\n                        (?:\n                            (?:\n                                play_redirect_hls|\n                                moogaloop\\.swf)\\?clip_id=\n                            )?\n                        (?:videos?/)?\n                        (?P<id>[0-9]+)\n                        (?:/[\\da-f]+)?\n                        /?(?:[?&].*)?(?:[#].*)?$\n                    '
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoAlbumIE(VimeoBaseInfoExtractor):
    _VALID_URL = 'https://vimeo\\.com/(?:album|showcase)/(?P<id>\\d+)(?:$|[?#]|/(?!video))'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoChannelIE(VimeoBaseInfoExtractor):
    _VALID_URL = 'https://vimeo\\.com/channels/(?P<id>[^/?#]+)/?(?:$|[?#])'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoGroupsIE(VimeoChannelIE):
    _VALID_URL = 'https://vimeo\\.com/groups/(?P<id>[^/]+)(?:/(?!videos?/\\d+)|$)'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoLikesIE(VimeoChannelIE):
    _VALID_URL = 'https://(?:www\\.)?vimeo\\.com/(?P<id>[^/]+)/likes/?(?:$|[?#]|sort:)'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoOndemandIE(VimeoIE):
    _VALID_URL = 'https?://(?:www\\.)?vimeo\\.com/ondemand/([^/]+/)?(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoReviewIE(VimeoBaseInfoExtractor):
    _VALID_URL = '(?P<url>https://vimeo\\.com/[^/]+/review/(?P<id>[^/]+)/[0-9a-f]{10})'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoUserIE(VimeoChannelIE):
    _VALID_URL = 'https://vimeo\\.com/(?!(?:[0-9]+|watchlater)(?:$|[?#/]))(?P<id>[^/]+)(?:/videos|[#?]|$)'
    _module = 'haruhi_dl.extractor.vimeo'


class VimeoWatchLaterIE(VimeoChannelIE):
    _VALID_URL = 'https://vimeo\\.com/(?:home/)?watchlater|:vimeowatchlater'
    _module = 'haruhi_dl.extractor.vimeo'


class VHXEmbedIE(VimeoBaseInfoExtractor):
    _VALID_URL = 'https?://embed\\.vhx\\.tv/videos/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.vimeo'


class VimpleIE(SprutoBaseIE):
    _VALID_URL = 'https?://(?:player\\.vimple\\.(?:ru|co)/iframe|vimple\\.(?:ru|co))/(?P<id>[\\da-f-]{32,36})'
    _module = 'haruhi_dl.extractor.vimple'


class VineIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vine\\.co/(?:v|oembed)/(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.vine'


class VineUserIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vine\\.co/(?P<u>u/)?(?P<user>[^/]+)'
    _module = 'haruhi_dl.extractor.vine'

    @classmethod
    def suitable(cls, url):
        return False if VineIE.suitable(url) else super(VineUserIE, cls).suitable(url)


class VikiBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.viki'


class VikiIE(VikiBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?viki\\.(?:com|net|mx|jp|fr)/(?:videos|player)/(?P<id>[0-9]+v)'
    _module = 'haruhi_dl.extractor.viki'


class VikiChannelIE(VikiBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?viki\\.(?:com|net|mx|jp|fr)/(?:tv|news|movies|artists)/(?P<id>[0-9]+c)'
    _module = 'haruhi_dl.extractor.viki'


class ViqeoIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        (?:\n                            viqeo:|\n                            https?://cdn\\.viqeo\\.tv/embed/*\\?.*?\\bvid=|\n                            https?://api\\.viqeo\\.tv/v\\d+/data/startup?.*?\\bvideo(?:%5B%5D|\\[\\])=\n                        )\n                        (?P<id>[\\da-f]+)\n                    '
    _module = 'haruhi_dl.extractor.viqeo'


class ViuBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.viu'


class ViuIE(ViuBaseIE):
    _VALID_URL = '(?:viu:|https?://[^/]+\\.viu\\.com/[a-z]{2}/media/)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.viu'


class ViuPlaylistIE(ViuBaseIE):
    _VALID_URL = 'https?://www\\.viu\\.com/[^/]+/listing/playlist-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.viu'


class ViuOTTIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?viu\\.com/ott/(?P<country_code>[a-z]{2})/[a-z]{2}-[a-z]{2}/vod/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.viu'


class VKBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vk'


class VKIE(VKBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:\n                                (?:(?:m|new)\\.)?vk\\.com/video_|\n                                (?:www\\.)?daxab.com/\n                            )\n                            ext\\.php\\?(?P<embed_query>.*?\\boid=(?P<oid>-?\\d+).*?\\bid=(?P<id>\\d+).*)|\n                            (?:\n                                (?:(?:m|new)\\.)?vk\\.com/(?:.+?\\?.*?z=)?video|\n                                (?:www\\.)?daxab.com/embed/\n                            )\n                            (?P<videoid>-?\\d+_\\d+)(?:.*\\blist=(?P<list_id>[\\da-f]+))?\n                        )\n                    '
    _module = 'haruhi_dl.extractor.vk'


class VKUserVideosIE(VKBaseIE):
    _VALID_URL = 'https?://(?:(?:m|new)\\.)?vk\\.com/videos(?P<id>-?[0-9]+)(?!\\?.*\\bz=video)(?:[/?#&](?:.*?\\bsection=(?P<section>\\w+))?|$)'
    _module = 'haruhi_dl.extractor.vk'


class VKWallPostIE(VKBaseIE):
    _VALID_URL = 'https?://(?:(?:(?:(?:m|new)\\.)?vk\\.com/(?:[^?]+\\?.*\\bw=)?wall(?P<id>-?\\d+_\\d+)))'
    _module = 'haruhi_dl.extractor.vk'


class VLiveIE(NaverBaseIE):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?vlive\\.tv/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.vlive'

    @classmethod
    def suitable(cls, url):
        return False if VLivePlaylistIE.suitable(url) else super(VLiveIE, cls).suitable(url)


class VLiveChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://channels\\.vlive\\.tv/(?P<id>[0-9A-Z]+)'
    _module = 'haruhi_dl.extractor.vlive'


class VLivePlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|m)\\.)?vlive\\.tv/video/(?P<video_id>[0-9]+)/playlist/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.vlive'


class VodlockerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vodlocker\\.(?:com|city)/(?:embed-)?(?P<id>[0-9a-zA-Z]+)(?:\\..*?)?'
    _module = 'haruhi_dl.extractor.vodlocker'


class VODPlIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vod\\.pl/(?:[^/]+/)+(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.vodpl'


class VODPlatformIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www\\.)?vod-platform\\.net|embed\\.kwikmotion\\.com)/[eE]mbed/(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.vodplatform'


class VoiceRepublicIE(LazyLoadExtractor):
    _VALID_URL = 'https?://voicerepublic\\.com/(?:talks|embed)/(?P<id>[0-9a-z-]+)'
    _module = 'haruhi_dl.extractor.voicerepublic'


class VootIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?voot\\.com/(?:[^/]+/)+(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.voot'


class VoxMediaVolumeIE(OnceIE):
    _VALID_URL = 'https?://volume\\.vox-cdn\\.com/embed/(?P<id>[0-9a-f]{9})'
    _module = 'haruhi_dl.extractor.voxmedia'


class VoxMediaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:(?:theverge|vox|sbnation|eater|polygon|curbed|racked|funnyordie)\\.com|recode\\.net)/(?:[^/]+/)*(?P<id>[^/?]+)'
    _module = 'haruhi_dl.extractor.voxmedia'


class VRTIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<site>vrt\\.be/vrtnws|sporza\\.be)/[a-z]{2}/\\d{4}/\\d{2}/\\d{2}/(?P<id>[^/?&#]+)'
    _module = 'haruhi_dl.extractor.vrt'


class VrakIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vrak\\.tv/videos\\?.*?\\btarget=(?P<id>[\\d.]+)'
    _module = 'haruhi_dl.extractor.vrak'


class VRVBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.vrv'


class VRVIE(VRVBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?vrv\\.co/watch/(?P<id>[A-Z0-9]+)'
    _module = 'haruhi_dl.extractor.vrv'


class CrunchyrollIE(CrunchyrollBaseIE, VRVIE):
    _VALID_URL = 'https?://(?:(?P<prefix>www|m)\\.)?(?P<url>crunchyroll\\.(?:com|fr)/(?:media(?:-|/\\?id=)|(?:[^/]*/){1,2}[^/?&]*?)(?P<video_id>[0-9]+))(?:[/?&]|$)'
    _module = 'haruhi_dl.extractor.crunchyroll'


class VRVSeriesIE(VRVBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?vrv\\.co/series/(?P<id>[A-Z0-9]+)'
    _module = 'haruhi_dl.extractor.vrv'


class VShareIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vshare\\.io/[dv]/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.vshare'


class MedialaanIE(GigyaBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.|nieuws\\.)?\n                        (?:\n                            (?P<site_id>vtm|q2|vtmkzoom)\\.be/\n                            (?:\n                                video(?:/[^/]+/id/|/?\\?.*?\\baid=)|\n                                (?:[^/]+/)*\n                            )\n                        )\n                        (?P<id>[^/?#&]+)\n                    '
    _module = 'haruhi_dl.extractor.medialaan'


class VubeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vube\\.com/(?:[^/]+/)+(?P<id>[\\da-zA-Z]{10})\\b'
    _module = 'haruhi_dl.extractor.vube'


class VuClipIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:m\\.)?vuclip\\.com/w\\?.*?cid=(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.vuclip'


class VVVVIDIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?vvvvid\\.it/(?:#!)?(?:show|anime|film|series)/(?P<show_id>\\d+)/[^/]+/(?P<season_id>\\d+)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.vvvvid'


class VyboryMosIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vybory\\.mos\\.ru/(?:#precinct/|account/channels\\?.*?\\bstation_id=)(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.vyborymos'


class VzaarIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|view)\\.)?vzaar\\.com/(?:videos/)?(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.vzaar'


class WakanimIE(LazyLoadExtractor):
    _VALID_URL = 'https://(?:www\\.)?wakanim\\.tv/[^/]+/v2/catalogue/episode/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.wakanim'


class WallaIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vod\\.walla\\.co\\.il/[^/]+/(?P<id>\\d+)/(?P<display_id>.+)'
    _module = 'haruhi_dl.extractor.walla'


class WashingtonPostIE(LazyLoadExtractor):
    _VALID_URL = '(?:washingtonpost:|https?://(?:www\\.)?washingtonpost\\.com/video/(?:[^/]+/)*)(?P<id>[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.washingtonpost'


class WashingtonPostArticleIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?washingtonpost\\.com/(?:[^/]+/)*(?P<id>[^/?#]+)'
    _module = 'haruhi_dl.extractor.washingtonpost'

    @classmethod
    def suitable(cls, url):
        return False if WashingtonPostIE.suitable(url) else super(WashingtonPostArticleIE, cls).suitable(url)


class WatIE(LazyLoadExtractor):
    _VALID_URL = '(?:wat:|https?://(?:www\\.)?wat\\.tv/video/.*-)(?P<id>[0-9a-z]+)'
    _module = 'haruhi_dl.extractor.wat'


class WatchBoxIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?watchbox\\.de/(?P<kind>serien|filme)/(?:[^/]+/)*[^/]+-(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.watchbox'


class WatchIndianPornIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?watchindianporn\\.net/(?:[^/]+/)*video/(?P<display_id>[^/]+)-(?P<id>[a-zA-Z0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.watchindianporn'


class WDRIE(LazyLoadExtractor):
    _VALID_URL = 'https?://deviceids-medp\\.wdr\\.de/ondemand/\\d+/(?P<id>\\d+)\\.js'
    _module = 'haruhi_dl.extractor.wdr'


class WDRPageIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\d?\\.)?(?:wdr\\d?|sportschau)\\.de/(?:mediathek/)?(?:[^/]+/)*(?P<display_id>[^/]+)\\.html|https?://(?:www\\.)wdrmaus.de/(?:[^/]+/){1,2}[^/?#]+\\.php5'
    _module = 'haruhi_dl.extractor.wdr'


class WDRElefantIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)wdrmaus\\.de/elefantenseite/#(?P<id>.+)'
    _module = 'haruhi_dl.extractor.wdr'


class WDRMobileIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        https?://mobile-ondemand\\.wdr\\.de/\n        .*?/fsk(?P<age_limit>[0-9]+)\n        /[0-9]+/[0-9]+/\n        (?P<id>[0-9]+)_(?P<title>[0-9]+)'
    _module = 'haruhi_dl.extractor.wdr'


class WebcasterIE(LazyLoadExtractor):
    _VALID_URL = 'https?://bl\\.webcaster\\.pro/(?:quote|media)/start/free_(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.webcaster'


class WebcasterFeedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://bl\\.webcaster\\.pro/feed/start/free_(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.webcaster'


class WebOfStoriesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?webofstories\\.com/play/(?:[^/]+/)?(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.webofstories'


class WebOfStoriesPlaylistIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?webofstories\\.com/playAll/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.webofstories'


class WeiboIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?weibo\\.com/[0-9]+/(?P<id>[a-zA-Z0-9]+)'
    _module = 'haruhi_dl.extractor.weibo'


class WeiboMobileIE(LazyLoadExtractor):
    _VALID_URL = 'https?://m\\.weibo\\.cn/status/(?P<id>[0-9]+)(\\?.+)?'
    _module = 'haruhi_dl.extractor.weibo'


class WeiqiTVIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?weiqitv\\.com/index/video_play\\?videoId=(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.weiqitv'


class WistiaIE(LazyLoadExtractor):
    _VALID_URL = '(?:wistia:|https?://(?:fast\\.)?wistia\\.(?:net|com)/embed/(?:iframe|medias)/)(?P<id>[a-z0-9]{10})'
    _module = 'haruhi_dl.extractor.wistia'


class WorldStarHipHopIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www|m)\\.worldstar(?:candy|hiphop)\\.com/(?:videos|android)/video\\.php\\?.*?\\bv=(?P<id>[^&]+)'
    _module = 'haruhi_dl.extractor.worldstarhiphop'


class WpPlIE(LazyLoadExtractor):
    _VALID_URL = 'https://(?:[^/]+\\.)?wp\\.pl/[^/]+-(?P<id>\\d+v)'
    _module = 'haruhi_dl.extractor.wppl'


class WSJIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        (?:\n                            https?://video-api\\.wsj\\.com/api-video/player/iframe\\.html\\?.*?\\bguid=|\n                            https?://(?:www\\.)?(?:wsj|barrons)\\.com/video/(?:[^/]+/)+|\n                            wsj:\n                        )\n                        (?P<id>[a-fA-F0-9-]{36})\n                    '
    _module = 'haruhi_dl.extractor.wsj'


class WSJArticleIE(LazyLoadExtractor):
    _VALID_URL = '(?i)https?://(?:www\\.)?wsj\\.com/articles/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.wsj'


class WWEBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.wwe'


class WWEIE(WWEBaseIE):
    _VALID_URL = 'https?://(?:[^/]+\\.)?wwe\\.com/(?:[^/]+/)*videos/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.wwe'


class WykopIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?wykop\\.pl/(?P<type>link|wpis)/(?P<id>\\d+)(?:/comment/\\d+|/[^#/\\s]+|/#comment-(?P<comment_id>\\d+))*'
    _module = 'haruhi_dl.extractor.wykop'


class XBefIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?xbef\\.com/video/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.xbef'


class XboxClipsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?xboxclips\\.com/(?:video\\.php\\?.*vid=|[^/]+/)(?P<id>[\\w-]{36})'
    _module = 'haruhi_dl.extractor.xboxclips'


class XFileShareIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?P<host>clipwatching\\.com|gounlimited\\.to|govid\\.me|holavid\\.com|streamty\\.com|thevideobee\\.to|uqload\\.com|vidbom\\.com|vidlo\\.us|vidlocker\\.xyz|vidshare\\.tv|vup\\.to|xvideosharing\\.com)/(?:embed-)?(?P<id>[0-9a-zA-Z]+)'
    _module = 'haruhi_dl.extractor.xfileshare'


class XHamsterIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/\n                        (?:\n                            movies/(?P<id>[\\dA-Za-z]+)/(?P<display_id>[^/]*)\\.html|\n                            videos/(?P<display_id_2>[^/]*)-(?P<id_2>[\\dA-Za-z]+)\n                        )\n                    '
    _module = 'haruhi_dl.extractor.xhamster'


class XHamsterEmbedIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/xembed\\.php\\?video=(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.xhamster'


class XHamsterUserIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?(?:xhamster\\.(?:com|one|desi)|xhms\\.pro|xhamster\\d+\\.com)/users/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.xhamster'


class XiamiBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.xiami'


class XiamiSongIE(XiamiBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/song/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.xiami'


class XiamiPlaylistBaseIE(XiamiBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.xiami'


class XiamiAlbumIE(XiamiPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/album/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.xiami'


class XiamiArtistIE(XiamiPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/artist/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.xiami'


class XiamiCollectionIE(XiamiPlaylistBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?xiami\\.com/collect/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.xiami'


class XimalayaBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.ximalaya'


class XimalayaIE(XimalayaBaseIE):
    _VALID_URL = 'https?://(?:www\\.|m\\.)?ximalaya\\.com/(?P<uid>[0-9]+)/sound/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.ximalaya'


class XimalayaAlbumIE(XimalayaBaseIE):
    _VALID_URL = 'https?://(?:www\\.|m\\.)?ximalaya\\.com/(?P<uid>[0-9]+)/album/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.ximalaya'


class XMinusIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?x-minus\\.org/track/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.xminus'


class XLinkIE(LazyLoadExtractor):
    _VALID_URL = 'https?://get\\.x-link\\.pl/(?:[a-f\\d]{8}-(?:[a-f\\d]{4}-){3}[a-f\\d]{12}),(?P<id>[a-f\\d]{8}-(?:[a-f\\d]{4}-){3}[a-f\\d]{12}),embed\\.html'
    _module = 'haruhi_dl.extractor.xnews'


class XNXXIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:video|www)\\.xnxx\\.com/video-?(?P<id>[0-9a-z]+)/'
    _module = 'haruhi_dl.extractor.xnxx'


class XstreamIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    (?:\n                        xstream:|\n                        https?://frontend\\.xstream\\.(?:dk|net)/\n                    )\n                    (?P<partner_id>[^/]+)\n                    (?:\n                        :|\n                        /feed/video/\\?.*?\\bid=\n                    )\n                    (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.xstream'


class VGTVIE(XstreamIE):
    _VALID_URL = '(?x)\n                    (?:https?://(?:www\\.)?\n                    (?P<host>\n                        vgtv.no|bt.no/tv|aftenbladet.no/tv|fvn.no/fvntv|aftenposten.no/webtv|ap.vgtv.no/webtv|tv.aftonbladet.se/abtv|www.aftonbladet.se/tv\n                    )\n                    /?\n                    (?:\n                        (?:\\#!/)?(?:video|live)/|\n                        embed?.*id=|\n                        a(?:rticles)?/\n                    )|\n                    (?P<appname>\n                        vgtv|bttv|satv|fvntv|aptv|abtv\n                    ):)\n                    (?P<id>\\d+)\n                    '
    _module = 'haruhi_dl.extractor.vgtv'


class XTubeUserIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?xtube\\.com/profile/(?P<id>[^/]+-\\d+)'
    _module = 'haruhi_dl.extractor.xtube'


class XTubeIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                        (?:\n                            xtube:|\n                            https?://(?:www\\.)?xtube\\.com/(?:watch\\.php\\?.*\\bv=|video-watch/(?:embedded/)?(?P<display_id>[^/]+)-)\n                        )\n                        (?P<id>[^/?&#]+)\n                    '
    _module = 'haruhi_dl.extractor.xtube'


class XuiteIE(LazyLoadExtractor):
    _VALID_URL = 'https?://vlog\\.xuite\\.net/(?:play|embed)/(?P<id>(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)'
    _module = 'haruhi_dl.extractor.xuite'


class XVideosIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            (?:[^/]+\\.)?xvideos2?\\.com/video|\n                            (?:www\\.)?xvideos\\.es/video|\n                            flashservice\\.xvideos\\.com/embedframe/|\n                            static-hw\\.xvideos\\.com/swf/xv-player\\.swf\\?.*?\\bid_video=\n                        )\n                        (?P<id>[0-9]+)\n                    '
    _module = 'haruhi_dl.extractor.xvideos'


class XXXYMoviesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?xxxymovies\\.com/videos/(?P<id>\\d+)/(?P<display_id>[^/]+)'
    _module = 'haruhi_dl.extractor.xxxymovies'


class YahooIE(LazyLoadExtractor):
    _VALID_URL = '(?P<url>https?://(?:(?P<country>[a-zA-Z]{2}(?:-[a-zA-Z]{2})?|malaysia)\\.)?(?:[\\da-zA-Z_-]+\\.)?yahoo\\.com/(?:[^/]+/)*(?P<id>[^?&#]*-[0-9]+(?:-[a-z]+)?)\\.html)'
    _module = 'haruhi_dl.extractor.yahoo'


class YahooSearchIE(LazyLoadSearchExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.yahoo'

    @classmethod
    def suitable(cls, url):
        return re.match(cls._make_valid_url(), url) is not None

    @classmethod
    def _make_valid_url(cls):
        return 'yvsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class YahooGyaOPlayerIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:gyao\\.yahoo\\.co\\.jp/(?:player|episode/[^/]+)|streaming\\.yahoo\\.co\\.jp/c/y)/(?P<id>\\d+/v\\d+/v\\d+|[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.yahoo'


class YahooGyaOIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:gyao\\.yahoo\\.co\\.jp/(?:p|title(?:/[^/]+)?)|streaming\\.yahoo\\.co\\.jp/p/y)/(?P<id>\\d+/v\\d+|[\\da-f]{8}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{4}-[\\da-f]{12})'
    _module = 'haruhi_dl.extractor.yahoo'


class YahooJapanNewsIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?P<host>(?:news|headlines)\\.yahoo\\.co\\.jp)[^\\d]*(?P<id>\\d[\\d-]*\\d)?'
    _module = 'haruhi_dl.extractor.yahoo'


class YandexDiskIE(LazyLoadExtractor):
    _VALID_URL = 'https?://yadi\\.sk/[di]/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.yandexdisk'


class YandexMusicBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.yandexmusic'


class YandexMusicTrackIE(YandexMusicBaseIE):
    _VALID_URL = 'https?://music\\.yandex\\.(?:ru|kz|ua|by)/album/(?P<album_id>\\d+)/track/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.yandexmusic'


class YandexMusicPlaylistBaseIE(YandexMusicBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.yandexmusic'


class YandexMusicAlbumIE(YandexMusicPlaylistBaseIE):
    _VALID_URL = 'https?://music\\.yandex\\.(?:ru|kz|ua|by)/album/(?P<id>\\d+)/?(\\?|$)'
    _module = 'haruhi_dl.extractor.yandexmusic'


class YandexMusicPlaylistIE(YandexMusicPlaylistBaseIE):
    _VALID_URL = 'https?://music\\.yandex\\.(?P<tld>ru|kz|ua|by)/users/(?P<user>[^/]+)/playlists/(?P<id>\\d+)'
    _module = 'haruhi_dl.extractor.yandexmusic'


class YandexVideoIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:\n                            yandex\\.ru(?:/portal/(?:video|efir))?/?\\?.*?stream_id=|\n                            frontend\\.vh\\.yandex\\.ru/player/\n                        )\n                        (?P<id>[\\da-f]+)\n                    '
    _module = 'haruhi_dl.extractor.yandexvideo'


class YapFilesIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:(?:www|api)\\.)?yapfiles\\.ru/get_player/*\\?.*?\\bv=(?P<id>\\w+)'
    _module = 'haruhi_dl.extractor.yapfiles'


class YesJapanIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?yesjapan\\.com/video/(?P<slug>[A-Za-z0-9\\-]*)_(?P<id>[A-Za-z0-9]+)\\.html'
    _module = 'haruhi_dl.extractor.yesjapan'


class YinYueTaiIE(LazyLoadExtractor):
    _VALID_URL = 'https?://v\\.yinyuetai\\.com/video(?:/h5)?/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.yinyuetai'


class YnetIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:.+?\\.)?ynet\\.co\\.il/(?:.+?/)?0,7340,(?P<id>L(?:-[0-9]+)+),00\\.html'
    _module = 'haruhi_dl.extractor.ynet'


class YouJizzIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:\\w+\\.)?youjizz\\.com/videos/(?:[^/#?]*-(?P<id>\\d+)\\.html|embed/(?P<embed_id>\\d+))'
    _module = 'haruhi_dl.extractor.youjizz'


class YoukuIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        (?:\n            https?://(\n                (?:v|player)\\.youku\\.com/(?:v_show/id_|player\\.php/sid/)|\n                video\\.tudou\\.com/v/)|\n            youku:)\n        (?P<id>[A-Za-z0-9]+)(?:\\.html|/v\\.swf|)\n    '
    _module = 'haruhi_dl.extractor.youku'


class YoukuShowIE(LazyLoadExtractor):
    _VALID_URL = 'https?://list\\.youku\\.com/show/id_(?P<id>[0-9a-z]+)\\.html'
    _module = 'haruhi_dl.extractor.youku'


class YouNowLiveIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.younow'

    @classmethod
    def suitable(cls, url):
        return (False
                if YouNowChannelIE.suitable(url) or YouNowMomentIE.suitable(url)
                else super(YouNowLiveIE, cls).suitable(url))


class YouNowChannelIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/(?P<id>[^/]+)/channel'
    _module = 'haruhi_dl.extractor.younow'


class YouNowMomentIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?younow\\.com/[^/]+/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.younow'

    @classmethod
    def suitable(cls, url):
        return (False
                if YouNowChannelIE.suitable(url)
                else super(YouNowMomentIE, cls).suitable(url))


class YouPornIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?youporn\\.com/(?:watch|embed)/(?P<id>\\d+)(?:/(?P<display_id>[^/?#&]+))?'
    _module = 'haruhi_dl.extractor.youporn'


class YourPornIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?sxyprn\\.com/post/(?P<id>[^/?#&.]+)'
    _module = 'haruhi_dl.extractor.yourporn'


class YourUploadIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?(?:yourupload\\.com/(?:watch|embed)|embed\\.yourupload\\.com)/(?P<id>[A-Za-z0-9]+)'
    _module = 'haruhi_dl.extractor.yourupload'


class YoutubeBaseInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeIE(YoutubeBaseInfoExtractor):
    _VALID_URL = '(?x)^\n                     (\n                         (?:https?://|//)                                    # http(s):// or protocol-independent URL\n                         (?:(?:(?:(?:\\w+\\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie|kids)?\\.com/|\n                            (?:www\\.)?deturl\\.com/www\\.youtube\\.com/|\n                            (?:www\\.)?pwnyoutube\\.com/|\n                            (?:www\\.)?hooktube\\.com/|\n                            (?:www\\.)?yourepeat\\.com/|\n                            tube\\.majestyc\\.net/|\n                            # Invidious instances taken from https://github.com/omarroth/invidious/wiki/Invidious-Instances\n                            (?:(?:www|dev)\\.)?invidio\\.us/|\n                            (?:(?:www|no)\\.)?invidiou\\.sh/|\n                            (?:(?:www|fi|de)\\.)?invidious\\.snopyta\\.org/|\n                            (?:www\\.)?invidious\\.kabi\\.tk/|\n                            (?:www\\.)?invidious\\.13ad\\.de/|\n                            (?:www\\.)?invidious\\.mastodon\\.host/|\n                            (?:www\\.)?invidious\\.nixnet\\.xyz/|\n                            (?:www\\.)?invidious\\.drycat\\.fr/|\n                            (?:www\\.)?tube\\.poal\\.co/|\n                            (?:www\\.)?vid\\.wxzm\\.sx/|\n                            (?:www\\.)?yewtu\\.be/|\n                            (?:www\\.)?yt\\.elukerio\\.org/|\n                            (?:www\\.)?yt\\.lelux\\.fi/|\n                            (?:www\\.)?invidious\\.ggc-project\\.de/|\n                            (?:www\\.)?yt\\.maisputain\\.ovh/|\n                            (?:www\\.)?invidious\\.13ad\\.de/|\n                            (?:www\\.)?invidious\\.toot\\.koeln/|\n                            (?:www\\.)?invidious\\.fdn\\.fr/|\n                            (?:www\\.)?watch\\.nettohikari\\.com/|\n                            (?:www\\.)?kgg2m7yk5aybusll\\.onion/|\n                            (?:www\\.)?qklhadlycap4cnod\\.onion/|\n                            (?:www\\.)?axqzx4s6s54s32yentfqojs3x5i7faxza6xo3ehd4bzzsg2ii4fv2iid\\.onion/|\n                            (?:www\\.)?c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid\\.onion/|\n                            (?:www\\.)?fz253lmuao3strwbfbmx46yu7acac2jz27iwtorgmbqlkurlclmancad\\.onion/|\n                            (?:www\\.)?invidious\\.l4qlywnpwqsluw65ts7md3khrivpirse744un3x7mlskqauz5pyuzgqd\\.onion/|\n                            (?:www\\.)?owxfohz4kjyv25fvlqilyxast7inivgiktls3th44jhk3ej3i7ya\\.b32\\.i2p/|\n                            (?:www\\.)?4l2dgddgsrkf2ous66i6seeyi6etzfgrue332grh2n7madpwopotugyd\\.onion/|\n                            youtube\\.googleapis\\.com/)                        # the various hostnames, with wildcard subdomains\n                         (?:.*?\\#/)?                                          # handle anchor (#/) redirect urls\n                         (?:                                                  # the various things that can precede the ID:\n                             (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/\n                             |(?:                                             # or the v= param in all its forms\n                                 (?:(?:watch|movie)(?:_popup)?(?:\\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)\n                                 (?:\\?|\\#!?)                                  # the params delimiter ? or # or #!\n                                 (?:.*?[&;])??                                # any other preceding param (like /?s=tuff&v=xxxx or ?s=tuff&amp;v=V36LpHqtcDY)\n                                 v=\n                             )\n                         ))\n                         |(?:\n                            youtu\\.be|                                        # just youtu.be/xxxx\n                            (?:www\\.)?youtube\\.com/(?:\n                                shorts|                                       # or youtube.com/shorts/xxx\n                                video                                         # or youtube.com/video/xxx\n                            )|\n                            vid\\.plus|                                        # or vid.plus/xxxx\n                            zwearz\\.com/watch|                                # or zwearz.com/watch/xxxx\n                         )/\n                         |(?:www\\.)?cleanvideosearch\\.com/media/action/yt/watch\\?videoId=\n                         )\n                     )?                                                       # all until now is optional -> you can pass the naked ID\n                     ([0-9A-Za-z_-]{11})                                      # here is it! the YouTube video ID\n                     (?!.*?\\blist=\n                        (?:\n                            (?:LL|WL|(?:PL|EC|UU|FL|RD|UL|TL|PU|OLAK5uy_)[0-9A-Za-z-_]{10,})|                                  # combined list/video URLs are handled by the playlist IE\n                            WL                                                # WL are handled by the watch later IE\n                        )\n                     )\n                     (?(1).+)?                                                # if we found the ID, everything can follow\n                     $'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeBaseListInfoExtractor(YoutubeBaseInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeAjaxListInfoExtractor(YoutubeBaseListInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeChannelIE(YoutubeAjaxListInfoExtractor):
    _VALID_URL = 'https?://(?:www\\.|music\\.)?youtube\\.com/(?P<type>user|channel|c)/(?P<id>[\\w-]+)(?!/live)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeYti1ListInfoExtractor(YoutubeBaseListInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeHistoryIE(YoutubeYti1ListInfoExtractor):
    _VALID_URL = '(?:https?://(?:www\\.)?youtube\\.com/feed/|:yt)(?P<id>history)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeLikedIE(LazyLoadExtractor):
    _VALID_URL = ':yt(?:fav(?:ourites)?|liked)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeMusicAlbumIE(YoutubeBaseListInfoExtractor):
    _VALID_URL = 'https://music\\.youtube\\.com/browse/(?P<id>MPREb_\\w{11})'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubePlaylistIE(YoutubeYti1ListInfoExtractor):
    _VALID_URL = '(?:https?://(?:www\\.|music\\.)?youtube\\.com/(?:playlist\\?(?:[^&;]+[&;])*|watch\\?(?:[^&;]+[&;])*)list=|ytplaylist:)?(?P<id>(?:LL|WL|(?:PL|EC|UU|FL|RD|UL|TL|PU|OLAK5uy_)[0-9A-Za-z-_]{10,}))'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeSearchIE(LazyLoadSearchExtractor, YoutubeYti1ListInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'

    @classmethod
    def suitable(cls, url):
        return re.match(cls._make_valid_url(), url) is not None

    @classmethod
    def _make_valid_url(cls):
        return 'ytsearch(?P<prefix>|[1-9][0-9]*|all):(?P<query>[\\s\\S]+)'


class YoutubeBaseShelfInfoExtractor(YoutubeYti1ListInfoExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeSubscriptionsIE(YoutubeBaseShelfInfoExtractor):
    _VALID_URL = '(?:https?://(?:www\\.)?youtube\\.com/feed/|:yt)(?P<id>subs(?:criptions)?)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeWatchLaterIE(LazyLoadExtractor):
    _VALID_URL = ':ytw(?:atchlater|l)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeTopicChannelWorkaroundIE(YoutubeBaseListInfoExtractor):
    _VALID_URL = 'youtube_topic_channel_workaround:(?P<id>.+)'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeTruncatedIDIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?youtube\\.com/watch\\?v=(?P<id>[0-9A-Za-z_-]{1,10})$'
    _module = 'haruhi_dl.extractor.youtube'


class YoutubeTruncatedURLIE(LazyLoadExtractor):
    _VALID_URL = '(?x)\n        (?:https?://)?\n        (?:\\w+\\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie)?\\.com/\n        (?:watch\\?(?:\n            feature=[a-z_]+|\n            annotation_id=annotation_[^&]+|\n            x-yt-cl=[0-9]+|\n            hl=[^&]*|\n            t=[0-9]+\n        )?\n        |\n            attribution_link\\?a=[^&]+\n        )\n        $\n    '
    _module = 'haruhi_dl.extractor.youtube'


class ZapiksIE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?zapiks\\.(?:fr|com)/(?:(?:[a-z]{2}/)?(?P<display_id>.+?)\\.html|index\\.php\\?.*\\bmedia_id=(?P<id>\\d+))'
    _module = 'haruhi_dl.extractor.zapiks'


class Zaq1IE(LazyLoadExtractor):
    _VALID_URL = 'https?://(?:www\\.)?zaq1\\.pl/video/(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.zaq1'


class ZattooPlatformBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.zattoo'


class QuicklineBaseIE(ZattooPlatformBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.zattoo'


class QuicklineIE(QuicklineBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?mobiltv\\.quickline\\.com/watch/(?P<channel>[^/]+)/(?P<id>[0-9]+)'
    _module = 'haruhi_dl.extractor.zattoo'


class QuicklineLiveIE(QuicklineBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?mobiltv\\.quickline\\.com/watch/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.zattoo'

    @classmethod
    def suitable(cls, url):
        return False if QuicklineIE.suitable(url) else super(QuicklineLiveIE, cls).suitable(url)


class ZattooBaseIE(ZattooPlatformBaseIE):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.zattoo'


class ZattooIE(ZattooBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?zattoo\\.com/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class BBVTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?bbv\\-tv\\.net/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class EinsUndEinsTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?1und1\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class EWETVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?tvonline\\.ewe\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class GlattvisionTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?iptv\\.glattvision\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class MNetTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?tvplus\\.m\\-net\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class MyVisionTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?myvisiontv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class NetPlusIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?netplus\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class OsnatelTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?tvonline\\.osnatel\\.de/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class QuantumTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?quantum\\-tv\\.com/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class SaltTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?tv\\.salt\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class SAKTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?saktv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class VTXTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?vtxtv\\.ch/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class WalyTVIE(ZattooIE):
    _VALID_URL = 'https?://(?:www\\.)?player\\.waly\\.tv/watch/(?P<channel>[^/]+?)/(?P<id>[0-9]+)[^/]+(?:/(?P<recid>[0-9]+))?'
    _module = 'haruhi_dl.extractor.zattoo'


class ZattooLiveIE(ZattooBaseIE):
    _VALID_URL = 'https?://(?:www\\.)?zattoo\\.com/watch/(?P<id>[^/]+)'
    _module = 'haruhi_dl.extractor.zattoo'

    @classmethod
    def suitable(cls, url):
        return False if ZattooIE.suitable(url) else super(ZattooLiveIE, cls).suitable(url)


class ZDFBaseIE(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.zdf'


class ZDFIE(ZDFBaseIE):
    _VALID_URL = 'https?://www\\.zdf\\.de/(?:[^/]+/)*(?P<id>[^/?]+)\\.html'
    _module = 'haruhi_dl.extractor.zdf'


class ZDFChannelIE(ZDFBaseIE):
    _VALID_URL = 'https?://www\\.zdf\\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _module = 'haruhi_dl.extractor.zdf'

    @classmethod
    def suitable(cls, url):
        return False if ZDFIE.suitable(url) else super(ZDFChannelIE, cls).suitable(url)


class ZingMp3BaseInfoExtractor(LazyLoadExtractor):
    _VALID_URL = None
    _module = 'haruhi_dl.extractor.zingmp3'


class ZingMp3IE(ZingMp3BaseInfoExtractor):
    _VALID_URL = 'https?://mp3\\.zing\\.vn/(?:bai-hat|album|playlist|video-clip)/[^/]+/(?P<id>\\w+)\\.html'
    _module = 'haruhi_dl.extractor.zingmp3'


class ZypeIE(LazyLoadExtractor):
    _VALID_URL = 'https?://player\\.zype\\.com/embed/(?P<id>[\\da-fA-F]+)\\.(?:js|json|html)\\?.*?(?:access_token|(?:ap[ip]|player)_key)=[^&]+'
    _module = 'haruhi_dl.extractor.zype'


class GenericIE(LazyLoadExtractor):
    _VALID_URL = '.*'
    _module = 'haruhi_dl.extractor.generic'


_ALL_CLASSES = [ABCIE, ABCIViewIE, AbcNewsIE, AbcNewsVideoIE, ABCOTVSIE, ABCOTVSClipsIE, AcademicEarthCourseIE, ACastIE, ACastChannelIE, ADNIE, AdobeConnectIE, AdobeTVEmbedIE, AdobeTVIE, AdobeTVShowIE, AdobeTVChannelIE, AdobeTVVideoIE, AdultSwimIE, AfreecaTVIE, TokFMAuditionIE, TokFMPodcastIE, WyborczaPodcastIE, WyborczaVideoIE, AirMozillaIE, AlbiclaIE, AlJazeeraIE, AlphaPornoIE, AmericasTestKitchenIE, AnimeOnDemandIE, AnvatoIE, AolIE, AllocineIE, AliExpressLiveIE, AliExpressProductIE, APAIE, AparatIE, AppleConnectIE, AppleTrailersIE, AppleTrailersSectionIE, ArchiveOrgIE, ArkenaIE, ARDBetaMediathekIE, ARDIE, ARDMediathekIE, ArteTVPlus7IE, ArteTVEmbedIE, ArteTVPlaylistIE, AsianCrushIE, AsianCrushPlaylistIE, AtresPlayerIE, ATTTechChannelIE, ATVAtIE, AudiMediaIE, AudioBoomIE, AudiomackIE, AudiomackAlbumIE, AWAANIE, AWAANVideoIE, AWAANLiveIE, AWAANSeasonIE, AZMedienIE, BaiduVideoIE, BandcampIE, BandcampAlbumIE, BandcampWeeklyIE, BBCCoUkIE, BBCCoUkArticleIE, BBCCoUkIPlayerPlaylistIE, BBCCoUkPlaylistIE, BBCIE, BeamProLiveIE, BeamProVodIE, BeegIE, BehindKinkIE, BellMediaIE, BeatportIE, BetIE, BFIPlayerIE, BigflixIE, BildIE, BiliBiliIE, BiliBiliBangumiIE, BilibiliAudioIE, BilibiliAudioAlbumIE, BiliBiliPlayerIE, BioBioChileTVIE, BitChuteIE, BitChuteChannelIE, BIQLEIE, BleacherReportIE, BleacherReportCMSIE, BlinkxIE, BloombergIE, BokeCCIE, BostonGlobeIE, BpbIE, BRIE, BRMediathekIE, BravoTVIE, BreakIE, BrightcoveLegacyIE, BrightcoveNewIE, BusinessInsiderIE, BuzzFeedIE, BYUtvIE, C56IE, CamdemyIE, CamdemyFolderIE, CamModelsIE, CamTubeIE, CamWithHerIE, CanalplusIE, Canalc2IE, CanvasIE, CanvasEenIE, VrtNUIE, CarambaTVIE, CarambaTVPageIE, CartoonNetworkIE, CBCIE, CBCPlayerIE, CBCWatchVideoIE, CBCWatchIE, CBCOlympicsIE, CBSLocalIE, CBSNewsLiveVideoIE, CCCIE, CCCPlaylistIE, CCMAIE, CCTVIE, CDAIE, CeskaTelevizeIE, CeskaTelevizePoradyIE, Channel9IE, CharlieRoseIE, ChaturbateIE, ChilloutzoneIE, ChirbitIE, ChirbitProfileIE, CinchcastIE, CinemaxIE, CiscoLiveSessionIE, CiscoLiveSearchIE, CJSWIE, CliphunterIE, ClippitIE, ClipRsIE, ClipsyndicateIE, CloserToTruthIE, CloudflareStreamIE, CloudyIE, ClubicIE, ClypIE, CNBCIE, CNBCVideoIE, CNNIE, CNNBlogsIE, CNNArticleIE, CoubIE, ComedyCentralFullEpisodesIE, ComedyCentralIE, ComedyCentralShortnameIE, ComedyCentralTVIE, ToshIE, CommonMistakesIE, UnicodeBOMIE, MmsIE, RtmpIE, CondeNastIE, CONtvIE, CrackedIE, CrackleIE, CrooksAndLiarsIE, CrunchyrollShowPlaylistIE, CSpanIE, CtsNewsIE, CTVNewsIE, CultureUnpluggedIE, CuriosityStreamIE, CuriosityStreamCollectionIE, CWTVIE, DailyMailIE, DailymotionIE, DailymotionPlaylistIE, DailymotionUserIE, DaumIE, DaumClipIE, DaumPlaylistIE, DaumUserIE, DBTVIE, DctpTvIE, DeezerPlaylistIE, DemocracynowIE, DFBIE, DHMIE, DiggIE, DotsubIE, DouyuShowIE, DouyuTVIE, DPlayIE, DreiSatIE, DRBonanzaIE, DrTuberIE, DRTVIE, DRTVLiveIE, DTubeIE, DVTVIE, DumpertIE, DefenseGouvFrIE, DiscoveryIE, DiscoveryGoIE, DiscoveryGoPlaylistIE, DiscoveryNetworksDeIE, DiscoveryVRIE, DisneyIE, DigitallySpeakingIE, DropboxIE, DWIE, DWArticleIE, EaglePlatformIE, EbaumsWorldIE, EchoMskIE, EggheadCourseIE, EggheadLessonIE, EHowIE, EightTracksIE, EinthusanIE, EitbIE, EllenTubeIE, EllenTubeVideoIE, EllenTubePlaylistIE, ElPaisIE, EmbedlyIE, EngadgetIE, EpornerIE, EroProfileIE, EscapistIE, EskaGoIE, ESPNIE, ESPNArticleIE, FiveThirtyEightIE, EsriVideoIE, EuropaIE, EurozetArticleIE, EurozetPlayerStreamIE, EurozetPlayerPodcastIE, EurozetPlayerMusicStreamIE, EveryonesMixtapeIE, ExpoTVIE, ExpressenIE, EyedoTVIE, FacebookIE, FacebookPluginsVideoIE, FazIE, FC2IE, FC2EmbedIE, FczenitIE, FilmOnIE, FilmOnChannelIE, FilmwebIE, FirstTVIE, FiveMinIE, FiveTVIE, FlickrIE, FolketingetIE, FootyRoomIE, Formula1IE, FourTubeIE, PornTubeIE, PornerBrosIE, FuxIE, FOXIE, FOX9IE, FOX9NewsIE, FoxgayIE, FoxNewsIE, FoxNewsArticleIE, FoxSportsIE, FranceCultureIE, FranceInterIE, FranceTVIE, FranceTVSiteIE, FranceTVEmbedIE, FranceTVInfoIE, FranceTVInfoSportIE, FranceTVJeunesseIE, GenerationWhatIE, CultureboxIE, FreesoundIE, FreespeechIE, FreshLiveIE, FrontendMastersIE, FrontendMastersLessonIE, FrontendMastersCourseIE, FunimationIE, FunkIE, FunkwhaleAlbumSHIE, FunkwhaleArtistSHIE, FunkwhaleChannelSHIE, FunkwhalePlaylistSHIE, FunkwhaleTrackSHIE, FunkwhaleRadioSHIE, FusionIE, FXNetworksIE, GaiaIE, GameInformerIE, GameSpotIE, GameStarIE, GaskrankIE, GazetaIE, GDCVaultIE, GfycatIE, GiantBombIE, GigaIE, GlideIE, GloboIE, GloboArticleIE, GoIE, GodTubeIE, GolemIE, GoogleDriveIE, GooglePlusIE, GoogleSearchIE, GoshgayIE, GPUTechConfIE, GrouponIE, GtvIE, GuardianAudioIE, GuardianVideoIE, HBOIE, HearThisAtIE, HeiseIE, HellPornoIE, HelsinkiIE, HentaiStigmaIE, HGTVComShowIE, HKETVIE, HiDiveIE, HistoricFilmsIE, HitboxIE, HitboxLiveIE, HitRecordIE, HornBunnyIE, HotNewHipHopIE, HotStarIE, HotStarPlaylistIE, HowcastIE, HowStuffWorksIE, HRTiIE, HRTiPlaylistIE, HuajiaoIE, HuffPostIE, HungamaIE, HungamaSongIE, HypemIE, IGNIE, OneUPIE, PCMagIE, ImdbIE, ImdbListIE, ImgurIE, ImgurGalleryIE, ImgurAlbumIE, InaIE, IncIE, IndavideoEmbedIE, InfoQIE, InstagramIE, InstagramUserIE, InstagramTagIE, InternazionaleIE, InternetVideoArchiveIE, IplaIE, IPrimaIE, IqiyiIE, Ir90TvIE, ITVIE, ITVBTCCIE, IviIE, IviCompilationIE, IvideonIE, IwaraIE, IzleseneIE, JamendoIE, JamendoAlbumIE, JeuxVideoIE, JoveIE, JojIE, JWPlatformIE, KakaoIE, KalturaIE, KanalPlayIE, KankanIE, KaraoketvIE, KarriereVideosIE, KeezMoviesIE, ExtremeTubeIE, KetnetIE, KhanAcademyIE, KickStarterIE, KinjaEmbedIE, KinoPoiskIE, KonserthusetPlayIE, KrasViewIE, Ku6IE, KUSIIE, KuwoIE, KuwoAlbumIE, KuwoChartIE, KuwoSingerIE, KuwoCategoryIE, KuwoMvIE, LA7IE, Laola1TvEmbedIE, Laola1TvIE, EHFTVIE, ITTFIE, LBRYIE, LCIIE, LcpPlayIE, LcpIE, Lecture2GoIE, LecturioIE, LecturioCourseIE, LecturioDeCourseIE, LeIE, LePlaylistIE, LetvCloudIE, LEGOIE, LemondeIE, LentaIE, LibraryOfCongressIE, LibsynIE, LifeNewsIE, LifeEmbedIE, LimelightMediaIE, LimelightChannelIE, LimelightChannelListIE, LineTVIE, LinkedInPostIE, LinkedInLearningIE, LinkedInLearningCourseIE, LinuxAcademyIE, LiTVIE, LiveJournalIE, LiveLeakIE, LiveLeakEmbedIE, LivestreamIE, LivestreamOriginalIE, LivestreamShortenerIE, LnkGoIE, LocalNews8IE, LoveHomePornIE, LRTIE, LurkerIE, LyndaIE, LyndaCourseIE, M6IE, MailRuIE, MailRuMusicIE, MailRuMusicSearchIE, MallTVIE, MangomoloVideoIE, MangomoloLiveIE, ManyVidsIE, MarkizaIE, MarkizaPageIE, MastodonSHIE, MassengeschmackTVIE, MatchTVIE, MDRIE, MediasetIE, MediasiteIE, MediasiteCatalogIE, MediasiteNamedCatalogIE, MediciIE, MegaphoneIE, MeipaiIE, MelonVODIE, METAIE, MetacafeIE, MetacriticIE, MgoonIE, MGTVIE, MiaoPaiIE, MicrosoftVirtualAcademyIE, MicrosoftVirtualAcademyCourseIE, MinistryGridIE, MinotoIE, MioMioIE, TechTVMITIE, OCWMITIE, MiTeleIE, MixcloudIE, MixcloudUserIE, MixcloudPlaylistIE, MLBIE, MnetIE, MoeVideoIE, MofosexIE, MofosexEmbedIE, MojvideoIE, MorningstarIE, MotherlessIE, MotherlessGroupIE, MotorsportIE, MovieClipsIE, MoviezineIE, MovingImageIE, MSNIE, MTVIE, CMTIE, MTVVideoIE, MTVServicesEmbeddedIE, MTVDEIE, MTVJapanIE, MuenchenTVIE, MwaveIE, MwaveMeetGreetIE, MyChannelsIE, MySpaceIE, MySpaceAlbumIE, MySpassIE, MyviIE, MyviEmbedIE, MyVidsterIE, NationalGeographicVideoIE, NationalGeographicTVIE, NaverIE, NBAIE, CSNNEIE, NBCIE, NBCOlympicsIE, NBCOlympicsStreamIE, NBCSportsIE, NBCSportsStreamIE, NBCSportsVPlayerIE, NDRIE, NJoyIE, NDREmbedBaseIE, NDREmbedIE, NJoyEmbedIE, NDTVIE, NetzkinoIE, NerdCubedFeedIE, NetEaseMusicIE, NetEaseMusicAlbumIE, NetEaseMusicSingerIE, NetEaseMusicListIE, NetEaseMusicMvIE, NetEaseMusicProgramIE, NetEaseMusicDjRadioIE, NewgroundsIE, NewgroundsPlaylistIE, NewstubeIE, NextMediaIE, NextMediaActionNewsIE, AppleDailyIE, NextTVIE, NexxIE, NexxEmbedIE, NFLIE, NhkVodIE, NHLIE, NickIE, NickBrIE, NickDeIE, NickNightIE, NickRuIE, NiconicoIE, NiconicoPlaylistIE, NinatekaIE, NineCNineMediaIE, NineGagIE, NineNowIE, NintendoIE, NJPWWorldIE, NobelPrizeIE, NocoIE, NonkTubeIE, NoovoIE, NormalbootsIE, NosVideoIE, NovaEmbedIE, NovaIE, NownessIE, NownessPlaylistIE, NownessSeriesIE, NozIE, NPOIE, AndereTijdenIE, NPOLiveIE, NPORadioIE, NPORadioFragmentIE, SchoolTVIE, HetKlokhuisIE, VPROIE, WNLIE, NprIE, NRKIE, NRKPlaylistIE, NRKSkoleIE, NRKTVIE, NRKTVDirekteIE, NRKTVEpisodeIE, NRKTVEpisodesIE, NRKTVSeasonIE, NRKTVSeriesIE, NRLTVIE, NTVCoJpCUIE, NTVDeIE, NTVRuIE, NYTimesIE, NYTimesArticleIE, NuvidIE, NZZIE, OdaTVIE, OdnoklassnikiIE, OKOPressIE, OktoberfestTVIE, OnDemandKoreaIE, OnetPlIE, OnionStudiosIE, OnNetworkLoaderIE, OnNetworkFrameIE, OoyalaIE, OoyalaExternalIE, OpenFMIE, OraTVIE, ORFTVthekIE, ORFFM4IE, ORFFM4StoryIE, ORFOE1IE, ORFOE3IE, ORFNOEIE, ORFWIEIE, ORFBGLIE, ORFOOEIE, ORFSTMIE, ORFKTNIE, ORFSBGIE, ORFTIRIE, ORFVBGIE, ORFIPTVIE, OutsideTVIE, PacktPubIE, PacktPubCourseIE, PandoraTVIE, ParliamentLiveUKIE, PatreonIE, PBSIE, PearVideoIE, PeerTubeSHIE, PeopleIE, PerformGroupIE, PeriscopeIE, PeriscopeUserIE, PhilharmonieDeParisIE, PhoenixIE, PhotobucketIE, PicartoIE, PicartoVodIE, PikselIE, PinkbikeIE, PladformIE, PlatziIE, PlatziCourseIE, PlayFMIE, PlayPlusTVIE, PlaysTVIE, PlaytvakIE, PlayvidIE, PlaywireIE, PluralsightIE, PluralsightCourseIE, PodomaticIE, PokemonIE, PolskieRadioIE, PolskieRadioCategoryIE, PolskieRadioPlayerIE, PopcorntimesIE, PopcornTVIE, Porn91IE, PornComIE, PornHdIE, PornHubIE, PornHubUserIE, PornHubPagedVideoListIE, PornHubUserVideosUploadIE, PornotubeIE, PornoVoisinesIE, PornoXOIE, PuhuTVIE, PuhuTVSerieIE, PulsEmbedIE, PulseVideoIE, PressTVIE, ProSiebenSat1IE, Puls4IE, PyvideoIE, QQMusicIE, QQMusicSingerIE, QQMusicAlbumIE, QQMusicToplistIE, QQMusicPlaylistIE, R7IE, R7ArticleIE, RadioCanadaIE, RadioCanadaAudioVideoIE, RadioDeIE, RadioJavanIE, RadioBremenIE, RadioFranceIE, RaiPlayIE, RaiPlayLiveIE, RaiPlayPlaylistIE, RaiIE, RayWenderlichIE, RayWenderlichCourseIE, RBMARadioIE, RDSIE, RedBullTVIE, RedBullEmbedIE, RedBullTVRrnContentIE, RedBullIE, RedditIE, RedditRIE, RedTubeIE, RegioTVIE, RENTVIE, RENTVArticleIE, RestudyIE, ReutersIE, ReverbNationIE, RICEIE, RMCDecouverteIE, RMFonPodcastsIE, RMFonStreamIE, RMF24IE, Ro220IE, RockstarGamesIE, RoosterTeethIE, RottenTomatoesIE, RoxwelIE, RozhlasIE, RTBFIE, RteIE, RteRadioIE, RtlNlIE, RTL2IE, RTL2YouIE, RTL2YouSeriesIE, RTPIE, RTVEALaCartaIE, RTVELiveIE, RTVEInfantilIE, RTVETelevisionIE, RTVNHIE, RTVSIE, RUHDIE, RutubeIE, RutubeChannelIE, RutubeEmbedIE, RutubeMovieIE, RutubePersonIE, RutubePlaylistIE, RUTVIE, RuutuIE, RuvIE, SafariIE, SafariApiIE, SafariCourseIE, SapoIE, SaveFromIE, SBSIE, ScreencastIE, ScreencastOMaticIE, ScrippsNetworksWatchIE, ScrippsNetworksIE, SCTEIE, SCTECourseIE, SeekerIE, SenateISVPIE, SendtoNewsIE, ServusIE, SevenPlusIE, SexuIE, SeznamZpravyIE, SeznamZpravyArticleIE, ShahidIE, ShahidShowIE, SharedIE, VivoIE, ShowRoomLiveIE, SinaIE, SixPlayIE, SkylineWebcamsIE, SkyNewsArabiaIE, SkyNewsArabiaArticleIE, SkyNewsIE, SkySportsIE, SlideshareIE, SlidesLiveIE, SlutloadIE, SmotriIE, SmotriCommunityIE, SmotriUserIE, SmotriBroadcastIE, SnotrIE, SohuIE, SonyLIVIE, SoundcloudEmbedIE, SoundcloudIE, SoundcloudSetIE, SoundcloudUserIE, SoundcloudTrackStationIE, SoundcloudPlaylistIE, SoundcloudSearchIE, SoundgasmIE, SoundgasmProfileIE, SouthParkIE, SouthParkDeIE, SouthParkDkIE, SouthParkEsIE, SouthParkNlIE, SpankBangIE, SpankBangPlaylistIE, SpankwireIE, SpiegelIE, SpiegelArticleIE, SpiegeltvIE, BellatorIE, ParamountNetworkIE, StitcherIE, Sport5IE, SportBoxIE, SportDeutschlandIE, SpringboardPlatformIE, SproutIE, SRGSSRIE, RTSIE, SRGSSRPlayIE, SRMediathekIE, StanfordOpenClassroomIE, SteamIE, StreamableIE, StreamcloudIE, StreamCZIE, StreetVoiceIE, StretchInternetIE, STVPlayerIE, SunPornoIE, SverigesRadioEpisodeIE, SverigesRadioPublicationIE, SVTIE, SVTPageIE, SVTPlayIE, SVTSeriesIE, SWRMediathekIE, SyfyIE, SztvHuIE, TagesschauPlayerIE, TagesschauIE, TassIE, TastyTradeIE, TBSIE, TDSLifewayIE, TeachableIE, TeachableCourseIE, TeacherTubeIE, TeacherTubeUserIE, TeachingChannelIE, TeamcocoIE, TeamTreeHouseIE, TechTalksIE, TEDIE, Tele5IE, Tele13IE, TeleBruxellesIE, TelecincoIE, TelegraafIE, TeleMBIE, TeleQuebecIE, TeleQuebecSquatIE, TeleQuebecEmissionIE, TeleQuebecLiveIE, TeleTaskIE, TelewebionIE, TennisTVIE, TenPlayIE, TestURLIE, TF1IE, TFOIE, TheInterceptIE, ThePlatformIE, AENetworksIE, HistoryTopicIE, AMCNetworksIE, NBCNewsIE, ThePlatformFeedIE, CBSIE, CBSInteractiveIE, CBSNewsEmbedIE, CBSNewsIE, CBSSportsIE, CorusIE, TheSceneIE, TheStarIE, TheSunIE, TheWeatherChannelIE, ThisAmericanLifeIE, ThisAVIE, ThisOldHouseIE, ThreeQSDNIE, TikTokIE, TikTokUserIE, TinyPicIE, TMZIE, TMZArticleIE, TNAFlixNetworkEmbedIE, TNAFlixIE, EMPFlixIE, MovieFapIE, ToggleIE, TOnlineIE, ToonGogglesIE, TouTvIE, ToypicsUserIE, ToypicsIE, TrailerAddictIE, TriluliluIE, TruNewsIE, TruTVIE, TubaFMIE, TubaFMPageIE, Tube8IE, TubiTvIE, TumblrIE, TuneInClipIE, TuneInStationIE, TuneInProgramIE, TuneInTopicIE, TuneInShortenerIE, TunePkIE, TurboIE, TV2IE, TV2ArticleIE, KatsomoIE, TV2DKIE, TV2DKBornholmPlayIE, TV2HuIE, TV4IE, TV5MondePlusIE, TVAIE, TVANouvellesIE, TVANouvellesArticleIE, TVCIE, TVCArticleIE, TvigleIE, TVLandIE, TVN24IE, TVNPlayerIE, TVNPlayerSeriesIE, TVNetIE, TVNoeIE, TVNowIE, TVNowNewIE, TVNowSeasonIE, TVNowAnnualIE, TVNowShowIE, TVPEmbedIE, TVPIE, TVPStreamIE, TVPWebsiteIE, TVPlayIE, ViafreeIE, TVPlayHomeIE, TVPlayerIE, TweakersIE, TwentyFourVideoIE, TwentyMinutenIE, TwentyThreeVideoIE, TwitCastingIE, TwitchVodIE, TwitchCollectionIE, TwitchVideosIE, TwitchVideosClipsIE, TwitchVideosCollectionsIE, TwitchStreamIE, TwitchClipsIE, TwitterCardIE, TwitterIE, TwitterAmplifyIE, TwitterBroadcastIE, UdemyIE, UdemyCourseIE, UDNEmbedIE, UFCTVIE, UFCArabiaIE, UKTVPlayIE, DigitekaIE, DLiveVODIE, DLiveStreamIE, UMGDeIE, UnistraIE, UnityIE, UOLIE, UplynkIE, UplynkPreplayIE, UrortIE, URPlayIE, USANetworkIE, USATodayIE, UstreamIE, UstreamChannelIE, UstudioIE, UstudioEmbedIE, Varzesh3IE, Vbox7IE, VeeHDIE, VeohIE, VestiIE, VevoIE, VevoPlaylistIE, BTArticleIE, BTVestlendingenIE, VH1IE, ViceIE, ViceArticleIE, ViceShowIE, VidbitIE, ViddlerIE, VideaIE, VideoDetectiveIE, VideofyMeIE, VideomoreIE, VideomoreVideoIE, VideomoreSeasonIE, VideoPressIE, VidioIE, VidLiiIE, VidmeIE, VidmeUserIE, VidmeUserLikesIE, VidziIE, VierIE, VierVideosIE, ViewLiftIE, ViewLiftEmbedIE, ViideaIE, VimeoIE, VimeoAlbumIE, VimeoChannelIE, VimeoGroupsIE, VimeoLikesIE, VimeoOndemandIE, VimeoReviewIE, VimeoUserIE, VimeoWatchLaterIE, VHXEmbedIE, VimpleIE, VineIE, VineUserIE, VikiIE, VikiChannelIE, ViqeoIE, ViuIE, ViuPlaylistIE, ViuOTTIE, VKIE, VKUserVideosIE, VKWallPostIE, VLiveIE, VLiveChannelIE, VLivePlaylistIE, VodlockerIE, VODPlIE, VODPlatformIE, VoiceRepublicIE, VootIE, VoxMediaVolumeIE, VoxMediaIE, VRTIE, VrakIE, VRVIE, CrunchyrollIE, VRVSeriesIE, VShareIE, MedialaanIE, VubeIE, VuClipIE, VVVVIDIE, VyboryMosIE, VzaarIE, WakanimIE, WallaIE, WashingtonPostIE, WashingtonPostArticleIE, WatIE, WatchBoxIE, WatchIndianPornIE, WDRIE, WDRPageIE, WDRElefantIE, WDRMobileIE, WebcasterIE, WebcasterFeedIE, WebOfStoriesIE, WebOfStoriesPlaylistIE, WeiboIE, WeiboMobileIE, WeiqiTVIE, WistiaIE, WorldStarHipHopIE, WpPlIE, WSJIE, WSJArticleIE, WWEIE, WykopIE, XBefIE, XboxClipsIE, XFileShareIE, XHamsterIE, XHamsterEmbedIE, XHamsterUserIE, XiamiSongIE, XiamiAlbumIE, XiamiArtistIE, XiamiCollectionIE, XimalayaIE, XimalayaAlbumIE, XMinusIE, XLinkIE, XNXXIE, XstreamIE, VGTVIE, XTubeUserIE, XTubeIE, XuiteIE, XVideosIE, XXXYMoviesIE, YahooIE, YahooSearchIE, YahooGyaOPlayerIE, YahooGyaOIE, YahooJapanNewsIE, YandexDiskIE, YandexMusicTrackIE, YandexMusicAlbumIE, YandexMusicPlaylistIE, YandexVideoIE, YapFilesIE, YesJapanIE, YinYueTaiIE, YnetIE, YouJizzIE, YoukuIE, YoukuShowIE, YouNowLiveIE, YouNowChannelIE, YouNowMomentIE, YouPornIE, YourPornIE, YourUploadIE, YoutubeIE, YoutubeChannelIE, YoutubeHistoryIE, YoutubeLikedIE, YoutubeMusicAlbumIE, YoutubePlaylistIE, YoutubeSearchIE, YoutubeSubscriptionsIE, YoutubeWatchLaterIE, YoutubeTopicChannelWorkaroundIE, YoutubeTruncatedIDIE, YoutubeTruncatedURLIE, ZapiksIE, Zaq1IE, QuicklineIE, QuicklineLiveIE, ZattooIE, BBVTVIE, EinsUndEinsTVIE, EWETVIE, GlattvisionTVIE, MNetTVIE, MyVisionTVIE, NetPlusIE, OsnatelTVIE, QuantumTVIE, SaltTVIE, SAKTVIE, VTXTVIE, WalyTVIE, ZattooLiveIE, ZDFIE, ZDFChannelIE, ZingMp3IE, ZypeIE, GenericIE]

_SH_CLASSES = [FunkwhaleAlbumSHIE, FunkwhaleArtistSHIE, FunkwhaleChannelSHIE, FunkwhalePlaylistSHIE, FunkwhaleTrackSHIE, FunkwhaleRadioSHIE, MastodonSHIE, PeerTubeSHIE]
