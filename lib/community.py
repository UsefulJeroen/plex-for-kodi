# coding=utf-8
"""Plex's online community and Discover services.

These are the same private APIs used by Plex Web, not Media Server APIs.
Keep credentials out of URLs, caches and exception messages. Review reactions use Plex's own mutation API; other community operations
are read-only. Watchlist changes use PM4K's existing implementation.
"""
from __future__ import absolute_import

import re

import requests

COMMUNITY_URL = 'https://community.plex.tv/api'
DISCOVER_URL = 'https://discover.provider.plex.tv/library/search'
PAGE_SIZE = 24

USER_FIELDS = 'id username displayName avatar isBlocked isMuted isHidden'
ACTIVITY_FIELDS = '''
  __typename
  ... on Activity {
    id date commentCount isMuted reaction reactionsCount reactionsTypes
    userV2 { %s }
    metadataItem { id title type year }
  }
  ... on ActivityReview { message reviewRating: rating hasSpoilers }
  ... on ActivityWatchReview { message reviewRating: rating hasSpoilers }
  ... on ActivityRating { rating }
  ... on ActivityWatchRating { rating }
''' % USER_FIELDS
PAGE_FIELDS = 'pageInfo { endCursor hasNextPage }'

REVIEWS_QUERY = '''query PM4KReviews($id: ID!, $type: ReviewsListType!,
    $first: PaginationInt!, $after: String) {
  metadataReviewsV2(metadata: {id: $id}, type: $type, first: $first, after: $after) {
    nodes { %s } %s
  }
}''' % (ACTIVITY_FIELDS, PAGE_FIELDS)

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
        raise CommunityError('unavailable')
    reaction = value.get('reaction')
    types = value.get('reactionsTypes')
    count = value.get('reactionsCount')
    if reaction is not None and reaction not in REACTION_TYPES:
        raise CommunityError('response')
    if not isinstance(types, list) or any(kind not in REACTION_TYPES for kind in types):
        raise CommunityError('response')
    if isinstance(count, bool) or not re.match(r'^\d+$', str(count)):
        raise CommunityError('response')
    return {'reaction': reaction, 'reactionsCount': int(count),
            'reactionsTypes': list(dict.fromkeys(types))}


COMMENTS_QUERY = '''query PM4KComments($id: ID!, $first: PaginationInt!, $after: String) {
  activityCommentsV2(id: $id, first: $first, after: $after) {
    nodes { id date message status user { %s } } %s
  }
}''' % (USER_FIELDS, PAGE_FIELDS)

FRIENDS_QUERY = '''query PM4KFriends {
  allFriendsV2 { user { %s } createdAt }
}''' % USER_FIELDS

PROFILE_QUERY = '''query PM4KProfile($username: ID!) {
  userByUsername(username: $username) {
    %s bio location url friendStatus
  }
}''' % USER_FIELDS

PROFILE_REVIEWS_QUERY = '''query PM4KProfileReviews($id: ID!,
    $first: PaginationInt!, $after: String) {
  user(id: $id) {
    reviews(first: $first, after: $after) { nodes { %s } %s }
  }
}''' % (ACTIVITY_FIELDS, PAGE_FIELDS)

FEED_QUERY = '''query PM4KActivity($first: PaginationInt!, $after: String,
    $types: [ActivityType!]!) {
  activityFeed(first: $first, after: $after, types: $types) {
    nodes { %s ... on ActivityPost { message } } %s
  }
}''' % (ACTIVITY_FIELDS, PAGE_FIELDS)


class CommunityError(Exception):
    """Only a safe, local error code; never contains a response or token."""


def metadata_id(guid):
    match = re.match(r'^plex://(?:movie|show|season|episode)/([a-fA-F0-9]{24})$', str(guid or ''))
    return match.group(1) if match else None


def visible_user(user):
    return bool(user) and not any(user.get(key) for key in ('isBlocked', 'isMuted', 'isHidden'))


def visible_activity(node):
    return not node.get('isMuted') and visible_user(node.get('userV2') or node.get('user')) and \
        node.get('status') not in ('DELETED', 'REMOVED', 'REJECTED')


def page(connection):
    if not isinstance(connection, dict) or not isinstance(connection.get('nodes'), list):
        raise CommunityError('response')
    info = connection.get('pageInfo') or {}
    cursor = info.get('endCursor') if info.get('hasNextPage') else None
    if info.get('hasNextPage') and not cursor:
        raise CommunityError('response')
    nodes = []
    for node in connection['nodes']:
        if isinstance(node, dict) and visible_activity(node):
            node = dict(node)
            if 'reviewRating' in node:
                node['rating'] = node.pop('reviewRating')
            nodes.append(node)
    return {'nodes': nodes, 'cursor': cursor}


