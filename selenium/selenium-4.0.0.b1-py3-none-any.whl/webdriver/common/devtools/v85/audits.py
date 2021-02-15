# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Audits (experimental)
from __future__ import annotations
from .util import event_class, T_JSON_DICT
from dataclasses import dataclass
import enum
import typing
from . import network
from . import page


@dataclass
class AffectedCookie:
    '''
    Information about a cookie that is affected by an inspector issue.
    '''
    #: The following three properties uniquely identify a cookie
    name: str

    path: str

    domain: str

    def to_json(self):
        json = dict()
        json['name'] = self.name
        json['path'] = self.path
        json['domain'] = self.domain
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            name=str(json['name']),
            path=str(json['path']),
            domain=str(json['domain']),
        )


@dataclass
class AffectedRequest:
    '''
    Information about a request that is affected by an inspector issue.
    '''
    #: The unique request id.
    request_id: network.RequestId

    url: typing.Optional[str] = None

    def to_json(self):
        json = dict()
        json['requestId'] = self.request_id.to_json()
        if self.url is not None:
            json['url'] = self.url
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            request_id=network.RequestId.from_json(json['requestId']),
            url=str(json['url']) if 'url' in json else None,
        )


@dataclass
class AffectedFrame:
    '''
    Information about the frame affected by an inspector issue.
    '''
    frame_id: page.FrameId

    def to_json(self):
        json = dict()
        json['frameId'] = self.frame_id.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            frame_id=page.FrameId.from_json(json['frameId']),
        )


class SameSiteCookieExclusionReason(enum.Enum):
    EXCLUDE_SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = "ExcludeSameSiteUnspecifiedTreatedAsLax"
    EXCLUDE_SAME_SITE_NONE_INSECURE = "ExcludeSameSiteNoneInsecure"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


class SameSiteCookieWarningReason(enum.Enum):
    WARN_SAME_SITE_UNSPECIFIED_CROSS_SITE_CONTEXT = "WarnSameSiteUnspecifiedCrossSiteContext"
    WARN_SAME_SITE_NONE_INSECURE = "WarnSameSiteNoneInsecure"
    WARN_SAME_SITE_UNSPECIFIED_LAX_ALLOW_UNSAFE = "WarnSameSiteUnspecifiedLaxAllowUnsafe"
    WARN_SAME_SITE_STRICT_LAX_DOWNGRADE_STRICT = "WarnSameSiteStrictLaxDowngradeStrict"
    WARN_SAME_SITE_STRICT_CROSS_DOWNGRADE_STRICT = "WarnSameSiteStrictCrossDowngradeStrict"
    WARN_SAME_SITE_STRICT_CROSS_DOWNGRADE_LAX = "WarnSameSiteStrictCrossDowngradeLax"
    WARN_SAME_SITE_LAX_CROSS_DOWNGRADE_STRICT = "WarnSameSiteLaxCrossDowngradeStrict"
    WARN_SAME_SITE_LAX_CROSS_DOWNGRADE_LAX = "WarnSameSiteLaxCrossDowngradeLax"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


class SameSiteCookieOperation(enum.Enum):
    SET_COOKIE = "SetCookie"
    READ_COOKIE = "ReadCookie"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


