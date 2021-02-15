# -*- coding: utf-8 -*-
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import io
import itertools
import logging
import operator
import os

from babelfish import Language, LanguageReverseError
from guessit import guessit
from rarfile import BadRarFile, NotRarFile, RarCannotExec, RarFile, Error, is_rarfile
from zipfile import BadZipfile

from .extensions import provider_manager, default_providers, refiner_manager
from .score import compute_score as default_compute_score
from .subtitle import SUBTITLE_EXTENSIONS
from .utils import handle_exception
from .video import VIDEO_EXTENSIONS, Episode, Movie, Video

#: Supported archive extensions
ARCHIVE_EXTENSIONS = ('.rar',)

logger = logging.getLogger(__name__)


class ProviderPool(object):
    """A pool of providers with the same API as a single :class:`~subliminal.providers.Provider`.

    It has a few extra features:

        * Lazy loads providers when needed and supports the `with` statement to :meth:`terminate`
          the providers on exit.
        * Automatically discard providers on failure.

    :param list providers: name of providers to use, if not all.
    :param dict provider_configs: provider configuration as keyword arguments per provider name to pass when
        instantiating the :class:`~subliminal.providers.Provider`.

    """
    def __init__(self, providers=None, provider_configs=None):
        #: Name of providers to use
        self.providers = providers or default_providers

        #: Provider configuration
        self.provider_configs = provider_configs or {}

        #: Initialized providers
        self.initialized_providers = {}

        #: Discarded providers
        self.discarded_providers = set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.terminate()

    def __getitem__(self, name):
        if name not in self.providers:
            raise KeyError
        if name not in self.initialized_providers:
            logger.info('Initializing provider %s', name)
            provider = provider_manager[name].plugin(**self.provider_configs.get(name, {}))
            provider.initialize()
            self.initialized_providers[name] = provider

        return self.initialized_providers[name]

    def __delitem__(self, name):
        if name not in self.initialized_providers:
            raise KeyError(name)

        try:
            logger.info('Terminating provider %s', name)
            self.initialized_providers[name].terminate()
        except Exception as e:
            handle_exception(e, 'Provider {} improperly terminated'.format(name))

        del self.initialized_providers[name]

    def __iter__(self):
        return iter(self.initialized_providers)

    def list_subtitles_provider(self, provider, video, languages):
        """List subtitles with a single provider.

        The video and languages are checked against the provider.

        :param str provider: name of the provider.
        :param video: video to list subtitles for.
        :type video: :class:`~subliminal.video.Video`
        :param languages: languages to search for.
        :type languages: set of :class:`~babelfish.language.Language`
        :return: found subtitles.
        :rtype: list of :class:`~subliminal.subtitle.Subtitle` or None

        """
        # check video validity
        if not provider_manager[provider].plugin.check(video):
            logger.info('Skipping provider %r: not a valid video', provider)
            return []

        # check supported languages
        provider_languages = provider_manager[provider].plugin.check_languages(languages)
        if not provider_languages:
            logger.info('Skipping provider %r: no language to search for', provider)
            return []

        # list subtitles
        logger.info('Listing subtitles with provider %r and languages %r', provider, provider_languages)
        try:
            return self[provider].list_subtitles(video, provider_languages)
        except Exception as e:
            handle_exception(e, 'Provider {}'.format(provider))

    def list_subtitles(self, video, languages):
        """List subtitles.

        :param video: video to list subtitles for.
        :type video: :class:`~subliminal.video.Video`
        :param languages: languages to search for.
        :type languages: set of :class:`~babelfish.language.Language`
        :return: found subtitles.
        :rtype: list of :class:`~subliminal.subtitle.Subtitle`

        """
        subtitles = []

        for name in self.providers:
            # check discarded providers
            if name in self.discarded_providers:
                logger.debug('Skipping discarded provider %r', name)
                continue

            # list subtitles
            provider_subtitles = self.list_subtitles_provider(name, video, languages)
            if provider_subtitles is None:
                logger.info('Discarding provider %s', name)
                self.discarded_providers.add(name)
                continue

            # add the subtitles
            subtitles.extend(provider_subtitles)

        return subtitles

    def download_subtitle(self, subtitle):
        """Download `subtitle`'s :attr:`~subliminal.subtitle.Subtitle.content`.

        :param subtitle: subtitle to download.
        :type subtitle: :class:`~subliminal.subtitle.Subtitle`
        :return: `True` if the subtitle has been successfully downloaded, `False` otherwise.
        :rtype: bool

        """
        # check discarded providers
        if subtitle.provider_name in self.discarded_providers:
            logger.warning('Provider %r is discarded', subtitle.provider_name)
            return False

        logger.info('Downloading subtitle %r', subtitle)
        try:
            self[subtitle.provider_name].download_subtitle(subtitle)
        except (BadZipfile, BadRarFile):
            logger.error('Bad archive for subtitle %r', subtitle)
        except Exception as e:
            handle_exception(e, 'Discarding provider {}'.format(subtitle.provider_name))
            self.discarded_providers.add(subtitle.provider_name)

        # check subtitle validity
        if not subtitle.is_valid():
            logger.error('Invalid subtitle')
            return False

        return True

    def download_best_subtitles(self, subtitles, video, languages, min_score=0, hearing_impaired=False, only_one=False,
                                compute_score=None):
        """Download the best matching subtitles.

        :param subtitles: the subtitles to use.
        :type subtitles: list of :class:`~subliminal.subtitle.Subtitle`
        :param video: video to download subtitles for.
        :type video: :class:`~subliminal.video.Video`
        :param languages: languages to download.
        :type languages: set of :class:`~babelfish.language.Language`
        :param int min_score: minimum score for a subtitle to be downloaded.
        :param bool hearing_impaired: hearing impaired preference.
        :param bool only_one: download only one subtitle, not one per language.
        :param compute_score: function that takes `subtitle` and `video` as positional arguments,
            `hearing_impaired` as keyword argument and returns the score.
        :return: downloaded subtitles.
        :rtype: list of :class:`~subliminal.subtitle.Subtitle`

        """
        compute_score = compute_score or default_compute_score

        # sort subtitles by score
        scored_subtitles = sorted([(s, compute_score(s, video, hearing_impaired=hearing_impaired))
                                  for s in subtitles], key=operator.itemgetter(1), reverse=True)

        # download best subtitles, falling back on the next on error
        downloaded_subtitles = []
        for subtitle, score in scored_subtitles:
            # check score
            if score < min_score:
                logger.info('Score %d is below min_score (%d)', score, min_score)
                break

            # check downloaded languages
            if subtitle.language in set(s.language for s in downloaded_subtitles):
                logger.debug('Skipping subtitle: %r already downloaded', subtitle.language)
                continue

            # download
            if self.download_subtitle(subtitle):
                downloaded_subtitles.append(subtitle)

            # stop when all languages are downloaded
            if set(s.language for s in downloaded_subtitles) == languages:
                logger.debug('All languages downloaded')
                break

            # stop if only one subtitle is requested
            if only_one:
                logger.debug('Only one subtitle downloaded')
                break

        return downloaded_subtitles

    def terminate(self):
        """Terminate all the :attr:`initialized_providers`."""
        logger.debug('Terminating initialized providers')
        for name in list(self.initialized_providers):
            del self[name]


