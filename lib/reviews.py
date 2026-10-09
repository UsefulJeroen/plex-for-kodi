# coding=utf-8
"""Reviews and reactions through the private API used by Plex clients."""
from __future__ import absolute_import

import re

import requests
from plexnet import plexapp, util

COMMUNITY_URL = 'https://community.plex.tv/api'
PAGE_SIZE = 24

USER_FIELDS = 'username displayName avatar isBlocked isMuted isHidden'
PAGE_FIELDS = 'pageInfo { endCursor hasNextPage }'

REVIEWS_QUERY = '''query PM4KReviews($id: ID!, $type: ReviewsListType!,
    $first: PaginationInt!, $after: String) {
  metadataReviewsV2(metadata: {id: $id}, type: $type, first: $first, after: $after) {
    nodes {
      ... on Activity {
        id date commentCount isMuted reaction reactionsCount reactionsTypes
        userV2 { %s }
      }
      ... on ActivityReview { message reviewRating: rating hasSpoilers }
      ... on ActivityWatchReview { message reviewRating: rating hasSpoilers }
      ... on ActivityRating { rating }
      ... on ActivityWatchRating { rating }
    } %s
  }
}''' % (USER_FIELDS, PAGE_FIELDS)

REACTION_TYPES = ('LIKE', 'DISLIKE', 'LOVE', 'LAUGH', 'APPLAUD', 'QUESTION')
REACTIONS_QUERY = """query PM4KReviewReactions($id: ID!) {
  activityByID(id: $id) {
    ... on Activity { reaction reactionsCount reactionsTypes }
  }
}"""
REACT_QUERY = """mutation PM4KReactToReview($input: ReactToActivityInput!) {
  reactToActivity(input: $input) { reaction reactionsCount reactionsTypes }
}"""


def reaction_state(value):
    if not isinstance(value, dict):
        raise ReviewsError('unavailable')
    reaction = value.get('reaction')
    types = value.get('reactionsTypes')
    count = value.get('reactionsCount')
    if reaction is not None and reaction not in REACTION_TYPES:
        raise ReviewsError('response')
    if not isinstance(types, list) or any(kind not in REACTION_TYPES for kind in types):
        raise ReviewsError('response')
    if isinstance(count, bool) or not re.match(r'^\d+$', str(count)):
        raise ReviewsError('response')
    return {'reaction': reaction, 'reactionsCount': int(count),
            'reactionsTypes': list(dict.fromkeys(types))}


COMMENTS_QUERY = '''query PM4KComments($id: ID!, $first: PaginationInt!, $after: String) {
  activityCommentsV2(id: $id, first: $first, after: $after) {
    nodes { id date message status user { %s } } %s
  }
}''' % (USER_FIELDS, PAGE_FIELDS)


class ReviewsError(Exception):
    """Only a safe, local error code; never contains a response or token."""


def metadata_id(guid):
    match = re.match(r'^plex://(?:movie|show|season|episode)/([a-fA-F0-9]{24})$', str(guid or ''))
    return match.group(1) if match else None


def page(connection):
    if not isinstance(connection, dict) or not isinstance(connection.get('nodes'), list):
        raise ReviewsError('response')
    info = connection.get('pageInfo') or {}
    if not isinstance(info, dict):
        raise ReviewsError('response')
    cursor = info.get('endCursor') if info.get('hasNextPage') else None
    if info.get('hasNextPage') and not cursor:
        raise ReviewsError('response')
    nodes = []
    for node in connection['nodes']:
        if not isinstance(node, dict):
            continue
        user = node.get('userV2') or node.get('user')
        if (not isinstance(user, dict) or not user or
                any(user.get(key) for key in ('isBlocked', 'isMuted', 'isHidden')) or
                node.get('isMuted') or node.get('status') in ('DELETED', 'REMOVED', 'REJECTED')):
            continue
        node = dict(node)
        if 'reviewRating' in node:
            node['rating'] = node.pop('reviewRating')
        nodes.append(node)
    return {'nodes': nodes, 'cursor': cursor}


class ReviewsClient(object):
    def __init__(self):
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _request(self, query, variables):
        if util.LOCAL_MODE or plexapp.ACCOUNT.isManaged:
            raise ReviewsError('offline')
        token = plexapp.ACCOUNT.authToken
        if not token:
            raise ReviewsError('signin')
        headers = dict(util.getPlexHeaders())
        headers.update({'X-Plex-Token': token, 'Accept': 'application/json'})
        try:
            response = self.session.post(
                COMMUNITY_URL, json={'query': query, 'variables': variables},
                headers=headers, timeout=(5, 15), allow_redirects=False)
        except requests.RequestException:
            raise ReviewsError('network') from None
        try:
            if response.status_code in (401, 403):
                raise ReviewsError('signin')
            if response.status_code == 429:
                raise ReviewsError('busy')
            if not 200 <= response.status_code < 300:
                raise ReviewsError('service')
            try:
                body = response.json()
            except ValueError:
                raise ReviewsError('response') from None
            if not isinstance(body, dict):
                raise ReviewsError('response')
            if body.get('errors') or not isinstance(body.get('data'), dict):
                raise ReviewsError('service')
            return body['data']
        finally:
            response.close()

    def reviews(self, guid, sort='RECENT', cursor=None):
        ident = metadata_id(guid)
        if not ident:
            raise ReviewsError('metadata')
        if sort not in ('RECENT', 'TOP', 'HOT', 'FRIENDS'):
            raise ValueError('Unknown review order')
        data = self._request(REVIEWS_QUERY,
                             {'id': ident, 'type': sort, 'first': PAGE_SIZE, 'after': cursor})
        return page(data.get('metadataReviewsV2'))

    def reactions(self, activity_id):
        data = self._request(REACTIONS_QUERY, {'id': activity_id})
        return reaction_state(data.get('activityByID'))

    def react(self, activity_id, reaction):
        # A timed-out mutation may have committed; never retry it automatically.
        if not isinstance(activity_id, str) or not activity_id.strip():
            raise ValueError('Missing activity ID')
        if reaction is not None and reaction not in REACTION_TYPES:
            raise ValueError('Unknown reaction')
        data = self._request(REACT_QUERY,
                             {'input': {'activity': activity_id, 'type': reaction}})
        return reaction_state(data.get('reactToActivity'))

    def comments(self, activity_id, cursor=None):
        data = self._request(COMMENTS_QUERY,
                             {'id': activity_id, 'first': PAGE_SIZE, 'after': cursor})
        return page(data.get('activityCommentsV2'))
