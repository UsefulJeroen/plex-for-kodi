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
- Movie and episode title pages now include an inline **Ratings and Reviews**
  carousel: circular avatars, author/date, five-star ratings (including halves),
  two-line excerpts and discussion counts. The row respects PM4K's existing
  watched/unwatched review visibility preference. Critic excerpts remain after
  community cards. The final community card opens all reviews.
- **Plex user reviews** opens a custom PM4K screen with **Top**, **Recent**,
  **Popular**, **Friends**, and next/previous page controls.
- Selecting a review opens a Plex HTPC-style two-column reader: title artwork
  and summary on the left, reviewer/full text on the right, replies below.
  Up/down scrolls the full review; Down at the bottom moves into replies.
  Select a reply to read its full text; Back restores the discussion and
  selected review. Select the author to open their profile. **Refresh replies**
  reloads the discussion. Review and discussion pagination retain the previous
  page and selection without refetching; a failed page leaves the current one.
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
management actions on catalog metadata. Discover movie pages also skip local
library-collection requests, which returned an unnecessary 404 from Plex.
Theme version 99 rebuilds the skin
for existing installations. The full suite passed: 746 tests + 787 subtests.

The Ugoos was unreachable at its prior IP during development. Installation,
remote-control navigation and playback on the device remain to be validated.
Live API checks were read-only; no reviews, comments, friendships or
watchlist entries were changed.

## Review presentation validation (social.2)

Compared the actual Plex HTPC Ratings and Reviews carousel and full-review
screen with this implementation in portable Kodi 21.3 on Windows. The
presentation uses PM4K fonts/backgrounds and Kodi remote navigation; it is
not an exact copy of Plex's UI. This remains a read-only community preview:
reaction counts/buttons and posting/editing reviews or replies are not
implemented. Private Plex APIs can change independently of PM4K releases.

Final real-Kodi checks: inline Dune cards; full Varun review with the same
actual reply displayed in Plex HTPC; long-review scrolling; opening the reply
in the styled reader and Back restoring scroll/focus; Top/Popular/Recent
switches and empty-state display; multiple review pages and Previous restoring
cached results. The full suite passed 751 tests and 811 subtests, including
all theme templates. Temporary profile-validation startup code was restored
and its PIN file was consumed and removed. No build was deployed to Ugoos.

## Review reactions (social.3)

The approved inline-card and two-column reader layout is retained. Review
cards now display Plex's reaction icons, total, and your selected reaction.
The full review offers a quick Like button and a styled six-emoji React
picker: Like, Dislike, Love, Laugh, Applaud, and Question. The current emoji
is marked in the picker. Selecting it again removes the reaction; another
emoji replaces it. A Remove reaction button is also available.

These are real account reactions sent through Plex's `reactToActivity` API,
with one reaction per account per activity. Counts and emoji types are taken
from Plex's response rather than incremented locally. The previous selection
and counts remain intact on failure. A potentially committed, timed-out
mutation is never retried automatically; the client reads the latest state
and disables writes if that state cannot be verified. Cancelling the picker,
opening a review, and browsing reviews never submit a reaction. Managed
profiles and local/offline mode cannot react. Existing privacy filters and
spoiler behavior remain in place.

Other community operations remain read-only; writing reviews and replies
has not been added. The old unused stock-dialog review/discussion flows
were removed. The previous social.2 limitation about reaction support is
superseded by this release.

Validation: the full suite passed 762 tests and 823 subtests, including all
skin templates, API set/change/remove behavior, failure reconciliation,
picker cancellation and the Kodi dialog lifecycle regression. Live Plex
reads matched the reference review's 34 reactions and emoji types. Real
portable Kodi 21.3 checks verified the inline icons/counts, full review
actions, picker opening, arrow navigation and Escape cancellation with the
count unchanged. No public reaction was submitted during validation;
mutation behavior was verified using automated mocked API responses.
Normal portable startup was restored and the temporary PIN file is absent.
This version is installed in local portable Kodi; it was not deployed to
Ugoos. Plex's private API can change independently of this addon.