@dataclass
class SameSiteCookieIssueDetails:
    '''
    This information is currently necessary, as the front-end has a difficult
    time finding a specific cookie. With this, we can convey specific error
    information without the cookie.
    '''
    cookie: AffectedCookie

    cookie_warning_reasons: typing.List[SameSiteCookieWarningReason]

    cookie_exclusion_reasons: typing.List[SameSiteCookieExclusionReason]

    #: Optionally identifies the site-for-cookies and the cookie url, which
    #: may be used by the front-end as additional context.
    operation: SameSiteCookieOperation

    site_for_cookies: typing.Optional[str] = None

    cookie_url: typing.Optional[str] = None

    request: typing.Optional[AffectedRequest] = None

    def to_json(self):
        json = dict()
        json['cookie'] = self.cookie.to_json()
        json['cookieWarningReasons'] = [i.to_json() for i in self.cookie_warning_reasons]
        json['cookieExclusionReasons'] = [i.to_json() for i in self.cookie_exclusion_reasons]
        json['operation'] = self.operation.to_json()
        if self.site_for_cookies is not None:
            json['siteForCookies'] = self.site_for_cookies
        if self.cookie_url is not None:
            json['cookieUrl'] = self.cookie_url
        if self.request is not None:
            json['request'] = self.request.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            cookie=AffectedCookie.from_json(json['cookie']),
            cookie_warning_reasons=[SameSiteCookieWarningReason.from_json(i) for i in json['cookieWarningReasons']],
            cookie_exclusion_reasons=[SameSiteCookieExclusionReason.from_json(i) for i in json['cookieExclusionReasons']],
            operation=SameSiteCookieOperation.from_json(json['operation']),
            site_for_cookies=str(json['siteForCookies']) if 'siteForCookies' in json else None,
            cookie_url=str(json['cookieUrl']) if 'cookieUrl' in json else None,
            request=AffectedRequest.from_json(json['request']) if 'request' in json else None,
        )


class MixedContentResolutionStatus(enum.Enum):
    MIXED_CONTENT_BLOCKED = "MixedContentBlocked"
    MIXED_CONTENT_AUTOMATICALLY_UPGRADED = "MixedContentAutomaticallyUpgraded"
    MIXED_CONTENT_WARNING = "MixedContentWarning"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


class MixedContentResourceType(enum.Enum):
    AUDIO = "Audio"
    BEACON = "Beacon"
    CSP_REPORT = "CSPReport"
    DOWNLOAD = "Download"
    EVENT_SOURCE = "EventSource"
    FAVICON = "Favicon"
    FONT = "Font"
    FORM = "Form"
    FRAME = "Frame"
    IMAGE = "Image"
    IMPORT = "Import"
    MANIFEST = "Manifest"
    PING = "Ping"
    PLUGIN_DATA = "PluginData"
    PLUGIN_RESOURCE = "PluginResource"
    PREFETCH = "Prefetch"
    RESOURCE = "Resource"
    SCRIPT = "Script"
    SERVICE_WORKER = "ServiceWorker"
    SHARED_WORKER = "SharedWorker"
    STYLESHEET = "Stylesheet"
    TRACK = "Track"
    VIDEO = "Video"
    WORKER = "Worker"
    XML_HTTP_REQUEST = "XMLHttpRequest"
    XSLT = "XSLT"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


@dataclass
class MixedContentIssueDetails:
    #: The way the mixed content issue is being resolved.
    resolution_status: MixedContentResolutionStatus

    #: The unsafe http url causing the mixed content issue.
    insecure_url: str

    #: The url responsible for the call to an unsafe url.
    main_resource_url: str

    #: The type of resource causing the mixed content issue (css, js, iframe,
    #: form,...). Marked as optional because it is mapped to from
    #: blink::mojom::RequestContextType, which will be replaced
    #: by network::mojom::RequestDestination
    resource_type: typing.Optional[MixedContentResourceType] = None

    #: The mixed content request.
    #: Does not always exist (e.g. for unsafe form submission urls).
    request: typing.Optional[AffectedRequest] = None

    #: Optional because not every mixed content issue is necessarily linked to a frame.
    frame: typing.Optional[AffectedFrame] = None

    def to_json(self):
        json = dict()
        json['resolutionStatus'] = self.resolution_status.to_json()
        json['insecureURL'] = self.insecure_url
        json['mainResourceURL'] = self.main_resource_url
        if self.resource_type is not None:
            json['resourceType'] = self.resource_type.to_json()
        if self.request is not None:
            json['request'] = self.request.to_json()
        if self.frame is not None:
            json['frame'] = self.frame.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            resolution_status=MixedContentResolutionStatus.from_json(json['resolutionStatus']),
            insecure_url=str(json['insecureURL']),
            main_resource_url=str(json['mainResourceURL']),
            resource_type=MixedContentResourceType.from_json(json['resourceType']) if 'resourceType' in json else None,
            request=AffectedRequest.from_json(json['request']) if 'request' in json else None,
            frame=AffectedFrame.from_json(json['frame']) if 'frame' in json else None,
        )