class AsyncProviderPool(ProviderPool):
    """Subclass of :class:`ProviderPool` with asynchronous support for :meth:`~ProviderPool.list_subtitles`.

    :param int max_workers: maximum number of threads to use. If `None`, :attr:`max_workers` will be set
        to the number of :attr:`~ProviderPool.providers`.

    """
    def __init__(self, max_workers=None, *args, **kwargs):
        super(AsyncProviderPool, self).__init__(*args, **kwargs)

        #: Maximum number of threads to use
        self.max_workers = max_workers or len(self.providers)

    def list_subtitles_provider(self, provider, video, languages):
        return provider, super(AsyncProviderPool, self).list_subtitles_provider(provider, video, languages)

    def list_subtitles(self, video, languages):
        subtitles = []

        with ThreadPoolExecutor(self.max_workers) as executor:
            for provider, provider_subtitles in executor.map(self.list_subtitles_provider, self.providers,
                                                             itertools.repeat(video, len(self.providers)),
                                                             itertools.repeat(languages, len(self.providers))):
                # discard provider that failed
                if provider_subtitles is None:
                    logger.info('Discarding provider %s', provider)
                    self.discarded_providers.add(provider)
                    continue

                # add subtitles
                subtitles.extend(provider_subtitles)

        return subtitles


