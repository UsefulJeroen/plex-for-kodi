# coding=utf-8
"""Plex-style review cards and a title/review/discussion screen."""
from __future__ import absolute_import

import datetime
import math
from urllib.parse import urlsplit

from kodi_six import xbmcgui

from lib import util, reviews as api
from lib.util import T
from . import busy, kodigui


def text(value):
    # Review text is user supplied, not Kodi formatting instructions.
    return str(value or '').replace('[', '\uff3b').replace(']', '\uff3d')


def user_name(user):
    return text(user.get('displayName') or user.get('username') or T(35124, 'Plex user'))


def activity_preview(node):
    if node.get('hasSpoilers'):
        return T(35109, 'May contain spoilers')
    message = text(node.get('message')).replace('\n', ' ')
    return message[:180] or T(35125, 'Rating without a written review')


def title_option(item):
    if api.metadata_id(getattr(item, 'guid', None)):
        return {'key': 'plex_reviews', 'display': T(35100, 'Plex user reviews')}


def show_reviews(item, parent=None):
    browser = ReviewsBrowser(parent=parent)
    try:
        ReviewsWindow.open(browser=browser, video=item)
    finally:
        browser.client.close()


class ReviewsBrowser(object):

    def __init__(self, parent=None, client=None):
        self.parent = parent
        self.client = client or api.client_for_account()
        self.revealed = set()

    def fetch(self, method, *args, **kwargs):
        try:
            return busy.widthDialog(method, None, *args, **kwargs)
        except api.ReviewsError as exc:
            messages = {
                'offline': T(35117, 'Plex user reviews require an online, full Plex account.'),
                'signin': T(35118, 'Plex did not accept this login. Check your Plex account sign-in.'),
                'network': T(35119, 'Could not connect to Plex. Please try again.'),
                'busy': T(35120, 'Plex is busy. Please try again later.'),
                'metadata': T(35121, 'This title needs a modern Plex Movie or Plex Series match.'),
                'unavailable': T(35122, 'This review is unavailable or private.'),
            }
            xbmcgui.Dialog().ok(T(35100, 'Plex user reviews'), messages.get(
                str(exc), T(35123, 'Plex could not load this page. Please try again later.')))

    def reveal(self, node):
        if not node.get('hasSpoilers') or node.get('id') in self.revealed:
            return True
        if not xbmcgui.Dialog().yesno(T(35109, 'May contain spoilers'),
                                     T(35113, 'Show this review and its discussion?')):
            return False
        self.revealed.add(node.get('id'))
        return True

    def open_review(self, node, video=None):
        if not self.reveal(node):
            return
        ReviewWindow.open(browser=self, node=node, video=video)


def date_label(value):
    try:
        date = datetime.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return date.strftime('%b %d, %Y').replace(' 0', ' ')
    except (ValueError, TypeError, OverflowError):
        return text(value)


def avatar_url(value):
    # Never let remotely supplied image paths resolve local files or Kodi protocols.
    if not isinstance(value, str):
        return ''
    try:
        url = urlsplit(value)
    except ValueError:
        return ''
    return value if url.scheme == 'https' and url.hostname and not url.username and not url.password else ''