class BlockedByResponseReason(enum.Enum):
    '''
    Enum indicating the reason a response has been blocked. These reasons are
    refinements of the net error BLOCKED_BY_RESPONSE.
    '''
    COEP_FRAME_RESOURCE_NEEDS_COEP_HEADER = "CoepFrameResourceNeedsCoepHeader"
    COOP_SANDBOXED_I_FRAME_CANNOT_NAVIGATE_TO_COOP_PAGE = "CoopSandboxedIFrameCannotNavigateToCoopPage"
    CORP_NOT_SAME_ORIGIN = "CorpNotSameOrigin"
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_COEP = "CorpNotSameOriginAfterDefaultedToSameOriginByCoep"
    CORP_NOT_SAME_SITE = "CorpNotSameSite"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


@dataclass
class BlockedByResponseIssueDetails:
    '''
    Details for a request that has been blocked with the BLOCKED_BY_RESPONSE
    code. Currently only used for COEP/COOP, but may be extended to include
    some CSP errors in the future.
    '''
    request: AffectedRequest

    reason: BlockedByResponseReason

    frame: typing.Optional[AffectedFrame] = None

    def to_json(self):
        json = dict()
        json['request'] = self.request.to_json()
        json['reason'] = self.reason.to_json()
        if self.frame is not None:
            json['frame'] = self.frame.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            request=AffectedRequest.from_json(json['request']),
            reason=BlockedByResponseReason.from_json(json['reason']),
            frame=AffectedFrame.from_json(json['frame']) if 'frame' in json else None,
        )


class HeavyAdResolutionStatus(enum.Enum):
    HEAVY_AD_BLOCKED = "HeavyAdBlocked"
    HEAVY_AD_WARNING = "HeavyAdWarning"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


class HeavyAdReason(enum.Enum):
    NETWORK_TOTAL_LIMIT = "NetworkTotalLimit"
    CPU_TOTAL_LIMIT = "CpuTotalLimit"
    CPU_PEAK_LIMIT = "CpuPeakLimit"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


@dataclass
class HeavyAdIssueDetails:
    #: The resolution status, either blocking the content or warning.
    resolution: HeavyAdResolutionStatus

    #: The reason the ad was blocked, total network or cpu or peak cpu.
    reason: HeavyAdReason

    #: The frame that was blocked.
    frame: AffectedFrame

    def to_json(self):
        json = dict()
        json['resolution'] = self.resolution.to_json()
        json['reason'] = self.reason.to_json()
        json['frame'] = self.frame.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            resolution=HeavyAdResolutionStatus.from_json(json['resolution']),
            reason=HeavyAdReason.from_json(json['reason']),
            frame=AffectedFrame.from_json(json['frame']),
        )


class InspectorIssueCode(enum.Enum):
    '''
    A unique identifier for the type of issue. Each type may use one of the
    optional fields in InspectorIssueDetails to convey more specific
    information about the kind of issue.
    '''
    SAME_SITE_COOKIE_ISSUE = "SameSiteCookieIssue"
    MIXED_CONTENT_ISSUE = "MixedContentIssue"
    BLOCKED_BY_RESPONSE_ISSUE = "BlockedByResponseIssue"
    HEAVY_AD_ISSUE = "HeavyAdIssue"

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json):
        return cls(json)


