# coding=utf-8
"""Authentication, privacy, pagination, spoilers and navigation of online Plex data."""
from unittest import mock

import requests
from kodienv import ENV

from lib import reviews as api
from lib.windows import reviews as ui
from .base import KodiTestCase

GUID = 'plex://movie/5d7769cefb0d55001f530acd'
USER = {'id': 'user-1', 'username': 'example', 'displayName': 'Example',
        'isBlocked': False, 'isMuted': False, 'isHidden': False}


def activity(**kwargs):
    value = {'id': 'review-1', 'userV2': dict(USER), 'message': 'A thoughtful review',
             'hasSpoilers': False, 'commentCount': 4, 'reviewRating': 8}
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
        self.account = mock.Mock(authToken=self.token, isManaged=False)
        self.account_patch = mock.patch.object(api.plexapp, 'ACCOUNT', self.account)
        self.mode_patch = mock.patch.object(api.util, 'LOCAL_MODE', False)
        self.account_patch.start()
        self.mode_patch.start()
        self.addCleanup(self.account_patch.stop)
        self.addCleanup(self.mode_patch.stop)
        with mock.patch.object(api.requests, 'Session', return_value=self.session):
            self.client = api.ReviewsClient()

    def test_uses_account_header_and_current_user_on_every_request(self):
        self.client.reviews(GUID)
        args, kwargs = self.session.post.call_args
        self.assertEqual(api.COMMUNITY_URL, args[0])
        self.assertNotIn(self.token, args[0])
        self.assertEqual(self.token, kwargs['headers']['X-Plex-Token'])
        self.assertEqual('5d7769cefb0d55001f530acd', kwargs['json']['variables']['id'])
        self.assertEqual((5, 15), kwargs['timeout'])
        self.assertFalse(kwargs['allow_redirects'])
        self.token = self.account.authToken = 'different-account'
        self.client.reviews(GUID)
        self.assertEqual(self.token, self.session.post.call_args.kwargs['headers']['X-Plex-Token'])

    def test_local_mode_and_missing_login_never_contact_plex(self):
        for offline, managed, token, code in [(True, False, self.token, 'offline'),
                                               (False, True, self.token, 'offline'),
                                               (False, False, None, 'signin')]:
            api.util.LOCAL_MODE = offline
            self.account.isManaged, self.account.authToken = managed, token
            with self.assertRaisesRegex(api.ReviewsError, code):
                self.client.reviews(GUID)
        self.session.post.assert_not_called()

    def test_legacy_agents_do_not_send_server_rating_keys_to_community(self):
        for guid in ('123', 'com.plexapp.agents.imdb://tt123', 'plex://movie/123',
                     GUID + '?token=secret', None):
            with self.assertRaisesRegex(api.ReviewsError, 'metadata'):
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
            with self.assertRaisesRegex(api.ReviewsError, code) as caught:
                self.client.reviews(GUID)
            self.assertNotIn(self.token, str(caught.exception))
            self.response.close.assert_called()
        self.response.status_code = 200
        self.response.json.return_value = {'data': {'metadataReviewsV2': connection([])},
                                           'errors': [{'message': 'private details ' + self.token}]}
        with self.assertRaisesRegex(api.ReviewsError, '^service$'):
            self.client.reviews(GUID)

    def test_transport_errors_do_not_expose_request_tokens(self):
        self.session.post.side_effect = requests.ConnectionError('secret ' + self.token)
        with self.assertRaisesRegex(api.ReviewsError, '^network$') as caught:
            self.client.reviews(GUID)
        self.assertTrue(caught.exception.__suppress_context__)

    def test_malformed_data_is_not_treated_as_an_empty_page(self):
        for payload in ([], {}, {'data': {}}, {'data': {'metadataReviewsV2': None}},
                        {'data': {'metadataReviewsV2': {'nodes': [], 'pageInfo': {'hasNextPage': True}}}},
                        {'data': {'metadataReviewsV2': {'nodes': [], 'pageInfo': 'invalid'}}}):
            self.response.json.return_value = payload
            with self.assertRaises(api.ReviewsError):
                self.client.reviews(GUID)