def check_video(video, languages=None, age=None, undefined=False):
    """Perform some checks on the `video`.

    All the checks are optional. Return `False` if any of this check fails:

        * `languages` already exist in `video`'s :attr:`~subliminal.video.Video.subtitle_languages`.
        * `video` is older than `age`.
        * `video` has an `undefined` language in :attr:`~subliminal.video.Video.subtitle_languages`.

    :param video: video to check.
    :type video: :class:`~subliminal.video.Video`
    :param languages: desired languages.
    :type languages: set of :class:`~babelfish.language.Language`
    :param datetime.timedelta age: maximum age of the video.
    :param bool undefined: fail on existing undefined language.
    :return: `True` if the video passes the checks, `False` otherwise.
    :rtype: bool

    """
    # language test
    if languages and not (languages - video.subtitle_languages):
        logger.debug('All languages %r exist', languages)
        return False

    # age test
    if age and video.age > age:
        logger.debug('Video is older than %r', age)
        return False

    # undefined test
    if undefined and Language('und') in video.subtitle_languages:
        logger.debug('Undefined language found')
        return False

    return True


def search_external_subtitles(path, directory=None):
    """Search for external subtitles from a video `path` and their associated language.

    Unless `directory` is provided, search will be made in the same directory as the video file.

    :param str path: path to the video.
    :param str directory: directory to search for subtitles.
    :return: found subtitles with their languages.
    :rtype: dict

    """
    # split path
    dirpath, filename = os.path.split(path)
    dirpath = dirpath or '.'
    fileroot, fileext = os.path.splitext(filename)

    # search for subtitles
    subtitles = {}
    for p in os.listdir(directory or dirpath):
        # keep only valid subtitle filenames
        if not p.startswith(fileroot) or not p.lower().endswith(SUBTITLE_EXTENSIONS):
            continue

        # extract the potential language code
        language = Language('und')
        language_code = p[len(fileroot):-len(os.path.splitext(p)[1])].replace(fileext, '').replace('_', '-')[1:]
        if language_code:
            try:
                language = Language.fromietf(language_code)
            except (ValueError, LanguageReverseError):
                logger.error('Cannot parse language code %r', language_code)

        subtitles[p] = language

    logger.debug('Found subtitles %r', subtitles)

    return subtitles


def scan_video(path):
    """Scan a video from a `path`.

    :param str path: existing path to the video.
    :return: the scanned video.
    :rtype: :class:`~subliminal.video.Video`

    """
    # check for non-existing path
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    # check video extension
    if not path.lower().endswith(VIDEO_EXTENSIONS):
        raise ValueError('%r is not a valid video extension' % os.path.splitext(path)[1])

    dirpath, filename = os.path.split(path)
    logger.info('Scanning video %r in %r', filename, dirpath)

    # guess
    video = Video.fromguess(path, guessit(path))

    # size
    video.size = os.path.getsize(path)
    logger.debug('Size is %d', video.size)

    return video


