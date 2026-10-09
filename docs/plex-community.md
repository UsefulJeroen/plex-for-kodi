# Plex community preview

The UsefulJeroen fork adds the community features that are separate from
numeric ratings and Rotten Tomatoes critic excerpts in upstream PM4K.

## Using the preview

- Open your account menu on PM4K's home screen, then **Plex community**.
- **Discover movies and shows** searches Plex's online catalog, including
  titles absent from your server. Select a result to open PM4K's existing
  title screen, add or remove it from your watchlist, and find playable copies
  on your Plex servers.
- **Friends** opens your friends list, each friend's profile and their reviews.
- **Friends activity** shows the account's community feed of reviews, ratings
  and posts. It can include your own activity too.
- On movie, show, season and episode screens, open the title's options menu
  and select **Plex user reviews**. Review views include recent, top, popular
  and friends reviews. On a show's season list, a season's context menu opens
  its reviews; on an episode list the selected episode is the review target.
- On Discover/watchlist movie pages, the **More** (three-dot) button opens
  community reviews directly.
- Select a review to read its full text, then select **Discussion** to read
  its comments or **View profile** to visit the author. Review pages and
  discussions have explicit next/previous page controls.
- Spoiler-marked reviews hide their text in lists. Opening a review asks
  whether to show its text and discussion. That choice is remembered only
  while the current community browser remains open.

Plex's privacy controls determine what the account can see. Muted/blocked
users, hidden users, muted activities and removed comments are also filtered
locally. Private or unavailable content and service failures show a message
instead of being silently reported as an empty successful result. No cached
social data survives an account switch.

## Account and installation

The preview retains addon ID `script.plexmod`, so installing the zip replaces
the current PM4K client and uses its existing login, subtitle settings and
other preferences. Make a backup before testing; reinstall upstream PM4K to
return to the original client. This preview is based on the fork's
`develop_kodi21` HEAD, upstream 1.14.1-beta1, rather than the older 1.3.19
client previously installed on the Ugoos.

Use Kodi's **Install from zip file** with the generated package, then restart
Kodi to reload the new English strings. Full online Plex accounts are
required; managed users and local mode cannot use community features. Library
titles need modern Plex Movie/Plex Series metadata GUIDs. Enable Plex's
**Sync Watch State and Ratings** for the official community integration of
server-library titles.

The preview keeps upstream's update machinery. Turn off automatic updates
for this addon in Kodi, and PM4K's own **Check for updates** / **Check for
updates on start**, while testing; installing an upstream update replaces the
fork's features. No fork update repository is published by this change.

## Scope

Implemented: full user review text, ratings attached to reviews, review
comments, author profiles, friends, profile reviews, community activity,
Discover catalog search, and existing watchlist/server availability controls.
Existing intro/credits skipping and Kodi playback are unchanged by the new
community code.

This preview does not compose reviews or comments, send friend requests,
manage notifications, or reproduce every official Discover page. Reading
discussions includes their existing @mention text, but does not create
mentions or notifications. Use official Plex mobile/web clients for posting.

## APIs and maintenance

Plex Web 4.162.1 currently uses `https://community.plex.tv/api` (GraphQL).
The client implements `metadataReviewsV2`, `activityCommentsV2`,
`allFriendsV2`, `userByUsername`, `user.reviews`, and `activityFeed` queries.
Discover uses `https://discover.provider.plex.tv/library/search` with
`searchProviders=discover` and `searchTypes=movies,tv`.

These are internal client APIs, not the documented Plex Media Server API.
Schema or access-policy changes may require maintenance. Requests use the
current account token in headers, bounded connection/read timeouts, HTTPS
certificate verification and no redirects. Responses aren't cached and raw
request/response bodies aren't logged. API errors shown to users contain only
local error messages, not credentials or server diagnostics.

References:

- [Plex user reviews and comments](https://support.plex.tv/articles/user-reviews/)
- [Plex developer documentation](https://developer.plex.tv/)
- [Upstream PM4K](https://github.com/pannal/plex-for-kodi)

## Building and verification

```powershell
python -m pytest tests -q
python tools/package_addon.py --output F:\kodidev\packages
```

The package has one top-level `script.plexmod` directory. It excludes Git
metadata, virtual environments, tests, build scripts and bytecode.

Development checks on 2026-10-09 verified live account authentication, each
review ordering, review pagination, a populated comment discussion, friends,
profiles, profile-review queries, activity and Discover search. The test
suite covers privacy filtering, spoilers, account changes, bounded requests,
pagination/retry behavior and use of PM4K's existing title opener rather than
direct playback of online catalog metadata.

Real GUI checks in portable Kodi 21.3 on Windows (Python 3.8.15) also
verified full-profile sign-in, the community menu, 18 friends, profiles,
empty profile-review handling, friends activity, Discover search and movie
details with watchlist controls and server availability. Dune: Part Two top
reviews opened full text and a populated discussion/comment; long text could
be paged. Interstellar Discover reviews loaded, spoiler decline returned to
the list, and next/previous review pages worked. Back navigation returned to
the calling title/results/menu. No social or watchlist data was changed.

The GUI checks found and fixed missing access to reviews on Discover movie
pages. Their More button now opens only community reviews, avoiding server
management actions on catalog metadata. Theme version 99 rebuilds the skin
for existing installations. The full suite passed: 745 tests + 787 subtests.

The Ugoos was unreachable at its prior IP during development. Installation,
remote-control navigation and playback on the device remain to be validated.
Live API checks were read-only; no reviews, comments, friendships or
watchlist entries were changed.
