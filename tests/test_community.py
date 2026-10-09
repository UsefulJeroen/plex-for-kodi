# coding=utf-8
"""Authentication, privacy, pagination, spoilers and navigation of online Plex data."""
from unittest import mock

import requests
from kodienv import ENV

from lib import community
from lib.windows import community as ui
from .base import KodiTestCase

GUID = 'plex://movie/5d7769cefb0d55001f530acd'
USER = {'id': 'user-1', 'username': 'example', 'displayName': 'Example',
        'isBlocked': False, 'isMuted': False, 'isHidden': False}


def activity(**kwargs):
    value = {'id': 'review-1', 'userV2': dict(USER), 'message': 'A thoughtful review',
             'hasSpoilers': False, 'commentCount': 4, 'reviewRating': 8,
             'metadataItem': {'id': community.metadata_id(GUID), 'type': 'movie', 'title': 'A movie'}}
    value.update(kwargs)
    return value


def connection(nodes=None, cursor=None):
    return {'nodes': nodes if nodes is not None else [activity()],
            'pageInfo': {'endCursor': cursor, 'hasNextPage': bool(cursor)}}


class ClientTest(KodiTestCase):
    def setUp(self):
        super(ClientTest, self).setUp()
        self.session = mock.Mock()
        self.response = self.session.post.return_value
        self.response.status_code = 200
        self.response.json.return_value = {'data': {'metadataReviewsV2': connection()}}
        self.token = 'not-a-real-token'
        self.offline = False
        self.client = community.CommunityClient(lambda: self.token,
                                                lambda: {'X-Plex-Product': 'PM4K'},
                                                lambda: self.offline, self.session)

    def test_uses_account_header_and_current_user_on_every_request(self):
        self.client.reviews(GUID)
        args, kwargs = self.session.post.call_args
        self.assertEqual(community.COMMUNITY_URL, args[0])
        self.assertNotIn(self.token, args[0])
        self.assertEqual(self.token, kwargs['headers']['X-Plex-Token'])
        self.assertEqual('5d7769cefb0d55001f530acd', kwargs['json']['variables']['id'])
        self.assertEqual((5, 15), kwargs['timeout'])
        self.assertFalse(kwargs['allow_redirects'])
        self.token = 'different-account'
        self.client.reviews(GUID)
        self.assertEqual(self.token, self.session.post.call_args.kwargs['headers']['X-Plex-Token'])

    def test_local_mode_and_missing_login_never_contact_plex(self):
        for offline, token, code in [(True, self.token, 'offline'), (False, None, 'signin')]:
            self.offline, self.token = offline, token
            with self.assertRaisesRegex(community.CommunityError, code):
                self.client.reviews(GUID)
        self.session.post.assert_not_called()

    def test_legacy_agents_do_not_send_server_rating_keys_to_community(self):
        for guid in ('123', 'com.plexapp.agents.imdb://tt123', 'plex://movie/123',
                     GUID + '?token=secret', None):
            with self.assertRaisesRegex(community.CommunityError, 'metadata'):
                self.client.reviews(guid)
        self.session.post.assert_not_called()

    def test_review_union_ratings_and_nullable_reviews_are_normalized(self):
        self.response.json.return_value = {'data': {'metadataReviewsV2': connection(
            [activity(reviewRating=None), activity(id='rating-1', rating=10, reviewRating=6)])}}
        nodes = self.client.reviews(GUID)['nodes']
        self.assertIsNone(nodes[0]['rating'])
        self.assertEqual(6, nodes[1]['rating'])
        self.assertNotIn('reviewRating', nodes[1])

    def test_muted_blocked_hidden_and_removed_content_is_filtered(self):
        nodes = [activity()]
        for flag in ('isMuted', 'isBlocked', 'isHidden'):
            user = dict(USER, **{flag: True})
            nodes.append(activity(userV2=user))
        nodes.extend([activity(isMuted=True), activity(status='REMOVED')])
        self.response.json.return_value = {'data': {'metadataReviewsV2': connection(nodes, 'more')}}
        result = self.client.reviews(GUID)
        self.assertEqual(1, len(result['nodes']))
        self.assertEqual('more', result['cursor'])

    def test_comment_pagination_uses_activity_id_not_metadata_id(self):
        self.response.json.return_value = {'data': {'activityCommentsV2': connection([
            {'id': 'comment', 'message': 'A reply', 'user': USER}])}}
        self.assertEqual('A reply', self.client.comments('activity-id', 'cursor')['nodes'][0]['message'])
        variables = self.session.post.call_args.kwargs['json']['variables']
        self.assertEqual('activity-id', variables['id'])
        self.assertEqual('cursor', variables['after'])

    def test_errors_are_safe_and_partial_data_is_not_reported_as_success(self):
        for status, code in [(401, 'signin'), (403, 'signin'), (429, 'busy'), (500, 'service'), (302, 'service')]:
            self.response.status_code = status
            with self.assertRaisesRegex(community.CommunityError, code) as caught:
                self.client.reviews(GUID)
            self.assertNotIn(self.token, str(caught.exception))
            self.response.close.assert_called()
        self.response.status_code = 200
        self.response.json.return_value = {'data': {'metadataReviewsV2': connection([])},
                                           'errors': [{'message': 'private details ' + self.token}]}
        with self.assertRaisesRegex(community.CommunityError, '^service$'):
            self.client.reviews(GUID)

    def test_transport_errors_do_not_expose_request_tokens(self):
        self.session.post.side_effect = requests.ConnectionError('secret ' + self.token)
        with self.assertRaisesRegex(community.CommunityError, '^network$') as caught:
            self.client.reviews(GUID)
        self.assertTrue(caught.exception.__suppress_context__)

    def test_malformed_data_is_not_treated_as_an_empty_page(self):
        for payload in ([], {}, {'data': {}}, {'data': {'metadataReviewsV2': None}},
                        {'data': {'metadataReviewsV2': {'nodes': [], 'pageInfo': {'hasNextPage': True}}}}):
            self.response.json.return_value = payload
            with self.assertRaises(community.CommunityError):
                self.client.reviews(GUID)

    def test_discover_searches_external_movies_and_tv_and_deduplicates(self):
        item = {'guid': GUID, 'type': 'movie', 'title': 'A movie'}
        response = self.session.get.return_value
        response.status_code = 200
        response.json.return_value = {'MediaContainer': {'SearchResults': [
            {'SearchResult': [{'Metadata': item}, {'Metadata': item},
                              {'Metadata': {'type': 'track'}}, {'Metadata': {}}]}]}}
        self.assertEqual([item], self.client.discover(' A movie '))
        kwargs = self.session.get.call_args.kwargs
        self.assertEqual('discover', kwargs['params']['searchProviders'])
        self.assertEqual('movies,tv', kwargs['params']['searchTypes'])
        self.assertEqual('A movie', kwargs['params']['query'])
        self.assertFalse(kwargs['allow_redirects'])
        response.close.assert_called_once()

    def test_blank_search_does_not_make_a_request(self):
        self.assertEqual([], self.client.discover('  '))
        self.session.get.assert_not_called()

    def test_profile_privacy_returns_unavailable(self):
        self.response.json.return_value = {'data': {'userByUsername': None}}
        with self.assertRaisesRegex(community.CommunityError, 'unavailable'):
            self.client.profile('private-user')

    def test_friends_and_profile_reviews_use_same_account(self):
        self.response.json.return_value = {'data': {'allFriendsV2': [{'user': USER}]}}
        self.assertEqual([USER], self.client.friends())
        self.response.json.return_value = {'data': {'user': {'reviews': connection([], 'more')}}}
        self.assertEqual('more', self.client.profile_reviews('user-id')['cursor'])
        self.assertEqual('user-id', self.session.post.call_args.kwargs['json']['variables']['id'])