class BrowserTest(KodiTestCase):
    def setUp(self):
        super(BrowserTest, self).setUp()
        self.client = mock.Mock()
        with mock.patch.object(api, 'ReviewsClient', return_value=self.client):
            self.browser = ui.ReviewsBrowser()
        self.browser.fetch = lambda method, *args, **kwargs: method(*args, **kwargs)

    def test_spoiler_text_is_hidden_in_lists(self):
        node = activity(hasSpoilers=True, message='The ending is revealed')
        self.assertNotIn('ending', ui.review_item(node).getProperty('text'))

    def test_declining_spoilers_never_displays_text_or_requests_discussion(self):
        ENV.dialog_answers.append(False)
        self.browser.open_review(activity(hasSpoilers=True), mock.Mock())
        self.assertEqual(['yesno'], [call[0] for call in ENV.dialog_calls])
        self.client.comments.assert_not_called()

    def test_revealing_a_review_is_remembered_only_for_this_browser(self):
        node = activity(hasSpoilers=True)
        ENV.dialog_answers.append(True)
        with mock.patch('lib.windows.reviews.ReviewWindow.open') as reader:
            self.browser.open_review(node, mock.Mock())
            self.browser.open_review(node, mock.Mock())
        self.assertEqual(2, reader.call_count)
        self.assertEqual(1, len([call for call in ENV.dialog_calls if call[0] == 'yesno']))
        with mock.patch.object(api, 'ReviewsClient', return_value=self.client):
            self.assertEqual(set(), ui.ReviewsBrowser().revealed)

    def test_untrusted_kodi_markup_is_displayed_as_text(self):
        rendered = ui.text('[B]Review[/B] [COLOR red]spoiler[/COLOR]')
        self.assertNotIn('[B]', rendered)
        self.assertNotIn('[COLOR', rendered)
        self.assertIn('Review', rendered)


    def test_title_options_require_modern_plex_guids(self):
        self.assertIsNone(ui.title_option(mock.Mock(guid='123')))
        self.assertEqual('plex_reviews', ui.title_option(mock.Mock(guid=GUID))['key'])

    def test_fetch_reports_api_failure_without_returning_a_page(self):
        with mock.patch.object(ui.busy, 'widthDialog', side_effect=api.ReviewsError('network')):
            self.assertIsNone(ui.ReviewsBrowser.fetch(self.browser, self.client.reviews, GUID))
        self.assertEqual(['ok'], [call[0] for call in ENV.dialog_calls])

    def test_client_is_closed_when_review_window_fails(self):
        with mock.patch.object(ui.api, 'ReviewsClient', return_value=self.client), \
                mock.patch.object(ui.ReviewsWindow, 'open', side_effect=RuntimeError('window')):
            with self.assertRaises(RuntimeError):
                ui.show_reviews(mock.Mock(guid=GUID))
        self.client.close.assert_called_once_with()


class InlineReviewTest(KodiTestCase):
    def setUp(self):
        super(InlineReviewTest, self).setUp()
        critic = mock.Mock(source='Critic', tag='Positive', text='Critic review')
        critic.ratingImage.return_value = 'review.fresh'
        self.video = mock.Mock(guid=GUID, isFullyWatched=False)
        self.video.reviews.return_value = [critic]
        self.window = mock.Mock(video=self.video)
        self.window.closing.return_value = False
        self.client = mock.Mock()

    def fill(self):
        from lib.windows.preplay import PrePlayWindow
        with mock.patch.object(ui.api, 'ReviewsClient', return_value=self.client), \
                mock.patch.object(ui.util, 'getSetting', return_value=['watched', 'unwatched']):
            return PrePlayWindow.fillReviews(self.window)

    def test_online_failure_still_displays_critic_reviews(self):
        self.client.reviews.side_effect = api.ReviewsError('network')
        self.assertTrue(self.fill())
        items = self.window.reviewsListControl.addItems.call_args.args[0]
        self.assertEqual(['Critic'], [item.getLabel() for item in items])
        self.client.close.assert_called_once_with()

    def test_title_change_discards_late_review_results(self):
        def change_title(*args):
            self.window.video = mock.Mock(guid=GUID)
            return {'nodes': [activity()], 'cursor': None}
        self.client.reviews.side_effect = change_title
        self.assertFalse(self.fill())
        self.window.reviewsListControl.reset.assert_not_called()
        self.window.reviewsListControl.addItems.assert_not_called()
        self.client.close.assert_called_once_with()

    def test_review_cards_and_browse_action_precede_existing_critics(self):
        self.client.reviews.return_value = {'nodes': [activity()], 'cursor': 'more'}
        self.assertTrue(self.fill())
        items = self.window.reviewsListControl.addItems.call_args.args[0]
        self.assertEqual('1', items[0].getProperty('user.review'))
        self.assertEqual('1', items[1].getProperty('browse'))
        self.assertEqual('Critic', items[2].getLabel())


