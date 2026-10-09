# Plex user reviews

Movie detail pages show Plex user review cards alongside existing critic
reviews. Open a card for its full text and discussion, or choose **Plex user
reviews** from a movie, show or episode's options menu. The full list supports
Top, Recent, Popular and Friends, with next/previous pages. Existing review
visibility settings still apply. Spoiler text requires confirmation.

Reviews show reaction icons, totals and your current reaction. **Like** is a
shortcut; **React** offers Like, Dislike, Love, Laugh, Applaud and Question.
Choose another emoji to replace your reaction, choose the current one again
to remove it, or use **Remove reaction**. Counts come from Plex's response.
An uncertain write is checked with a read, never automatically retried.

This uses Plex's private community API and the current Plex account token.
It requires an online, full Plex account and modern Plex Movie/Series GUIDs.
Local mode and managed profiles cannot use it. Failed requests leave critic
reviews and playback available. Blocked, muted, hidden and removed content
is filtered. Reviews and replies cannot be posted from this addon.

The full repository suite passed 754 tests. Validation covers authentication,
privacy, spoilers, paging, reaction writes
and failures, critic fallback, and late results after changing titles. All
five themes render; the cards and emoji picker match the approved layout.
Live Plex reads succeeded. No public reactions were submitted in testing.
Plex can change this private API independently of the addon.