class BrowserTest(KodiTestCase):
    def setUp(self):
        super(BrowserTest, self).setUp()
        self.client = mock.Mock()
        self.browser = ui.CommunityBrowser(client=self.client)
        self.browser.fetch = lambda method, *args, **kwargs: method(*args, **kwargs)

    def test_spoiler_text_is_hidden_in_lists(self):
        node = activity(hasSpoilers=True, message='The ending is revealed')
        self.assertNotIn('ending', ui.activity_preview(node))

    def test_declining_spoilers_never_displays_text_or_requests_discussion(self):
        ENV.dialog_answers.append(False)
        self.browser.read_activity(activity(hasSpoilers=True))
        self.assertEqual(['yesno'], [call[0] for call in ENV.dialog_calls])
        self.client.comments.assert_not_called()

    def test_revealing_a_review_is_remembered_only_for_this_browser(self):
        node = activity(hasSpoilers=True)
        ENV.dialog_answers.extend([True, None, -1, None, -1])
        self.browser.read_activity(node)
        self.browser.read_activity(node)
        self.assertEqual(1, len([call for call in ENV.dialog_calls if call[0] == 'yesno']))
        self.assertTrue(ui.CommunityBrowser(client=self.client).revealed == set())

    def test_untrusted_kodi_markup_is_displayed_as_text(self):
        rendered = ui.text('[B]Review[/B] [COLOR red]spoiler[/COLOR]')
        self.assertNotIn('[B]', rendered)
        self.assertNotIn('[COLOR', rendered)
        self.assertIn('Review', rendered)

    def test_next_and_previous_preserve_selection_without_refetching(self):
        load = mock.Mock(side_effect=[{'nodes': [activity()], 'cursor': 'page-2'},
                                      {'nodes': [activity(id='review-2')], 'cursor': None}])
        ENV.dialog_answers.extend([1, 1, -1])
        self.browser.pages('Reviews', load, lambda nodes: [('Review', '') for n in nodes], mock.Mock())
        self.assertEqual([mock.call(None), mock.call('page-2')], load.call_args_list)
        calls = [call for call in ENV.dialog_calls if call[0] == 'select']
        self.assertEqual(1, calls[-1][2]['preselect'])

    def test_failed_next_page_keeps_current_page_and_allows_retry(self):
        load = mock.Mock(side_effect=[{'nodes': [activity()], 'cursor': 'page-2'},
                                      community.CommunityError('network'),
                                      {'nodes': [], 'cursor': None}])
        # Next, acknowledge the error, retry Next, Back out of empty second page.
        ENV.dialog_answers.extend([1, None, 1, -1])
        self.browser.pages('Reviews', load, lambda nodes: [('Review', '') for n in nodes], mock.Mock())
        self.assertEqual([mock.call(None), mock.call('page-2'), mock.call('page-2')], load.call_args_list)

    def test_empty_filtered_page_can_still_advance(self):
        load = mock.Mock(side_effect=[{'nodes': [], 'cursor': 'page-2'},
                                      {'nodes': [activity()], 'cursor': None}])
        ENV.dialog_answers.extend([0, -1])
        self.browser.pages('Reviews', load, lambda nodes: [('Review', '') for n in nodes], mock.Mock())
        self.assertEqual(2, load.call_count)

    def test_nonadvancing_cursor_does_not_offer_endless_next(self):
        load = mock.Mock(side_effect=[{'nodes': [], 'cursor': 'same'}, {'nodes': [], 'cursor': 'same'}])
        ENV.dialog_answers.extend([0, -1])
        self.browser.pages('Reviews', load, lambda nodes: [], mock.Mock())
        self.assertEqual(2, load.call_count)
        last_rows = [call for call in ENV.dialog_calls if call[0] == 'select'][-1][1][1]
        self.assertEqual(1, len(last_rows))  # Previous page only.

    def test_opening_external_title_uses_watchlist_availability_not_direct_playback(self):
        from plexnet import plexapp
        from lib.windows import opener
        server = mock.Mock()
        with mock.patch.object(plexapp, 'SERVERMANAGER') as manager, \
                mock.patch.object(opener, 'open', return_value='') as open_item:
            manager.getDiscoverServer.return_value = server
            self.browser.open_title({'guid': GUID})
        server.getObject.assert_called_once_with('/library/metadata/' + community.metadata_id(GUID))
        open_item.assert_called_once_with(server.getObject.return_value, from_watchlist=True,
                                          directly_from_watchlist=False)

    def test_removed_discover_title_shows_an_unavailable_error(self):
        from plexnet import plexapp, exceptions
        for failure in (exceptions.BadRequest('404'), IndexError(), TypeError()):
            with mock.patch.object(plexapp, 'SERVERMANAGER') as manager:
                manager.getDiscoverServer.return_value.getObject.side_effect = failure
                with self.assertRaisesRegex(community.CommunityError, 'unavailable'):
                    self.browser.open_title({'guid': GUID})

    def test_title_options_only_offer_community_for_modern_plex_guids(self):
        self.assertIsNone(ui.title_option(mock.Mock(guid='123')))
        self.assertEqual('community_reviews', ui.title_option(mock.Mock(guid=GUID))['key'])

    def test_home_navigation_leaves_nested_community_pages(self):
        from plexnet import plexapp
        from lib.windows import opener
        self.browser.parent = mock.Mock()
        with mock.patch.object(plexapp, 'SERVERMANAGER'), \
                mock.patch.object(opener, 'open', return_value='HOME'):
            with self.assertRaises(ui._LeaveCommunity):
                self.browser.open_title({'guid': GUID})
        self.browser.parent.processCommand.assert_called_once_with('HOME')

    def test_close_account_client_when_backing_out(self):
        with mock.patch.object(ui.api, 'client_for_account', return_value=self.client):
            ui.show_home(mock.Mock())
        self.client.close.assert_called_once()


class DiscoverReviewMenuTest(KodiTestCase):
    def test_discover_menu_reads_reviews_without_server_mutations(self):
        from lib.windows.preplay import PrePlayWindowWL
        window = mock.Mock(video=mock.Mock(guid=GUID))
        with mock.patch.object(ui, 'show_reviews') as show, \
                mock.patch('lib.windows.dropdown.showDropdown') as dropdown:
            PrePlayWindowWL.optionsButtonClicked(window)
        show.assert_called_once_with(window.video, parent=window)
        dropdown.assert_not_called()

    def test_unmatched_discover_title_does_not_open_reviews(self):
        from lib.windows.preplay import PrePlayWindowWL
        window = mock.Mock(video=mock.Mock(guid='123'))
        with mock.patch.object(ui, 'show_reviews') as show:
            PrePlayWindowWL.optionsButtonClicked(window)
        show.assert_not_called()
