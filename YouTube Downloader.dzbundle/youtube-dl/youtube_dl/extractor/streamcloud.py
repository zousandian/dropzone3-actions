# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    sanitized_Request,
    urlencode_postdata,
)


class StreamcloudIE(InfoExtractor):
    IE_NAME = 'streamcloud.eu'
    _VALID_URL = r'https?://streamcloud\.eu/(?P<id>[a-zA-Z0-9_-]+)(?:/(?P<fname>[^#?]*)\.html)?'

    _TESTS = [{
        'url': 'http://streamcloud.eu/skp9j99s4bpz/youtube-dl_test_video_____________-BaW_jenozKc.mp4.html',
        'md5': '6bea4c7fa5daaacc2a946b7146286686',
        'info_dict': {
            'id': 'skp9j99s4bpz',
            'ext': 'mp4',
            'title': 'youtube-dl test video  \'/\\ ä ↭',
        },
        'skip': 'Only available from the EU'
    }, {
        'url': 'http://streamcloud.eu/ua8cmfh1nbe6/NSHIP-148--KUC-NG--H264-.mp4.html',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        url = 'http://streamcloud.eu/%s' % video_id

        orig_webpage = self._download_webpage(url, video_id)

        if '>File Not Found<' in orig_webpage:
            raise ExtractorError(
                'Video %s does not exist' % video_id, expected=True)

        fields = re.findall(r'''(?x)<input\s+
            type="(?:hidden|submit)"\s+
            name="([^"]+)"\s+
            (?:id="[^"]+"\s+)?
            value="([^"]*)"
            ''', orig_webpage)
        post = urlencode_postdata(fields)

        self._sleep(12, video_id)
        headers = {
            b'Content-Type': b'application/x-www-form-urlencoded',
        }
        req = sanitized_Request(url, post, headers)

        webpage = self._download_webpage(
            req, video_id, note='Downloading video page ...')
        title = self._html_search_regex(
            r'<h1[^>]*>([^<]+)<', webpage, 'title')
        video_url = self._search_regex(
            r'file:\s*"([^"]+)"', webpage, 'video URL')
        thumbnail = self._search_regex(
            r'image:\s*"([^"]+)"', webpage, 'thumbnail URL', fatal=False)

        return {
            'id': video_id,
            'title': title,
            'url': video_url,
            'thumbnail': thumbnail,
        }
