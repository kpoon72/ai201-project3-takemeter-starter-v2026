# Milestone 1 — Community and reading notes

**Community:** r/nba (https://www.reddit.com/r/nba/) — public, no login needed.
The largest NBA discussion community; comment quality ranges from stat-backed
arguments to one-line insults, which is exactly the variation TakeMeter needs.

**How I got the posts:** public r/nba comments from 2026-09-20 to 2026-10-16,
pulled from the Arctic Shift Reddit archive with `scripts/collect_nba.py`
(Reddit's own JSON endpoint returned 403). Filters: 40–1200 characters, score
≥ 2, no links, no AutoModerator or deleted/removed comments. Result:
`data/nba_pool.csv`, 890 candidate posts. It's the offseason/preseason, so
threads are mostly trades, season predictions, preseason clips and history.

**What I read:** 40 random posts from the pool, saved in
`notes/m1_reading_sample.csv` (numbers below refer to that file's order).

## Candidate distinctions I saw in the text

1. **Some posts cite a specific, checkable number; most don't.** #2 (Deron
   Williams "26/8 on 61% TS"), #16 (Maravich's 1168 / 1022 / 976 attempts),
   #27 (Wilt's 50.4 points and 25.7 rebounds in 1961-62), #30 (35 vs 45 wins
   and what that means for the play-in).
2. **Some posts make a confident basketball claim and offer nothing behind it.**
   #8 ("Deuce won't make it past the trade deadline"), #13, #33, #40 ("Celtics
   weirdly will be the second best team").
3. **Some posts react to a clip or moment, not to an argument.** #10 ("insane.
   ive actually never seen someone get hit in the face like that"), #29, #35,
   #36.
4. **A large share of posts aren't about basketball at all; they're aimed at
   another user or fanbase.** #1, #11, #15, #25, #39 ("Damn you Wolves fans
   can't let it go huh"). The classic analysis / hot take / reaction split has
   no home for these, and they're common here.

**Something in between:** #17 (Knecht vs Bronny) has real specifics ("scored
30 against the tanking Jazz", "productive playoff minutes") but ends on "the
guy is just bad". Whether specifics like that count as support is the boundary
I expect to fight with.
