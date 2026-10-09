# coding=utf-8
"""Remote-friendly browsing of Plex reviews, discussions, friends and Discover."""
from __future__ import absolute_import

from kodi_six import xbmcgui

from lib import community as api
from lib.i18n import T
from . import busy


def text(value):
    # Community text is user supplied, not Kodi formatting instructions.
    return str(value or '').replace('[', '\uff3b').replace(']', '\uff3d')


def user_name(user):
    return text(user.get('displayName') or user.get('username') or T(35124, 'Plex user'))


def activity_label(node):
    author = user_name(node.get('userV2') or node.get('user') or {})
    rating = node.get('rating')
    if isinstance(rating, (int, float)):
        author += ' - {:g}/10'.format(rating)
    title = text((node.get('metadataItem') or {}).get('title'))
    return author + (' - ' + title if title else '')


def activity_preview(node):
    if node.get('hasSpoilers'):
        return T(35109, 'May contain spoilers')
    message = text(node.get('message')).replace('\n', ' ')
    return message[:180] or T(35125, 'Rating without a written review')


def title_option(item):
    if api.metadata_id(getattr(item, 'guid', None)):
        return {'key': 'community_reviews', 'display': T(35100, 'Plex user reviews')}


class _LeaveCommunity(Exception):
    pass


def show_reviews(item, parent=None):
    from .reviews import ReviewsWindow
    browser = CommunityBrowser(parent=parent)
    try:
        browser.run(ReviewsWindow.open, browser=browser, video=item)
    finally:
        browser.client.close()


def show_home(parent):
    browser = CommunityBrowser(parent=parent)
    try:
        browser.run(browser.home)
    except _LeaveCommunity:
        pass
    finally:
        browser.client.close()