def scan_archive(path):
    """Scan an archive from a `path`.

    :param str path: existing path to the archive.
    :return: the scanned video.
    :rtype: :class:`~subliminal.video.Video`

    """
    # check for non-existing path
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    if not is_rarfile(path):
        raise ValueError("'{0}' is not a valid archive".format(os.path.splitext(path)[1]))

    dir_path, filename = os.path.split(path)

    logger.info('Scanning archive %r in %r', filename, dir_path)

    # Get filename and file size from RAR
    rar = RarFile(path)

    # check that the rar doesnt need a password
    if rar.needs_password():
        raise ValueError('Rar requires a password')

    # raise an exception if the rar file is broken
    # must be called to avoid a potential deadlock with some broken rars
    rar.testrar()

    file_info = [f for f in rar.infolist() if not f.isdir() and f.filename.endswith(VIDEO_EXTENSIONS)]

    # sort by file size descending, the largest video in the archive is the one we want, there may be samples or intros
    file_info.sort(key=operator.attrgetter('file_size'), reverse=True)

    # no video found
    if not file_info:
        raise ValueError('No video in archive')

    # Free the information about irrelevant files before guessing
    file_info = file_info[0]

    # guess
    video_filename = file_info.filename
    video_path = os.path.join(dir_path, video_filename)
    video = Video.fromguess(video_path, guessit(video_path))

    # size
    video.size = file_info.file_size

    return video


def scan_videos(path, age=None, archives=True):
    """Scan `path` for videos and their subtitles.

    See :func:`refine` to find additional information for the video.

    :param str path: existing directory path to scan.
    :param datetime.timedelta age: maximum age of the video or archive.
    :param bool archives: scan videos in archives.
    :return: the scanned videos.
    :rtype: list of :class:`~subliminal.video.Video`

    """
    # check for non-existing path
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    # check for non-directory path
    if not os.path.isdir(path):
        raise ValueError('Path is not a directory')

    # walk the path
    videos = []
    for dirpath, dirnames, filenames in os.walk(path):
        logger.debug('Walking directory %r', dirpath)

        # remove badly encoded and hidden dirnames
        for dirname in list(dirnames):
            if dirname.startswith('.'):
                logger.debug('Skipping hidden dirname %r in %r', dirname, dirpath)
                dirnames.remove(dirname)
            # Skip Sample folder
            if dirname.lower() == 'sample':
                logger.debug('Skipping sample dirname %r in %r', dirname, dirpath)
                dirnames.remove(dirname)

        # scan for videos
        for filename in filenames:
            # filter on videos and archives
            if not (filename.lower().endswith(VIDEO_EXTENSIONS) or
                    archives and filename.lower().endswith(ARCHIVE_EXTENSIONS)):
                continue

            # skip hidden files
            if filename.startswith('.'):
                logger.debug('Skipping hidden filename %r in %r', filename, dirpath)
                continue
            # skip 'sample' media files
            if os.path.splitext(filename)[0].lower() == 'sample':
                logger.debug('Skipping sample filename %r in %r', filename, dirpath)
                continue

            # reconstruct the file path
            filepath = os.path.join(dirpath, filename)

            # skip links
            if os.path.islink(filepath):
                logger.debug('Skipping link %r in %r', filename, dirpath)
                continue

            # skip old files
            try:
                file_age = datetime.utcfromtimestamp(os.path.getmtime(filepath))
            except ValueError:
                logger.warning('Could not get age of file %r in %r', filename, dirpath)
                continue
            else:
                if age and datetime.utcnow() - file_age > age:
                    logger.debug('Skipping old file %r in %r', filename, dirpath)
                    continue

            # scan
            if filename.lower().endswith(VIDEO_EXTENSIONS):  # video
                try:
                    video = scan_video(filepath)
                except ValueError:  # pragma: no cover
                    logger.exception('Error scanning video')
                    continue
            elif archives and filename.lower().endswith(ARCHIVE_EXTENSIONS):  # archive
                try:
                    video = scan_archive(filepath)
                except (Error, NotRarFile, RarCannotExec, ValueError):  # pragma: no cover
                    logger.exception('Error scanning archive')
                    continue
            else:  # pragma: no cover
                raise ValueError('Unsupported file %r' % filename)

            videos.append(video)

    return videos