class WatchlistReviewMenuTest(KodiTestCase):
    def test_watchlist_menu_reads_reviews_without_server_mutations(self):
        from lib.windows.preplay import PrePlayWindowWL
        window = mock.Mock(video=mock.Mock(guid=GUID))
        with mock.patch.object(ui, 'show_reviews') as show, \
                mock.patch('lib.windows.dropdown.showDropdown') as dropdown:
            PrePlayWindowWL.optionsButtonClicked(window)
        show.assert_called_once_with(window.video, parent=window)
        dropdown.assert_not_called()

    def test_unmatched_watchlist_title_does_not_open_reviews(self):
        from lib.windows.preplay import PrePlayWindowWL
        window = mock.Mock(video=mock.Mock(guid='123'))
        with mock.patch.object(ui, 'show_reviews') as show:
            PrePlayWindowWL.optionsButtonClicked(window)
        show.assert_not_called()


class ReviewPresentationTest(KodiTestCase):
    def test_star_texture_uses_ten_half_steps_and_handles_missing_rating(self):
        from lib.windows.reviews import star_texture
        self.assertTrue(star_texture(10).endswith('/10.png'))
        self.assertTrue(star_texture(9).endswith('/9.png'))
        for value in (None, '8', float('nan'), float('inf'), -1, 11, True):
            self.assertEqual('', star_texture(value))

    def test_review_cards_escape_text_and_hide_spoilers(self):
        from lib.windows.reviews import review_item
        item = review_item(activity(hasSpoilers=True, message='secret ending', rating=8,
                                    date='2025-01-26T00:00:00Z',
                                    userV2=dict(USER, displayName='[B]Example[/B]')))
        self.assertNotIn('secret', item.getProperty('text'))
        self.assertTrue(item.getProperty('star.texture').endswith('/8.png'))
        self.assertEqual('Discussion (4)', item.getProperty('discussion'))
        self.assertNotIn('[B]', item.getLabel())
        self.assertEqual('Jan 26, 2025', item.getLabel2())

    def test_remote_avatar_cannot_read_local_paths(self):
        from lib.windows.reviews import avatar_url
        for value in ('file:///C:/secret', 'special://profile/foo', 'http://example.com/a',
                      'https://user:pass@example.com/a', None, {}):
            self.assertEqual('', avatar_url(value))
        self.assertEqual('https://example.com/a', avatar_url('https://example.com/a'))

    def test_failed_review_page_preserves_cursor_and_cards(self):
        from lib.windows.reviews import ReviewsWindow
        window = mock.Mock(cursor='old', current={'nodes': [activity()], 'cursor': 'next'}, sort='TOP')
        window.browser.fetch.return_value = None
        self.assertFalse(ReviewsWindow.load_page(window, 'next'))
        self.assertEqual('old', window.cursor)
        self.assertEqual('next', window.current['cursor'])
        window.render_page.assert_not_called()

    def test_next_then_previous_restores_review_selection(self):
        from lib.windows.reviews import ReviewsWindow
        current = {'nodes': [activity()], 'cursor': 'next'}
        window = mock.Mock(cursor=None, current=current, history=[])
        window.cards.getSelectedPosition.return_value = 5
        window.load_page.return_value = True
        ReviewsWindow.onClick(window, 306)
        self.assertEqual([(None, current, 5)], window.history)
        ReviewsWindow.onClick(window, 305)
        window.render_page.assert_called_once_with(5)
        self.assertEqual([], window.history)


class ReactionClientTest(KodiTestCase):
    def setUp(self):
        super(ReactionClientTest, self).setUp()
        self.session = mock.Mock()
        self.response = self.session.post.return_value
        self.response.status_code = 200
        self.state = {'reaction': 'LIKE', 'reactionsCount': '35', 'reactionsTypes': ['LIKE', 'LOVE']}
        self.response.json.return_value = {'data': {'reactToActivity': self.state}}
        account = mock.patch.object(api.plexapp, 'ACCOUNT', mock.Mock(authToken='test-token', isManaged=False))
        mode = mock.patch.object(api.util, 'LOCAL_MODE', False)
        account.start()
        mode.start()
        self.addCleanup(account.stop)
        self.addCleanup(mode.stop)
        with mock.patch.object(api.requests, 'Session', return_value=self.session):
            self.client = api.ReviewsClient()

    def test_set_replace_and_remove_use_activity_id_and_nullable_type(self):
        for kind in ('LIKE', 'LOVE', None):
            state = dict(self.state, reaction=kind)
            self.response.json.return_value = {'data': {'reactToActivity': state}}
            result = self.client.react('review-id', kind)
            self.assertEqual(kind, result['reaction'])
            self.assertEqual(35, result['reactionsCount'])
            sent = self.session.post.call_args.kwargs['json']
            self.assertIn('mutation ', sent['query'])
            self.assertEqual({'input': {'activity': 'review-id', 'type': kind}}, sent['variables'])

    def test_unsupported_reactions_do_not_contact_plex(self):
        for value in ('HEART', '', 123, {}):
            with self.assertRaises(ValueError):
                self.client.react('id', value)
        with self.assertRaises(ValueError):
            self.client.react('', 'LIKE')
        self.session.post.assert_not_called()

    def test_uncertain_write_never_retries(self):
        self.session.post.side_effect = requests.Timeout()
        with self.assertRaisesRegex(api.ReviewsError, 'network'):
            self.client.react('id', 'LOVE')
        self.assertEqual(1, self.session.post.call_count)

    def test_offline_profile_cannot_react(self):
        api.util.LOCAL_MODE = True
        with self.assertRaisesRegex(api.ReviewsError, 'offline'):
            self.client.react('id', 'LIKE')
        self.session.post.assert_not_called()

    def test_read_and_write_share_server_authoritative_state(self):
        self.response.json.return_value = {'data': {'activityByID': self.state}}
        self.assertEqual(35, self.client.reactions('id')['reactionsCount'])
        for field, value in [('reaction', 'UNKNOWN'), ('reactionsCount', '-1'),
                             ('reactionsCount', True), ('reactionsTypes', ['UNKNOWN'])]:
            with self.assertRaises(api.ReviewsError):
                api.reaction_state(dict(self.state, **{field: value}))


