# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import json, os, shutil, copy
from typing import Optional, List, Union, Dict, Tuple
from urllib.parse import quote, unquote

# Pip
from ksimpleapi import Api, Request
from kstopit import signal_timeoutable

# Local
from .models import SearchResultListing, Listing, Region
from .models.enums import ListingSortType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Zillow ------------------------------------------------------------- #

class Zillow(Api):

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def get_regions(
        self,
        search_term: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: Optional[bool] = None
    ) -> Optional[List[Region]]:
        debug = debug if debug is not None else self._request.debug

        try:
            return [Region(d) for d in self._get(
                'https://www.zillowstatic.com/autocomplete/v2/suggestions?q={}'.format(quote(search_term)),
                user_agent=user_agent,
                proxy=proxy,
                max_request_try_count=max_request_try_count,
                sleep_s_between_failed_requests=sleep_s_between_failed_requests,
                debug=debug
            ).json()['resultGroups'][0]['results']]
        except Exception as e:
            if debug:
                print(e)

            return None

    def get_listings(
        self,
        region: Region,
        sort_type: Optional[ListingSortType] = ListingSortType.NEWEST,
        min_bedrooms: Optional[int] = None,
        min_bathrooms: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        min_results: int = 20,
        ignored_ids: List[int] = [],
        needs_video: bool = False,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: Optional[bool] = None
    ) -> Optional[List[SearchResultListing]]:
        debug = debug if debug is not None else self._request.debug
        ignored_ids = copy.deepcopy(ignored_ids) if ignored_ids else []
        north, east, south, west = self.__get_region_bounds(region.slug, debug)

        searchQueryState={
            "pagination":{},
            "mapBounds":{
                "west":west,
                "east":east,
                "south":south,
                "north":north
            },
            "regionSelection":[{"regionId":region.id}],
            "isMapVisible":True,
            "filterState":{
                "ah":{"value":True}
            },
            "isAllHomes":{"value":True},
            "isListVisible":True
        }

        if sort_type and sort_type.value:
            searchQueryState['filterState']['sort'] = sort_type.value

        if min_bedrooms:
            searchQueryState['filterState']['beds'] = min_bedrooms

        if min_bathrooms:
            searchQueryState['filterState']['baths'] = min_bathrooms

        if min_price or max_price:
            searchQueryState['filterState']['price'] = {}

            if min_price:
                searchQueryState['filterState']['price']['min'] = min_price

            if max_price:
                searchQueryState['filterState']['price']['max'] = max_price

        org_keep_cookies = self._request.keep_cookies
        self._request.keep_cookies = True
        listings = []
        page_number = 1

        while len(listings) < min_results:
            new_listings = self.__get_listings(region.slug, searchQueryState, page_number, debug)

            if not new_listings:
                self._request.keep_cookies = org_keep_cookies

                return listings

            for l in new_listings:
                if l.id not in ignored_ids and (not needs_video or l.has_video):
                    listings.append(l)
                    ignored_ids.append(l.id)

            page_number += 1

        self._request.keep_cookies = org_keep_cookies

        return listings

    def get_listing(
        self,
        listing_id: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: Optional[bool] = None
    ) -> Optional[Listing]:
        debug = debug if debug is not None else self._request.debug

        try:
            res = self._get('https://www.zillow.com/homedetails/{}_zpid'.format(listing_id))
            res_text = res.content.decode('unicode_escape').split('<script id=hdpApolloPreloadedData type="application/json">')[1].split('</script>')[0].strip().replace('apiCache":"{"VariantQuery', 'apiCache\\":\\"{\\"VariantQuery').split('}}","zpid"')[0] + '}}'

            return Listing(json.loads(res_text))
        except Exception as e:
            if debug:
                print(e)

            return None

    @signal_timeoutable(name='zillow.download')
    def download_listing_assets(
        self,
        listing: Listing,
        out_folder_path: str,
        image_pre_name: str = 'image',
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        debug: Optional[bool] = None,
        download_images_max_concurent_processes: Optional[int] = None,
        create_video_max_concurent_processes: Optional[int] = None,
        timeout: Optional[int]= 10*60
    ) -> Tuple[Optional[str], List[str]]:
        from simple_multiprocessing import MultiProcess, Task
        """Returns:
            Tuple[Optional[str], Optional[str], Optional[List[str]]]: [video_path, main_image_path, image_paths]
        """

        def create_video(max_concurent_processes: Optional[int] = None):
            if listing.video:
                video_path = os.path.join(out_folder_path, 'video.mp4')
                video_temp_folder_path = os.path.join(out_folder_path, 'video_temp')
                os.makedirs(video_temp_folder_path, exist_ok=True)
                video_res = self.__download_listing_video(
                    listing.video.url_m3u8,
                    video_temp_folder_path,
                    video_path,
                    user_agent=user_agent,
                    proxy=proxy,
                    max_request_try_count=max_request_try_count,
                    sleep_s_between_failed_requests=sleep_s_between_failed_requests,
                    debug=debug,
                    max_concurent_processes=max_concurent_processes
                )
                shutil.rmtree(video_temp_folder_path)

                return video_path if video_res else None
            else:
                return None

        return MultiProcess([
            Task(create_video, max_concurent_processes=create_video_max_concurent_processes),
            Task(
                self.__download_listing_images,
                [l.url for l in listing.images],
                out_folder_path,
                image_pre_name,
                user_agent=user_agent,
                proxy=proxy,
                max_request_try_count=max_request_try_count,
                sleep_s_between_failed_requests=sleep_s_between_failed_requests,
                debug=debug,
                max_concurent_processes=download_images_max_concurent_processes
            )
        ]).solve()

    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __get_listings(
        self,
        region_str: str,
        searchQueryState: dict,
        page: int,
        debug: bool
    ) -> Optional[List[SearchResultListing]]:
        searchQueryState['pagination']['currentPage'] = page

        try:
            url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={}&wants=%7B%22cat1%22%3A%5B%22listResults%22%5D%7D&requestId={}'.format(quote(json.dumps(searchQueryState)), page+1)
            res = self._get(url)
            j = res.json()['cat1']['searchResults']['listResults']

            return [SearchResultListing(e)for e in j]
        except Exception as e:
            if debug:
                print('err', e)

            return None

    def __get_region_bounds(
        self,
        region_str: str,
        debug: bool
    ) -> Optional[Tuple[float, float, float, float]]:
        try:
            res = self._get('https://www.zillow.com/homes/{}'.format(quote(region_str)))
            s = unquote(unquote(res.cookies.get('search'))).split('rect=')[-1].split('&')[0].replace('\t', '')

            return [float(_s) for _s in s.split(',')]
        except Exception as e:
            if debug:
                print(e)

            return None

    def __download_listing_video(
        self,
        url: str,
        temp_folder_path: str,
        out_path: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        debug: Optional[bool] = None,
        max_concurent_processes: Optional[int] = None
    ) -> bool:
        import m3u8
        from kffmpeg import ffmpeg

        info = m3u8.load(url)

        if not info or not info.playlists:
            return False

        playlist = info.playlists[-1]
        playlist_url = playlist.base_uri+playlist.uri
        playlist = m3u8.load(playlist_url)
        # urls_paths = {s.base_uri+s.uri:os.path.join(temp_folder_path, s.uri) for s in playlist.segments}
        file_paths = []

        for s in playlist.segments:
            url_download_path = s.base_uri+s.uri
            file_path = os.path.join(temp_folder_path, s.uri)

            self.download(url_download_path, file_path, user_agent=user_agent, proxy=proxy, max_request_try_count=max_request_try_count, debug=debug)
            file_paths.append(file_path)

        # res = self.download_async(urls_paths, user_agent=user_agent, proxy=proxy, max_request_try_count=max_request_try_count, debug=debug, max_concurent_processes=max_concurent_processes)
        # paths = list(urls_paths.values())

        # if False in res:
        #     [os.remove(p) for p in file_paths if os.path.exists(p)]

        #     return False

        p_ts = os.path.join(temp_folder_path, 'temp.ts')

        if not ffmpeg.concat_videos_copy(file_paths, p_ts, debug=debug):
            [os.remove(p) for p in file_paths if os.path.exists(p)]

            return False

        res = ffmpeg.ts_to_mp4(p_ts, out_path, debug=debug)
        os.remove(p_ts)

        return res

    def __download_listing_images(
        self,
        urls: List[str],
        folder_path: str,
        image_pre_name: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = None,
        sleep_s_between_failed_requests: Optional[float] = None,
        debug: Optional[bool] = None,
        max_concurent_processes: Optional[int] = None
    ) -> List[str]:

        urls_paths = {url:os.path.join(folder_path, str(i).zfill(3) + '.' + url.split('.')[-1]) for i, url in enumerate(urls)}
        paths = list(urls_paths.values())
        res = self.download_async(urls_paths, user_agent=user_agent, proxy=proxy, max_request_try_count=max_request_try_count, debug=debug, max_concurent_processes=max_concurent_processes)

        return [paths[i] for i, _res in enumerate(res) if _res]


# ---------------------------------------------------------------------------------------------------------------------------------------- #