def refine(video, episode_refiners=None, movie_refiners=None, refiner_configs=None, **kwargs):
    """Refine a video using :ref:`refiners`.

    .. note::

        Exceptions raised in refiners are silently passed and logged.

    :param video: the video to refine.
    :type video: :class:`~subliminal.video.Video`
    :param tuple episode_refiners: refiners to use for episodes.
    :param tuple movie_refiners: refiners to use for movies.
    :param dict refiner_configs: refiner configuration as keyword arguments per refiner name to pass when
        calling the refine method
    :param \*\*kwargs: additional parameters for the :func:`~subliminal.refiners.refine` functions.

    """
    refiners = ()
    if isinstance(video, Episode):
        refiners = episode_refiners or ('metadata', 'tvdb', 'omdb')
    elif isinstance(video, Movie):
        refiners = movie_refiners or ('metadata', 'omdb')
    for refiner in ('hash', ) + refiners:
        logger.info('Refining video with %s', refiner)
        try:
            refiner_manager[refiner].plugin(video, **dict((refiner_configs or {}).get(refiner, {}), **kwargs))
        except Exception as e:
            handle_exception(e, 'Failed to refine video {0!r}'.format(video.name))


def list_subtitles(videos, languages, pool_class=ProviderPool, **kwargs):
    """List subtitles.

    The `videos` must pass the `languages` check of :func:`check_video`.

    :param videos: videos to list subtitles for.
    :type videos: set of :class:`~subliminal.video.Video`
    :param languages: languages to search for.
    :type languages: set of :class:`~babelfish.language.Language`
    :param pool_class: class to use as provider pool.
    :type pool_class: :class:`ProviderPool`, :class:`AsyncProviderPool` or similar
    :param \*\*kwargs: additional parameters for the provided `pool_class` constructor.
    :return: found subtitles per video.
    :rtype: dict of :class:`~subliminal.video.Video` to list of :class:`~subliminal.subtitle.Subtitle`

    """
    listed_subtitles = defaultdict(list)

    # check videos
    checked_videos = []
    for video in videos:
        if not check_video(video, languages=languages):
            logger.info('Skipping video %r', video)
            continue
        checked_videos.append(video)

    # return immediately if no video passed the checks
    if not checked_videos:
        return listed_subtitles

    # list subtitles
    with pool_class(**kwargs) as pool:
        for video in checked_videos:
            logger.info('Listing subtitles for %r', video)
            subtitles = pool.list_subtitles(video, languages - video.subtitle_languages)
            listed_subtitles[video].extend(subtitles)
            logger.info('Found %d subtitle(s)', len(subtitles))

    return listed_subtitles


def download_subtitles(subtitles, pool_class=ProviderPool, **kwargs):
    """Download :attr:`~subliminal.subtitle.Subtitle.content` of `subtitles`.

    :param subtitles: subtitles to download.
    :type subtitles: list of :class:`~subliminal.subtitle.Subtitle`
    :param pool_class: class to use as provider pool.
    :type pool_class: :class:`ProviderPool`, :class:`AsyncProviderPool` or similar
    :param \*\*kwargs: additional parameters for the provided `pool_class` constructor.

    """
    with pool_class(**kwargs) as pool:
        for subtitle in subtitles:
            logger.info('Downloading subtitle %r', subtitle)
            pool.download_subtitle(subtitle)