def star_texture(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 10:
        return 'script.plex/review-stars/{}.png'.format(int(math.floor(value + 0.5)))
    return ''


REACTION_LABELS = {
    'LIKE': (35138, 'Like'), 'DISLIKE': (35139, 'Dislike'),
    'LOVE': (35140, 'Love'), 'LAUGH': (35141, 'Laugh'),
    'APPLAUD': (35142, 'Applaud'), 'QUESTION': (35143, 'Question'),
}


def reaction_icon(kind):
    return 'script.plex/reactions/{}.png'.format(kind.lower()) if kind in api.REACTION_TYPES else ''


def update_reaction_properties(item):
    node = item.dataSource or {}
    if not isinstance(node, dict):
        return
    try:
        state = api.reaction_state(node)
    except api.ReviewsError:
        state = {'reaction': None, 'reactionsCount': 0, 'reactionsTypes': []}
    item.setProperty('reaction.count', str(state['reactionsCount']) if state['reactionsCount'] else '')
    item.setProperty('reaction.mine', reaction_icon(state['reaction']))
    for index in range(3):
        types = state['reactionsTypes']
        item.setProperty('reaction.icon.' + str(index), reaction_icon(types[index]) if index < len(types) else '')


def review_item(node):
    user = node.get('userV2') or node.get('user') or {}
    item = kodigui.ManagedListItem(user_name(user), date_label(node.get('date')),
                                  thumbnailImage=avatar_url(user.get('avatar')), data_source=node)
    item.setProperty('text', activity_preview(node))
    item.setProperty('star.texture', star_texture(node.get('rating')))
    update_reaction_properties(item)
    item.setProperty('user.review', '1')
    item.setProperty('discussion', T(35115, 'Discussion') + ' ({})'.format(node.get('commentCount') or 0))
    return item


class ReviewBase(kodigui.ControlledWindow):
    path = util.ADDON.getAddonInfo('path')
    theme = 'Main'
    res = '1080i'
    width = 1920
    height = 1080
    dismissOnClose = True

    def __init__(self, *args, **kwargs):
        super(ReviewBase, self).__init__(*args, **kwargs)
        self.browser = kwargs['browser']
        self.video = kwargs.get('video')

    def title_info(self):
        video = self.video or getattr(self.browser.parent, 'video', None)
        if video is not None:
            self.setProperty('title', text(video.defaultTitle))
            self.setProperty('summary', text(video.summary))
            self.setProperty('year', text(video.year))
            self.setProperty('poster', (video.art or video.defaultThumb).asTranscodedImageURL(*util.scaleResolution(520, 292)))
        if self.browser.parent:
            self.setProperty('background', self.browser.parent.getProperty('background'))


class ReviewsWindow(ReviewBase):
    xmlFile = 'script-plex-reviews.xml'

    def __init__(self, *args, **kwargs):
        super(ReviewsWindow, self).__init__(*args, **kwargs)
        self.sort = 'TOP'
        self.cursor = None
        self.current = None
        self.history = []

    def onFirstInit(self):
        self.cards = kodigui.ManagedControlList(self, 401, 3)
        self.title_info()
        self.load_page()

    def onReInit(self):
        for item in self.cards:
            update_reaction_properties(item)

    def load_page(self, cursor=None):
        page = self.browser.fetch(self.browser.client.reviews,
                               str(self.video.guid), self.sort, cursor)
        if page is None:
            if self.current is None:
                self.setProperty('status', T(35119, 'Could not connect to Plex. Please try again.'))
                self.setFocusId(301)
            return False
        self.cursor, self.current = cursor, page
        self.render_page()
        return True

    def render_page(self, selected=0):
        self.setProperty('review.sort', self.sort)
        for order, label in [('TOP', T(35132, 'Top')), ('RECENT', T(35133, 'Recent')), ('HOT', T(35134, 'Popular')), ('FRIENDS', T(35103, 'Friends'))]:
            self.setProperty('sort.' + order, label + (' •' if order == self.sort else ''))
        self.cards.reset()
        self.cards.addItems([review_item(node) for node in self.current['nodes']])
        self.setBoolProperty('has.previous', bool(self.history))
        self.setBoolProperty('has.next', bool(self.current['cursor'] and self.current['cursor'] != self.cursor))
        self.setProperty('status', '' if self.current['nodes'] else T(35112, 'Nothing to show here yet, or this content is private.'))
        if self.current['nodes']:
            self.cards.selectItem(selected)
            self.setFocusId(401)
        else:
            self.setFocusId(301)

    def onClick(self, controlID):
        if controlID == 401:
            item = self.cards.getSelectedItem()
            if item:
                self.browser.open_review(item.dataSource, self.video)
        elif controlID in (301, 302, 303, 304):
            order = {301: 'TOP', 302: 'RECENT', 303: 'HOT', 304: 'FRIENDS'}[controlID]
            old = self.sort
            self.sort = order
            if self.load_page():
                self.history = []
                self.setProperty('has.previous', '')
            else:
                self.sort = old
        elif controlID == 305 and self.history:
            self.cursor, self.current, selected = self.history.pop()
            self.render_page(selected)
        elif controlID == 306 and self.current and self.current['cursor'] != self.cursor:
            previous = (self.cursor, self.current, self.cards.getSelectedPosition())
            if self.load_page(self.current['cursor']):
                self.history.append(previous)
                self.setProperty('has.previous', '1')
        elif controlID == 307:
            self.doClose()


class ReviewWindow(ReviewBase):
    xmlFile = 'script-plex-review.xml'

    def __init__(self, *args, **kwargs):
        super(ReviewWindow, self).__init__(*args, **kwargs)
        self.node = kwargs['node']
        self.reply = kwargs.get('reply', False)
        self.cursor = None
        self.current = None
        self.history = []
        self.reactionKnown = False
        self.reacting = False

    def onFirstInit(self):
        self.comments = kodigui.ManagedControlList(self, 410, 2)
        self.title_info()
        user = self.node.get('userV2') or self.node.get('user') or {}
        self.setProperty('author', user_name(user))
        self.setProperty('avatar', avatar_url(user.get('avatar')))
        self.setProperty('date', date_label(self.node.get('date')))
        self.setProperty('star.texture', star_texture(self.node.get('rating')))
        self.setBoolProperty('is.reply', self.reply)
        self.setProperty('review', text(self.node.get('message')) or T(35125, 'Rating without a written review'))
        self.setProperty('discussion', T(35115, 'Discussion') + ' ({})'.format(self.node.get('commentCount') or 0))
        if not self.getProperty('title'):
            self.setProperty('title', text((self.node.get('metadataItem') or {}).get('title')))
        if not self.reply:
            self.refresh_reactions()
            self.load_comments()
        self.setFocusId(152)

    def render_reactions(self):
        state = api.reaction_state(self.node)
        self.setBoolProperty('reaction.known', self.reactionKnown)
        self.setBoolProperty('reaction.mine', bool(state['reaction']))
        self.setProperty('reaction.count', str(state['reactionsCount']))
        current = state['reaction']
        self.setProperty('reaction.action', T(*REACTION_LABELS[current or 'LIKE']))
        self.setProperty('reaction.current.icon', reaction_icon(current or 'LIKE'))
        for index in range(3):
            types = state['reactionsTypes']
            self.setProperty('reaction.icon.' + str(index), reaction_icon(types[index]) if index < len(types) else '')

    def refresh_reactions(self):
        state = self.browser.fetch(self.browser.client.reactions, self.node['id'])
        self.reactionKnown = state is not None
        self.setBoolProperty('reaction.known', self.reactionKnown)
        if state is not None:
            self.node.update(state)
            self.render_reactions()
        return self.reactionKnown

    def react(self, reaction):
        if self.reply or self.reacting or not self.reactionKnown:
            return
        self.reacting = True
        self.setBoolProperty('reaction.busy', True)
        try:
            state = self.browser.fetch(self.browser.client.react, self.node['id'], reaction)
            if state is not None:
                self.node.update(state)
                self.render_reactions()
            else:
                # Reconcile uncertain outcomes instead of blindly retrying a write.
                self.refresh_reactions()
        finally:
            self.reacting = False
            self.setProperty('reaction.busy', '')

    def pick_reaction(self):
        if self.reply or self.reacting:
            return
        if not self.reactionKnown and not self.refresh_reactions():
            return
        picker = ReactionPicker.open(current=self.node.get('reaction'))
        if picker.result is not None:
            kind = picker.result[0]
            self.react(None if kind == self.node.get('reaction') else kind)

    def load_comments(self, cursor=None):
        page = self.browser.fetch(self.browser.client.comments, self.node['id'], cursor)
        if page is None:
            if self.current is None:
                self.setProperty('comment.status', T(35119, 'Could not connect to Plex. Please try again.'))
            return False
        self.cursor, self.current = cursor, page
        self.render_comments()
        return True

    def render_comments(self, selected=0):
        self.comments.reset()
        items = []
        for node in self.current['nodes']:
            item = review_item(node)
            item.setProperty('text', text(node.get('message')))
            items.append(item)
        self.comments.addItems(items)
        if items:
            self.comments.selectItem(selected)
        self.setProperty('comment.status', '' if items else T(35112, 'Nothing to show here yet, or this content is private.'))
        self.setBoolProperty('has.next', bool(self.current['cursor'] and self.current['cursor'] != self.cursor))
        self.setBoolProperty('has.previous', bool(self.history))

    def onClick(self, controlID):
        if controlID == 410:
            item = self.comments.getSelectedItem()
            if item:
                # Reuse the styled reader for long replies; Back restores the discussion.
                ReviewWindow.open(browser=self.browser, node=dict(item.dataSource, commentCount=0), video=self.video, reply=True)
        elif controlID == 305 and self.history:
            self.cursor, self.current, selected = self.history.pop()
            self.render_comments(selected)
        elif controlID == 306 and self.current and self.current['cursor'] and self.current['cursor'] != self.cursor:
            previous = (self.cursor, self.current, self.comments.getSelectedPosition())
            if self.load_comments(self.current['cursor']):
                self.history.append(previous)
                self.setProperty('has.previous', '1')
        elif controlID == 307:
            self.doClose()
        elif controlID == 308 and not self.reply:
            self.refresh_reactions()
            self.load_comments(self.cursor)
        elif controlID == 310:
            self.react(None if self.node.get('reaction') else 'LIKE')
        elif controlID == 311:
            self.pick_reaction()
        elif controlID == 312:
            self.react(None)


class ReactionPicker(kodigui.ControlledDialog):
    xmlFile = 'script-plex-reaction_picker.xml'
    path = util.ADDON.getAddonInfo('path')
    theme = 'Main'
    res = '1080i'
    width = 1920
    height = 1080

    def __init__(self, *args, **kwargs):
        super(ReactionPicker, self).__init__(*args, **kwargs)
        self.current = kwargs.get('current')
        self.result = None

    def show(self, aggressive=False):
        # ControlledBase passes a window argument that native dialogs do not accept.
        kodigui.BaseDialog.show(self)

    def onFirstInit(self):
        for index, kind in enumerate(api.REACTION_TYPES):
            self.setProperty('label.' + kind, T(*REACTION_LABELS[kind]))
            self.setBoolProperty('selected.' + kind, self.current == kind)
        self.setBoolProperty('has.reaction', bool(self.current))
        self.setFocusId(500 + api.REACTION_TYPES.index(self.current) if self.current in api.REACTION_TYPES else 500)

    def onClick(self, controlID):
        if 500 <= controlID < 506:
            self.result = (api.REACTION_TYPES[controlID - 500],)
        elif controlID == 506 and self.current:
            self.result = (None,)
        elif controlID != 507:
            return
        self.doClose()