class ReactionWindowTest(KodiTestCase):
    def test_failure_reconciles_without_optimistic_counts(self):
        from lib.windows.reviews import ReviewWindow
        original = {'id': 'review', 'reaction': 'LOVE', 'reactionsCount': 4, 'reactionsTypes': ['LOVE']}
        window = mock.Mock(reply=False, reacting=False, reactionKnown=True, node=dict(original))
        window.browser.fetch.return_value = None
        ReviewWindow.react(window, 'LIKE')
        self.assertEqual(original, window.node)
        window.render_reactions.assert_not_called()
        window.refresh_reactions.assert_called_once_with()
        self.assertFalse(window.reacting)

    def test_success_uses_returned_count_not_local_arithmetic(self):
        from lib.windows.reviews import ReviewWindow
        window = mock.Mock(reply=False, reacting=False, reactionKnown=True, node={'id': 'review'})
        window.browser.fetch.return_value = {'reaction': 'LIKE', 'reactionsCount': 42, 'reactionsTypes': ['LIKE']}
        ReviewWindow.react(window, 'LIKE')
        self.assertEqual(42, window.node['reactionsCount'])
        window.render_reactions.assert_called_once_with()

    def test_unknown_state_reply_and_duplicate_click_do_not_write(self):
        from lib.windows.reviews import ReviewWindow
        for values in ({'reply': True}, {'reacting': True}, {'reactionKnown': False}):
            base = dict(reply=False, reacting=False, reactionKnown=True)
            base.update(values)
            window = mock.Mock(**base)
            ReviewWindow.react(window, 'LIKE')
            window.browser.fetch.assert_not_called()

    def test_selected_emoji_toggles_off_and_cancel_does_nothing(self):
        from lib.windows.reviews import ReviewWindow, ReactionPicker
        window = mock.Mock(reply=False, reacting=False, reactionKnown=True, node={'reaction': 'LOVE'})
        with mock.patch.object(ReactionPicker, 'open') as picker:
            picker.return_value.result = None
            ReviewWindow.pick_reaction(window)
            window.react.assert_not_called()
            picker.return_value.result = ('LOVE',)
            ReviewWindow.pick_reaction(window)
            window.react.assert_called_once_with(None)

    def test_card_totals_and_current_emoji_update_in_place(self):
        from lib.windows.reviews import review_item, update_reaction_properties
        node = activity(reaction='LOVE', reactionsCount='34', reactionsTypes=['LOVE', 'APPLAUD', 'LIKE'])
        item = review_item(node)
        self.assertEqual('34', item.getProperty('reaction.count'))
        self.assertTrue(item.getProperty('reaction.mine').endswith('/love.png'))
        node.update(reaction=None, reactionsCount='0', reactionsTypes=[])
        update_reaction_properties(item)
        self.assertEqual('', item.getProperty('reaction.mine'))
        self.assertEqual('', item.getProperty('reaction.icon.0'))


class ReactionPickerLifecycleTest(KodiTestCase):
    def test_controlled_dialog_accepts_window_modal_show_argument(self):
        from lib.windows.reviews import ReactionPicker
        with mock.patch('lib.windows.kodigui.BaseDialog.show') as show:
            ReactionPicker.show(mock.Mock(), aggressive=False)
        show.assert_called_once_with(mock.ANY)