def download_best_subtitles(videos, languages, min_score=0, hearing_impaired=False, only_one=False, compute_score=None,
                            pool_class=ProviderPool, **kwargs):
    """List and download the best matching subtitles.

    The `videos` must pass the `languages` and `undefined` (`only_one`) checks of :func:`check_video`.

    :param videos: videos to download subtitles for.
    :type videos: set of :class:`~subliminal.video.Video`
    :param languages: languages to download.
    :type languages: set of :class:`~babelfish.language.Language`
    :param int min_score: minimum score for a subtitle to be downloaded.
    :param bool hearing_impaired: hearing impaired preference.
    :param bool only_one: download only one subtitle, not one per language.
    :param compute_score: function that takes `subtitle` and `video` as positional arguments,
        `hearing_impaired` as keyword argument and returns the score.
    :param pool_class: class to use as provider pool.
    :type pool_class: :class:`ProviderPool`, :class:`AsyncProviderPool` or similar
    :param \*\*kwargs: additional parameters for the provided `pool_class` constructor.
    :return: downloaded subtitles per video.
    :rtype: dict of :class:`~subliminal.video.Video` to list of :class:`~subliminal.subtitle.Subtitle`

    """
    downloaded_subtitles = defaultdict(list)

    # check videos
    checked_videos = []
    for video in videos:
        if not check_video(video, languages=languages, undefined=only_one):
            logger.info('Skipping video %r', video)
            continue
        checked_videos.append(video)

    # return immediately if no video passed the checks
    if not checked_videos:
        return downloaded_subtitles

    # download best subtitles
    with pool_class(**kwargs) as pool:
        for video in checked_videos:
            logger.info('Downloading best subtitles for %r', video)
            subtitles = pool.download_best_subtitles(pool.list_subtitles(video, languages - video.subtitle_languages),
                                                     video, languages, min_score=min_score,
                                                     hearing_impaired=hearing_impaired, only_one=only_one,
                                                     compute_score=compute_score)
            logger.info('Downloaded %d subtitle(s)', len(subtitles))
            downloaded_subtitles[video].extend(subtitles)

    return downloaded_subtitles


def save_subtitles(video, subtitles, single=False, directory=None, encoding=None):
    """Save subtitles on filesystem.

    Subtitles are saved in the order of the list. If a subtitle with a language has already been saved, other subtitles
    with the same language are silently ignored.

    The extension used is `.lang.srt` by default or `.srt` is `single` is `True`, with `lang` being the IETF code for
    the :attr:`~subliminal.subtitle.Subtitle.language` of the subtitle.

    :param video: video of the subtitles.
    :type video: :class:`~subliminal.video.Video`
    :param subtitles: subtitles to save.
    :type subtitles: list of :class:`~subliminal.subtitle.Subtitle`
    :param bool single: save a single subtitle, default is to save one subtitle per language.
    :param str directory: path to directory where to save the subtitles, default is next to the video.
    :param str encoding: encoding in which to save the subtitles, default is to keep original encoding.
    :return: the saved subtitles
    :rtype: list of :class:`~subliminal.subtitle.Subtitle`

    """
    saved_subtitles = []
    for subtitle in subtitles:
        # check content
        if subtitle.content is None:
            logger.error('Skipping subtitle %r: no content', subtitle)
            continue

        # check language
        if subtitle.language in set(s.language for s in saved_subtitles):
            logger.debug('Skipping subtitle %r: language already saved', subtitle)
            continue

        # create subtitle path
        subtitle_path = subtitle.get_path(video, single=single)
        if directory is not None:
            subtitle_path = os.path.join(directory, os.path.split(subtitle_path)[1])

        # save content as is or in the specified encoding
        logger.info('Saving %r to %r', subtitle, subtitle_path)
        if encoding is None:
            with io.open(subtitle_path, 'wb') as f:
                f.write(subtitle.content)
        else:
            with io.open(subtitle_path, 'w', encoding=encoding) as f:
                f.write(subtitle.text)
        saved_subtitles.append(subtitle)

        # check single
        if single:
            break

    return saved_subtitles