class CommunityBrowser(object):
    def __init__(self, parent=None, client=None):
        self.parent = parent
        self.client = client or api.client_for_account()
        self.revealed = set()

    def run(self, method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except api.CommunityError as exc:
            messages = {
                'offline': T(35117, 'Plex community requires an online, full Plex account.'),
                'signin': T(35118, 'Plex did not accept this login. Check your Plex account sign-in.'),
                'network': T(35119, 'Could not connect to Plex. Please try again.'),
                'busy': T(35120, 'Plex is busy. Please try again later.'),
                'metadata': T(35121, 'This title needs a modern Plex Movie or Plex Series match.'),
                'unavailable': T(35122, 'This profile or activity is unavailable or private.'),
            }
            xbmcgui.Dialog().ok(T(35101, 'Plex community'), messages.get(
                str(exc), T(35123, 'Plex could not load this page. Please try again later.')))

    def fetch(self, method, *args, **kwargs):
        # A bounded request under PM4K's existing loading dialog, only on demand.
        return busy.widthDialog(method, None, *args, **kwargs)

    def select(self, heading, rows, selected=0):
        items = []
        for label, detail in rows:
            item = xbmcgui.ListItem(label=label, label2=detail)
            items.append(item)
        return xbmcgui.Dialog().select(heading, items, useDetails=True, preselect=selected)

    def home(self):
        labels = [T(35102, 'Discover movies and shows'), T(35103, 'Friends'),
                  T(35104, 'Friends activity')]
        while True:
            choice = xbmcgui.Dialog().select(T(35101, 'Plex community'), labels)
            if choice < 0:
                return
            self.run([self.discover, self.friends, self.activity][choice])

    def reviews(self, guid, title):
        orders = [('RECENT', T(35105, 'Recent reviews')), ('TOP', T(35106, 'Top reviews')),
                  ('HOT', T(35107, 'Popular reviews')), ('FRIENDS', T(35108, 'Friends reviews'))]
        while True:
            choice = xbmcgui.Dialog().select(T(35100, 'Plex user reviews') + ' - ' + title,
                                            [order[1] for order in orders])
            if choice < 0:
                return
            sort, label = orders[choice]
            self.run(self.activities, label + ' - ' + title,
                     lambda cursor: self.client.reviews(guid, sort, cursor))

    def activities(self, heading, load):
        def rows(nodes):
            return [(activity_label(node), activity_preview(node)) for node in nodes]
        self.pages(heading, load, rows, self.read_activity)

    def pages(self, heading, load, make_rows, open_node):
        cursor, history, selected = None, [], 0
        current = self.fetch(load, cursor)
        while True:
            nodes = current['nodes']
            rows = make_rows(nodes)
            actions = []
            if history:
                actions.append(('previous', T(35111, 'Previous page')))
            if current['cursor'] and current['cursor'] != cursor:
                actions.append(('next', T(35110, 'Next page')))
            rows += [(label, '') for _, label in actions]
            if not rows:
                xbmcgui.Dialog().ok(heading, T(35112, 'Nothing to show here yet, or this content is private.'))
                return
            index = self.select(heading, rows, min(selected, len(rows) - 1))
            if index < 0:
                return
            selected = index
            if index < len(nodes):
                self.run(open_node, nodes[index])
            elif actions[index - len(nodes)][0] == 'previous':
                cursor, current, selected = history.pop()
            else:
                # Keep the displayed page if a request fails, so Back and retry work.
                next_cursor = current['cursor']
                next_page = self.run(self.fetch, load, next_cursor)
                if next_page is not None:
                    history.append((cursor, current, selected))
                    cursor, current, selected = next_cursor, next_page, 0

    def reveal(self, node):
        if not node.get('hasSpoilers') or node.get('id') in self.revealed:
            return True
        if not xbmcgui.Dialog().yesno(T(35109, 'May contain spoilers'),
                                     T(35113, 'Show this review and its discussion?')):
            return False
        self.revealed.add(node.get('id'))
        return True

    def read_activity(self, node):
        if not self.reveal(node):
            return
        from .reviews import ReviewWindow
        ReviewWindow.open(browser=self, node=node)

    def comments(self, activity_id, title):
        def rows(nodes):
            return [(user_name(node.get('user') or {}), text(node.get('message')).replace('\n', ' ')[:180])
                    for node in nodes]

        def read(node):
            xbmcgui.Dialog().textviewer(user_name(node.get('user') or {}),
                                       text(node.get('date')) + '\n\n' + text(node.get('message')))
        self.pages(T(35115, 'Discussion') + ' - ' + title,
                   lambda cursor: self.client.comments(activity_id, cursor), rows, read)

    def friends(self):
        users = self.fetch(self.client.friends)
        if not users:
            xbmcgui.Dialog().ok(T(35103, 'Friends'), T(35112, 'Nothing to show here yet, or this content is private.'))
            return
        selected = 0
        while True:
            selected = self.select(T(35103, 'Friends'),
                                   [(user_name(user), text(user.get('username'))) for user in users], selected)
            if selected < 0:
                return
            self.run(self.profile, users[selected]['username'])

    def profile(self, username):
        user = self.fetch(self.client.profile, username)
        while True:
            choice = xbmcgui.Dialog().select(user_name(user),
                                            [T(35127, 'About'), T(35100, 'Plex user reviews')])
            if choice < 0:
                return
            if choice == 0:
                xbmcgui.Dialog().textviewer(user_name(user), '\n\n'.join(
                    text(user.get(key)) for key in ('username', 'bio', 'location', 'url') if user.get(key)))
            else:
                self.run(self.activities, user_name(user),
                         lambda cursor: self.client.profile_reviews(user['id'], cursor))

    def activity(self):
        self.activities(T(35104, 'Friends activity'), self.client.activity)

    def discover(self):
        while True:
            query = xbmcgui.Dialog().input(T(35128, 'Search all Plex movies and shows'))
            if not query.strip():
                return
            results = self.fetch(self.client.discover, query)
            if not results:
                xbmcgui.Dialog().ok(T(35102, 'Discover movies and shows'),
                                    T(35129, 'No matching movies or shows found.'))
                continue
            selected = 0
            while True:
                selected = self.select(query, [(text(item.get('title')), '{} - {}'.format(
                    item.get('year') or '', T(32348, 'Movies') if item['type'] == 'movie'
                    else T(32393, 'TV Shows'))) for item in results], selected)
                if selected < 0:
                    break
                self.run(self.open_title, results[selected])

    def open_title(self, metadata):
        from plexnet import plexapp, exceptions
        from . import opener
        guid = metadata.get('guid') or 'plex://{}/{}'.format(metadata['type'], metadata['id'])
        ident = api.metadata_id(guid)
        if not ident:
            raise api.CommunityError('metadata')
        server = plexapp.SERVERMANAGER.getDiscoverServer()
        try:
            item = self.fetch(server.getObject, '/library/metadata/' + ident)
        except (exceptions.BadRequest, IndexError, TypeError):
            # plexnet.getObject indexes the first result even when an online
            # title has been removed or its provider returned no data.
            raise api.CommunityError('unavailable') from None
        if not item:
            raise api.CommunityError('unavailable')
        # Existing PM4K title screens supply summary, watchlist controls and
        # availability on the user's servers. Never play Discover metadata directly.
        command = opener.open(item, from_watchlist=True, directly_from_watchlist=False)
        if command and self.parent:
            self.parent.processCommand(command)
            raise _LeaveCommunity()
