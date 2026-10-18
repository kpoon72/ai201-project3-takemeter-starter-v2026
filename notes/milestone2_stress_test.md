# Milestone 2 — Stress test of the label definitions

An AI tool (Claude) was given the four definitions and asked to write eight
posts that sit on the boundaries. Each was then classified using only the
written definitions.

| # | Post | Boundary | Label | Did the rules decide it cleanly? |
|---|---|---|---|---|
| 1 | "Giannis is washed. 30/12 on 60% from the field last year means nothing when he can't stay on the floor in April." | analysis / hot_take | hot_take | **No, at first.** It has a stat, but the post waves it away instead of using it as support. Rule tightened: a conceded or dismissed fact doesn't count. |
| 2 | "LMAO Lakers fans really thought Bronny was a lottery pick" | reaction / trash_talk | trash_talk | Yes. It's aimed at a fanbase. |
| 3 | "That Wemby block was disgusting, he's going to win DPOY every year for a decade." | reaction / hot_take | hot_take | **No, at first.** It starts as a reaction but makes a prediction beyond the moment. Fixed by adding a label order (analysis → hot_take → reaction → trash_talk). |
| 4 | "Brunson is the best clutch player in the league, ask anyone who watched the playoffs." | analysis / hot_take | hot_take | Yes. "Ask anyone" is a vague appeal, not a checkable fact. |
| 5 | "Knicks won 51 games last year, they're obviously winning the east." | analysis / hot_take | analysis | Yes, though it's uncomfortable: the support is weak, but it's checkable. The label measures *whether* support is offered, not how good it is. |
| 6 | "You clearly never watched him play, he averaged 8 points on that team." | analysis / trash_talk | analysis | **No, at first.** It insults a user and makes a stat-backed claim. Rule added: a post that insults *and* claims is labelled by the claim. |
| 7 | "Refs just handed them that game. Unreal." | reaction / hot_take | reaction | Yes. It responds to one specific game and makes no claim beyond it. |
| 8 | "Bro this sub hates every player who isn't on the Celtics" | trash_talk / hot_take | trash_talk | Yes. It's aimed at the subreddit, not at basketball. |

**Result:** 5 of 8 were clean on the first pass. Posts 1, 3 and 6 caused three
changes, all now in the README: (a) a fact must be used as *support*;
(b) the label-precedence order; (c) a claim beats an insult.