@dataclass
class InspectorIssueDetails:
    '''
    This struct holds a list of optional fields with additional information
    specific to the kind of issue. When adding a new issue code, please also
    add a new optional field to this type.
    '''
    same_site_cookie_issue_details: typing.Optional[SameSiteCookieIssueDetails] = None

    mixed_content_issue_details: typing.Optional[MixedContentIssueDetails] = None

    blocked_by_response_issue_details: typing.Optional[BlockedByResponseIssueDetails] = None

    heavy_ad_issue_details: typing.Optional[HeavyAdIssueDetails] = None

    def to_json(self):
        json = dict()
        if self.same_site_cookie_issue_details is not None:
            json['sameSiteCookieIssueDetails'] = self.same_site_cookie_issue_details.to_json()
        if self.mixed_content_issue_details is not None:
            json['mixedContentIssueDetails'] = self.mixed_content_issue_details.to_json()
        if self.blocked_by_response_issue_details is not None:
            json['blockedByResponseIssueDetails'] = self.blocked_by_response_issue_details.to_json()
        if self.heavy_ad_issue_details is not None:
            json['heavyAdIssueDetails'] = self.heavy_ad_issue_details.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            same_site_cookie_issue_details=SameSiteCookieIssueDetails.from_json(json['sameSiteCookieIssueDetails']) if 'sameSiteCookieIssueDetails' in json else None,
            mixed_content_issue_details=MixedContentIssueDetails.from_json(json['mixedContentIssueDetails']) if 'mixedContentIssueDetails' in json else None,
            blocked_by_response_issue_details=BlockedByResponseIssueDetails.from_json(json['blockedByResponseIssueDetails']) if 'blockedByResponseIssueDetails' in json else None,
            heavy_ad_issue_details=HeavyAdIssueDetails.from_json(json['heavyAdIssueDetails']) if 'heavyAdIssueDetails' in json else None,
        )


@dataclass
class InspectorIssue:
    '''
    An inspector issue reported from the back-end.
    '''
    code: InspectorIssueCode

    details: InspectorIssueDetails

    def to_json(self):
        json = dict()
        json['code'] = self.code.to_json()
        json['details'] = self.details.to_json()
        return json

    @classmethod
    def from_json(cls, json):
        return cls(
            code=InspectorIssueCode.from_json(json['code']),
            details=InspectorIssueDetails.from_json(json['details']),
        )


def get_encoded_response(
        request_id: network.RequestId,
        encoding: str,
        quality: typing.Optional[float] = None,
        size_only: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.Tuple[typing.Optional[str], int, int]]:
    '''
    Returns the response body and size if it were re-encoded with the specified settings. Only
    applies to images.

    :param request_id: Identifier of the network request to get content for.
    :param encoding: The encoding to use.
    :param quality: *(Optional)* The quality of the encoding (0-1). (defaults to 1)
    :param size_only: *(Optional)* Whether to only return the size information (defaults to false).
    :returns: A tuple with the following items:

        0. **body** - *(Optional)* The encoded body as a base64 string. Omitted if sizeOnly is true.
        1. **originalSize** - Size before re-encoding.
        2. **encodedSize** - Size after re-encoding.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    params['encoding'] = encoding
    if quality is not None:
        params['quality'] = quality
    if size_only is not None:
        params['sizeOnly'] = size_only
    cmd_dict: T_JSON_DICT = {
        'method': 'Audits.getEncodedResponse',
        'params': params,
    }
    json = yield cmd_dict
    return (
        str(json['body']) if 'body' in json else None,
        int(json['originalSize']),
        int(json['encodedSize'])
    )


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables issues domain, prevents further issues from being reported to the client.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Audits.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables issues domain, sends the issues collected so far to the client by means of the
    ``issueAdded`` event.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Audits.enable',
    }
    json = yield cmd_dict


@event_class('Audits.issueAdded')
@dataclass
class IssueAdded:
    issue: InspectorIssue

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> IssueAdded:
        return cls(
            issue=InspectorIssue.from_json(json['issue'])
        )