class CommunityClient(object):
    def __init__(self, token_getter, headers_getter=None, offline_getter=None, session=None):
        self.token_getter = token_getter
        self.headers_getter = headers_getter or (lambda: {})
        self.offline_getter = offline_getter or (lambda: False)
        self.session = session or requests.Session()

    def close(self):
        self.session.close()

    def _request(self, url, query=None, variables=None, params=None):
        if self.offline_getter():
            raise CommunityError('offline')
        token = self.token_getter()
        if not token:
            raise CommunityError('signin')
        headers = dict(self.headers_getter())
        headers.update({'X-Plex-Token': token, 'Accept': 'application/json'})
        try:
            if query is not None:
                response = self.session.post(
                    url, json={'query': query, 'variables': variables or {}},
                    headers=headers, timeout=(5, 15), allow_redirects=False)
            else:
                response = self.session.get(url, params=params, headers=headers,
                                            timeout=(5, 15), allow_redirects=False)
        except requests.RequestException:
            raise CommunityError('network') from None
        try:
            if response.status_code in (401, 403):
                raise CommunityError('signin')
            if response.status_code == 429:
                raise CommunityError('busy')
            if not 200 <= response.status_code < 300:
                raise CommunityError('service')
            try:
                body = response.json()
            except ValueError:
                raise CommunityError('response') from None
            if not isinstance(body, dict):
                raise CommunityError('response')
            if query is not None:
                # A partial GraphQL response must not masquerade as an empty list.
                if body.get('errors') or not isinstance(body.get('data'), dict):
                    raise CommunityError('service')
                return body['data']
            return body
        finally:
            response.close()

    def reviews(self, guid, sort='RECENT', cursor=None):
        ident = metadata_id(guid)
        if not ident:
            raise CommunityError('metadata')
        if sort not in ('RECENT', 'TOP', 'HOT', 'FRIENDS'):
            raise ValueError('Unknown review order')
        data = self._request(COMMUNITY_URL, REVIEWS_QUERY,
                             {'id': ident, 'type': sort, 'first': PAGE_SIZE, 'after': cursor})
        return page(data.get('metadataReviewsV2'))

    def reactions(self, activity_id):
        data = self._request(COMMUNITY_URL, REACTIONS_QUERY, {'id': activity_id})
        return reaction_state(data.get('activityByID'))

    def react(self, activity_id, reaction):
        # None removes the account's reaction. No automatic retry for mutations:
        # a timeout may occur after Plex has already committed the change.
        if not isinstance(activity_id, str) or not activity_id.strip():
            raise ValueError('Missing activity ID')
        if reaction is not None and reaction not in REACTION_TYPES:
            raise ValueError('Unknown reaction')
        data = self._request(COMMUNITY_URL, REACT_QUERY,
                             {'input': {'activity': activity_id, 'type': reaction}})
        return reaction_state(data.get('reactToActivity'))

    def comments(self, activity_id, cursor=None):
        data = self._request(COMMUNITY_URL, COMMENTS_QUERY,
                             {'id': activity_id, 'first': PAGE_SIZE, 'after': cursor})
        return page(data.get('activityCommentsV2'))

    def friends(self):
        data = self._request(COMMUNITY_URL, FRIENDS_QUERY)
        friends = data.get('allFriendsV2')
        if not isinstance(friends, list):
            raise CommunityError('response')
        return [item['user'] for item in friends if isinstance(item, dict)
                and isinstance(item.get('user'), dict) and visible_user(item['user'])]

    def profile(self, username):
        data = self._request(COMMUNITY_URL, PROFILE_QUERY, {'username': username})
        user = data.get('userByUsername')
        if not isinstance(user, dict) or not visible_user(user):
            raise CommunityError('unavailable')
        return user

    def profile_reviews(self, user_id, cursor=None):
        data = self._request(COMMUNITY_URL, PROFILE_REVIEWS_QUERY,
                             {'id': user_id, 'first': PAGE_SIZE, 'after': cursor})
        user = data.get('user')
        if not isinstance(user, dict):
            raise CommunityError('unavailable')
        return page(user.get('reviews'))

    def activity(self, cursor=None):
        data = self._request(COMMUNITY_URL, FEED_QUERY,
                             {'first': PAGE_SIZE, 'after': cursor,
                              'types': ['REVIEW', 'RATING', 'WATCH_REVIEW', 'WATCH_RATING', 'POST']})
        return page(data.get('activityFeed'))

    def discover(self, query):
        if not query or not query.strip():
            return []
        data = self._request(DISCOVER_URL, params={
            'query': query.strip(), 'searchProviders': 'discover',
            'searchTypes': 'movies,tv', 'limit': 50, 'includeMeta': 1})
        container = data.get('MediaContainer')
        if not isinstance(container, dict) or not isinstance(container.get('SearchResults'), list):
            raise CommunityError('response')
        results, seen = [], set()
        for group in container['SearchResults']:
            if not isinstance(group, dict) or not isinstance(group.get('SearchResult', []), list):
                raise CommunityError('response')
            for result in group.get('SearchResult', []):
                if not isinstance(result, dict):
                    raise CommunityError('response')
                item = result.get('Metadata') or {}
                if not isinstance(item, dict):
                    raise CommunityError('response')
                guid = item.get('guid')
                if item.get('type') in ('movie', 'show') and metadata_id(guid) and guid not in seen:
                    seen.add(guid)
                    results.append(item)
        return results


def client_for_account():
    from plexnet import plexapp, util
    return CommunityClient(lambda: plexapp.ACCOUNT.authToken,
                           util.getPlexHeaders,
                           lambda: util.LOCAL_MODE or plexapp.ACCOUNT.isManaged)
