# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments from **r/nba**, Reddit's main NBA discussion
community, into four kinds of post: **`analysis`** (a basketball claim backed
by a checkable fact), **`hot_take`** (a confident claim with no support),
**`reaction`** (a response to one play, clip or piece of news) and
**`trash_talk`** (aimed at another user, fanbase or the sub, not at
basketball). The point is to separate the comments worth reading for an
argument from the noise around them. It's a DistilBERT model fine-tuned on
276 r/nba comments I collected and labelled.

**Stretch feature:** a fourth label, `trash_talk`. In my first 40 posts, about
1 in 8 were people sniping at each other, and analysis / hot_take / reaction
had no home for them.

---

## Label Taxonomy

Four labels. Every post gets exactly one. When a post seems to fit two, check
them in this order and stop at the first that applies: **analysis → hot_take
→ reaction → trash_talk**.

### `analysis`

**Definition:** Makes a basketball claim and supports it with at least one
specific, checkable fact: a stat, record, date, contract figure, award, or a
named game or event.

**Example 1:**
> That is honestly the biggest problem with Maravich: he never hesitated to take a shot from anywhere on the court if he felt like it. The all-time record for attempts in a season (1168) is held by Pete Maravich, set his senior year. Second in attempts (1022) is Pete Maravich, during his junior year. Third in attempts (976) is Pete Maravich, during his sophomore year. Fourth is Bill Mikvy with 964. Pete took more than half of his team's shots in college.

**Example 2:**
> Pretty good indeed. 50.4 points and 25.7 rebounds a night in 1961-62, and he never fouled out of a single game in his whole career.

### `hot_take`

**Definition:** A confident basketball opinion, ranking or prediction that
reaches beyond a single moment and offers no checkable fact in support.

**Example 1:**
> Look for the Knicks to make a move for a more viable backup 5. I predict Deuce won't make it past the trade deadline

**Example 2:**
> Obviously Knicks are the top but after them I think the Celtics weirdly will be the second best team

### `reaction`

**Definition:** An immediate response to one specific play, clip or piece of
news (a feeling, joke or exclamation) that makes no claim beyond that moment.

**Example 1:**
> insane. ive actually never seen someone get hit in the face like that and not even move

**Example 2:**
> Hand on the throat is a bit much for 5mins in preseason basketball

### `trash_talk`

**Definition:** Aimed at another user, a fanbase or the subreddit rather than
at basketball, such as an insult, mockery or banter, with no basketball claim
of its own.

**Example 1:**
> Damn you Wolves fans can't let it go huh. Lol

**Example 2:**
> Maybe stop being obtuse and contrarian. I'm out on a walk to happy hour right now. Hard to tell people to stop making dumb comments on Reddit when you're busy making dumb comments on Reddit

### The hardest boundary

**Which two labels:** `analysis` vs `hot_take`.

**The post that sits between them:**
> Knecht scored 30 against the tanking jazz 2 years ago then never got better. He got plenty of opportunities and would forget offensive plays and miss defensive assignments. Bronny literally had productive playoff minutes last year. JJ is a good coach you think he doesn't want to play the movement shooter guy off screens? The guy is just bad

**The decision rule I used every time:** If the post offers at least one
specific, checkable fact *as support for its claim*, it's `analysis`, even if
the tone is heated, the conclusion is extreme, or the reasoning is weak. Vague
appeals ("he's been bad all year", "ask anyone who watched", "everyone knows")
are not checkable facts. A fact the post concedes or waves away ("30/12 means
nothing") is not support either. Under this rule, the Knecht post is
`analysis`: "scored 30 against the tanking Jazz" and "productive playoff
minutes last year" are checkable, and both are used to argue the conclusion.

**Second rule (reaction vs trash_talk):** Ask who the post is aimed at. A
player, play or piece of news makes it `reaction`, even when the language is
insulting ("this makes Stew look like a huge bitch"). Another user, a fanbase
or the sub makes it `trash_talk`. A post that insults a user *and* makes a
basketball claim is labelled by the claim (`analysis` or `hot_take`), which
is what the label order above enforces.

---

## The Dataset

**Where the posts came from:** public r/nba comments posted between
2026-09-01 and 2026-10-16 (offseason and preseason), pulled from the Arctic
Shift public Reddit archive with `scripts/collect_nba.py`, because Reddit's
own JSON endpoint blocked automated requests (403). Filters: 40–1200
characters, comment score ≥ 2, no links, no AutoModerator or deleted posts.
That gave a pool of 958 posts (`data/nba_pool.csv`). `analysis` and
`trash_talk` were thin in a random sample, so I added two targeted pulls: a
second pass of posts that cite a number (`--stat`), and posts addressed to
"you / fans / this sub". 40 candidates were skipped because they fit no label
(off-topic politics or other sports, personal stories, bare questions).

**How I labelled them:**
- **Cold set:** 20 posts set aside before any AI labelling. I labelled **16**
  of them by hand from the definitions alone (note `cold`). For the other 4 I
  asked the AI to choose, so they are marked pre-labelled, not cold.
- **Pre-labelled:** the other 256 rows were pre-labelled by an AI (Claude)
  given my definitions, label order and decision rules (note `pre-labelled
  by AI`). The AI then did a second consistency pass (every non-analysis post
  containing a number, and every analysis post without one), which changed
  nothing.
- **My review:** I spot-checked 20 random pre-labelled rows (5 per label) and
  agreed with the AI on **3 of 20**. Several of my picks contradicted my own
  written rules, so I recorded them in `notes/milestone4_spot_check.csv`
  instead of overwriting the training labels. The other 236 rows I did not
  review individually. Full log: `notes/milestone4_hard_cases.md`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| analysis | 93 | 33.7% |
| hot_take | 80 | 29.0% |
| reaction | 54 | 19.6% |
| trash_talk | 49 | 17.8% |
| **Total** | 276 | 100% |

**Three hard cases**

**1.**
> *The post:* "holy shit, he went 56-104 on threes in the 16-17 season"
>
> *Could have been:* `analysis` or `reaction`
>
> *I chose, because:* `reaction`. It has a checkable number, but the number
> isn't used to support any claim; it's surprise at a fact. My analysis rule
> needs a claim for the fact to support.

**2.**
> *The post:* "Gordon is bigger, more athletic, can shoot 3s, a better decision maker, and is more skilled than Sochan. He's also a way more impactful defender. ... He's just not a good player and I think he'll be out of the league soon."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. It's long and gives reasons, so it reads
> like analysis, but every reason is itself an opinion. Effort isn't the test;
> a checkable fact is.

**3.**
> *The post:* "Damn Collins just got ragebaited in preseason game 1 on a brand new team. Could easily be nothing but honestly that just does not bode well for his season/future in the league."
>
> *Could have been:* `reaction` or `hot_take`
>
> *I chose, because:* `hot_take`. It starts as a reaction to one clip, but the
> second sentence makes a claim about his whole season, and my label order
> puts `hot_take` ahead of `reaction`.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on **`mps` (Apple Silicon GPU)**, torch 2.14.1, as
recorded in `results.json`.

**Anything I changed from the defaults, and why:** nothing. The only notebook
edits were my name and the label list (four labels instead of the example
three).

**Split sizes:** train 192 · val 42 · test 42 (stratified 70/15/15).

| Label | Train | Val | Test |
|---|---|---|---|
| analysis | 65 | 14 | 14 |
| hot_take | 56 | 12 | 12 |
| reaction | 38 | 8 | 8 |
| trash_talk | 33 | 8 | 8 |

`reaction` and `trash_talk` have exactly 8 posts each in test, right at the
edge where one wrong prediction moves a label's F1 a lot. Expect those two
to be the jumpiest across seeds next unit.

---

## How I Used AI

I used Claude (in Claude Code) throughout this unit.

**Moment 1: stress-testing the labels**

- *What I asked for:* eight posts that sit on the boundaries between my four
  labels, to classify using only my definitions.
- *What came back:* eight posts. Five were clean; three weren't: a stat the
  poster waves away ("30/12 means nothing"), a reaction that ends in a
  prediction, and an insult to a user that also cites a stat.
- *What I changed:* three rule changes, all now in the taxonomy: a fact must be
  used *as support*; a label order (analysis → hot_take → reaction →
  trash_talk); and a basketball claim beats an insult. Log:
  `notes/milestone2_stress_test.md`.

**Moment 2: drafting the acceptance criteria**

- *What I asked for:* after checking with course staff that it was allowed,
  I had Claude draft the five criteria, using the metrics the notebook
  actually records.
- *What came back:* five criteria, one per area (accuracy 0.60, per-label F1
  0.45, balance 15–40%, staff agreement 22/30, confidence gap 0.20), each
  with a reason tied to my data.
- *What I changed:* I kept the numbers. The balance criterion changed my
  collection plan: `analysis` was too rare in a random sample, so I pulled
  extra stat-citing posts to reach 15%.

**Other AI use:** Claude wrote the collection script, picked the README
example posts, drafted the definitions and this README, and ran the
notebook.

**Pre-labelling disclosure:** 260 of 276 rows were labelled by AI (256
pre-labelled, plus 4 cold-set posts I asked it to choose). 16 rows are my own
cold labels. I spot-checked 20 AI rows, agreed with 3, and kept the AI
labels because my picks didn't follow my written rules. I did not review the
remaining 236 individually. Each row's `note` column says which group it is
in.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both scored on the same 42 held-out posts in `test_split.csv`. Baseline:
`facebook/bart-large-mnli` zero-shot, given my four definitions from
`label_definitions.txt`. Trained: the unit 5 run (seed 42, `mps`).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.357 | 0.500 | +0.143 |
| Macro F1 | 0.199 | 0.371 | +0.171 |
| F1 — `analysis` | 0.531 | 0.683 | +0.152 |
| F1 — `hot_take` | 0.267 | 0.400 | +0.133 |
| F1 — `reaction` | 0.000 | 0.000 | +0.000 |
| F1 — `trash_talk` | 0.000 | 0.400 | +0.400 |

**What my definitions were worth:** the same baseline with bare label names
instead of definitions (`baseline_results_bare_names.json`) scored accuracy
**0.310** and macro F1 **0.184**, versus 0.357 / 0.199 with definitions. So
the definitions bought about 5 points of accuracy. They also changed *what*
it got right: with bare names it never predicted `analysis` correctly
(F1 0.000) and leaned on `hot_take` (0.537). With definitions, `analysis`
became its best label (0.531). The baseline reported above is the run with
definitions.

The baseline took a few seconds per post; the trained model scores all 42 in
about a second.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
Written before running the baseline: the trained model will beat the
baseline on overall accuracy, mostly on `analysis`, because it learned what
"a checkable fact used as support" looks like in r/nba posts.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
The prediction was right in direction: the trained model beat the
baseline on accuracy (+0.14) and on `analysis` (+0.15). But `analysis` was
not where it gained most. The biggest gain was `trash_talk` (0.000 → 0.400):
a general model reading "aimed at another user… rather than at basketball"
never picked it, while the fine-tuned model learned r/nba's surface signs of
it ("you", "y'all", "this sub"). Neither model got a single `reaction` right,
so fine-tuning added nothing there. That points at the label, not the
training method. All of this is one split of 42 posts, so a 0.14 gap is
about 6 posts.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

All three seeds trained on `mps` (Apple Silicon GPU), torch 2.14.1, default
settings (3 epochs, lr 2e-5, batch 16). Each seed is a different stratified
split, with 42 test posts. Seed 42 reproduced the unit 5 run exactly (0.500).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.500 | 0.476 | 0.500 | MISSED |
| 2. Every label F1 (worst label shown) | ≥ 0.45 | 0.000 (`reaction`) | 0.000 (`reaction`, `trash_talk`) | 0.000 (`trash_talk`) | MISSED |
| 3. Every label 15–40% of `labels.csv` | 15%–40% | 17.8%–33.7% | 17.8%–33.7% | 17.8%–33.7% | MET |
| 4. Agreement with staff labels | ≥ 22/30 | 5/30 (measured once, not per seed) | — | — | MISSED |
| 5. Most-confident third minus least-confident third, accuracy | ≥ +0.20 | +0.286 (0.714 vs 0.429) | +0.500 (0.714 vs 0.214) | +0.429 (0.643 vs 0.214) | MET |

Criterion 3 is a property of the labelled file, not of a split, so it's the
same on every seed. Criterion 4 is a property of my labelling, measured once
on the 30 staff posts.

**Per-label F1, all three seeds** (from section 6):

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.500 | 0.476 | 0.500 | 0.024 |
| Macro F1 | 0.371 | 0.294 | 0.378 | 0.084 |
| F1 — `analysis` | 0.683 | 0.824 | 0.727 | 0.141 |
| F1 — `hot_take` | 0.400 | 0.353 | 0.452 | 0.099 |
| F1 — `reaction` | 0.000 | 0.000 | 0.333 | 0.333 |
| F1 — `trash_talk` | 0.400 | 0.000 | 0.000 | 0.400 |

Accuracy moved only 0.024 across seeds, well under the 10-point warning line,
so the overall number is stable. The per-label F1s for `reaction` and
`trash_talk` swing much more, as expected with only 8 test posts each.

### Confusion matrix

Seed 42 (section 7 prints the first seed):

| true \ predicted | analysis | hot_take | reaction | trash_talk |
|---|---|---|---|---|
| **analysis** | 14 | 0 | 0 | 0 |
| **hot_take** | 7 | 5 | 0 | 0 |
| **reaction** | 4 | 4 | 0 | 0 |
| **trash_talk** | 2 | 4 | 0 | 2 |

The other two seeds, from `results_three_seeds_before.json`:

| Seed 7: true \ predicted | analysis | hot_take | reaction | trash_talk |
|---|---|---|---|---|
| **analysis** | 14 | 0 | 0 | 0 |
| **hot_take** | 6 | 6 | 0 | 0 |
| **reaction** | 0 | 8 | 0 | 0 |
| **trash_talk** | 0 | 8 | 0 | 0 |

| Seed 2024: true \ predicted | analysis | hot_take | reaction | trash_talk |
|---|---|---|---|---|
| **analysis** | 12 | 2 | 0 | 0 |
| **hot_take** | 5 | 7 | 0 | 0 |
| **reaction** | 2 | 4 | 2 | 0 |
| **trash_talk** | 0 | 6 | 2 | 0 |

**My biggest off-diagonal number, and what it means:**
7 real `hot_take` posts were called `analysis`, and 0 went the other way.
The model treats "sounds like a basketball argument" as `analysis` whether or
not a checkable fact is there, so it hasn't learned my hardest boundary, and
it errs in one direction only. Across all three seeds there's a second
pattern: the model almost never predicts `reaction` or `trash_talk` at all
(6 such predictions in 126 test posts). It falls back on the two biggest
labels.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy on the test split | ≥ 0.60 on all 3 seeds | **MISSED** | 0.500 / 0.476 / 0.500. No seed reached 0.60; the best is 10 points short. |
| 2 | Every label F1 | ≥ 0.45 for all 4 labels, all 3 seeds | **MISSED** | Some label scored 0.000 on every seed (`reaction` on 42 and 7, `trash_talk` on 7 and 2024). Only `analysis` cleared 0.45 on all three. |
| 3 | Every label 15–40% of `labels.csv` | all four inside 15%–40% | **MET** | Smallest `trash_talk` 17.8%, largest `analysis` 33.7%. It's a property of the file, so it's the same for every seed. |
| 4 | Agreement with the staff labels | ≥ 22/30 | **MISSED** | 5/30 from `agreement.py`, 17 short. |
| 5 | Most-confident third beats least-confident third | ≥ +0.20 on all 3 seeds | **MET** | +0.286 / +0.500 / +0.429. The smallest gap (seed 42) still clears 0.20 by about one post per third (14 posts each). |

**Arguing against my two MET verdicts.** Criterion 5 could be called
hollow: the model is confident mainly on `analysis`, the one label it gets
right, so the gap may just reflect "analysis is easy" rather than useful
calibration. But the criterion as written asks only for the gap, the gap
holds on all three seeds, and so the verdict stays MET. Criterion 3 can't be
argued against: it's a count.

**Diagnoses**

**Criterion 1 (accuracy) and criterion 2 (per-label F1): undertrained,
falling back on the two biggest labels.**
- *Evidence from the matrix:* across 126 test predictions (3 seeds × 42),
  the model predicted `reaction` or `trash_talk` only 6 times, although 48
  of those posts really were one of the two. On seed 7, every real
  `reaction` and `trash_talk` post was called `hot_take` (8 and 8).
- *Evidence from training:* the training loss ended at about 1.19–1.25.
  Random guessing over four labels is 1.39 (ln 4). Validation loss was still
  falling at epoch 3 on every seed (seed 42: 1.30 → 1.24 → 1.21). The model
  stopped while still learning, before it got past "guess one of the two
  big labels".
- *Evidence it isn't the labels' fault:* `reaction` is the easiest label to
  spot from the surface. Its posts average 15 words against 50 for
  `analysis`, yet the model still mislabels them. A model that had learned
  anything about these labels would pick that up.
- *Why the small labels suffer most:* `reaction` and `trash_talk` have only
  38 and 33 training posts. With so little training, the model gets the
  most out of predicting the 65- and 56-post labels.

**Criterion 2, the `hot_take` → `analysis` direction: a genuinely hard
pair.** On seed 42, 7 real `hot_take` posts were called `analysis` and 0
went the other way (6 and 0 on seed 7, 5 and 2 on seed 2024). My rule
separates these two by *whether a fact is used as support*, but on the
surface they look alike: 51% of my `hot_take` posts contain a number
(against 87% of `analysis`). The model has learned "a number plus a
confident claim means `analysis`" and not the support rule. The agreement
report is what rules out "I labelled this boundary inconsistently" as the
main cause. My inconsistency on the staff set was the same mistake
(number = analysis), but 260 of 276 training rows were labelled by AI
applying the written rule, not by me, so the training data mostly holds
the rule, not my habit. The model is failing the same boundary I fail,
for a similar reason: the surface cue is easier than the rule.

**Criterion 4 (agreement): my own labelling, pile (a).** 19 of 25
disagreements were cases where a staff rule covered the post and I didn't
apply it. The consistent error was treating any number or date as
`analysis` and treating confident conclusions as `hot_take` even when facts
carried them. My unit 5 spot-check (3/20) showed the same pattern. This is
a labelling-consistency problem, not a model problem. What it means for the
model is limited to my 16 cold rows in `labels.csv`, which are less
reliable than the rest.

**What this points at for the improvement:** the matrix and the loss both
say the first problem is training, not labels. The model never got far
enough to show whether it can learn my boundaries. So my one change is a
training setting (more epochs), which the assignment says to choose only
when the diagnosis points at training. Here it does.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 5 / 30 = 17%

I labelled all 30 under `data/staff_taxonomy.md` and committed
`my_staff_labels.csv` (commit `500ef18`) before opening the staff labels.
Matches: posts 1, 2, 3, 5 and 13.

**Where the 25 disagreements fall:**

| Staff label | My label | Count | Posts |
|---|---|---|---|
| `analysis` | `hot_take` / `reaction` | 6 | 4, 6, 7, 8, 9, 10 |
| `hot_take` | `analysis` | 8 | 11, 12, 15, 16, 17, 18, 19, 20 |
| `hot_take` | `reaction` | 1 | 14 |
| `reaction` | `analysis` | 7 | 21, 22, 23, 25, 26, 27, 29 |
| `reaction` | `hot_take` | 3 | 24, 28, 30 |

**Piles:** (a) applied loosely: 19 · (b) rule gap: 4 (14, 19, 25, 28) ·
(c) defensible reading: 2 (24, 30).

**Disagreements**

**4.**
> *The post:* Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder.
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The post sets up a test (first half under or over 1:45), reports the result (the same slowdown after 18), and draws the inference from it. Rule 1: the test result carries the argument. I called it hot_take because no single number appears in the conclusion, but the definition doesn't require one; it requires a checkable fact doing the work.
>
> *Which pile:* (a) applied loosely

**6.**
> *The post:* Checked the entry lists. 41% of this year's field have never run the distance before, against 26% five years ago. That's why the finish-line photos look different, not because standards dropped.
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. 41% vs 26% is used to reject a rival explanation ('not because standards dropped'). Under Rule 1 that is the fact carrying the argument. I read the confident ending as a hot take, but the confidence rests on the numbers.
>
> *Which pile:* (a) applied loosely

**7.**
> *The post:* Ran the same loop in 4C and in 24C within a fortnight, same effort by heart rate. 90 seconds slower in the heat over six miles. People keep saying heat costs you 'a bit' and it's more than that.
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. A same-loop, same-effort comparison with a number attached (90 seconds over six miles), used to answer 'heat costs a bit'. Rule 1 asks whether the fact is load-bearing, not whether the sample is big.
>
> *Which pile:* (a) applied loosely

**8.**
> *The post:* Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate.
>
> *Staff said / I said:* `analysis` / `reaction`
>
> *My call, and why:* Staff is right. A range (18–23%) across a named span (since 2012), used to argue it's a base rate, not a bad-luck year. Nothing in it is about the writer's own feelings, so the reaction definition doesn't fit, and Rule 3 says recency doesn't outrank evidence.
>
> *Which pile:* (a) applied loosely

**9.**
> *The post:* The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace.
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. A date (2021), a measurement (60 m long) and the arithmetic consequence (about 12 seconds) are the whole argument. I reacted to 'Everyone comparing PBs…' as a sweeping claim, but that claim is exactly what the remeasurement supports.
>
> *Which pile:* (a) applied loosely

**10.**
> *The post:* Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people.
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right, though staff flagged it as hard. The sample is tiny (three runners) and the conclusion is hedged, but Rule 1 doesn't ask for strong evidence, only that the checkable observation (within 10 seconds over 5 miles) is what the claim rests on. It is.
>
> *Which pile:* (a) applied loosely

**11.**
> *The post:* Anyone who races more than once a month isn't training, they're just collecting medals.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. There is no fact anywhere in the post. 'Once a month' is part of the claim, not evidence for it, so the analysis definition can't apply. A confident claim about a group with zero support is the hot_take definition.
>
> *Which pile:* (a) applied loosely

**12.**
> *The post:* Heart rate zones are astrology for runners.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. A metaphor is not a 'named comparison' in the sense the definition means (a comparison with checkable content). Nothing is argued, so it's hot_take.
>
> *Which pile:* (a) applied loosely

**14.**
> *The post:* Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem.
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* Staff says hot_take, I said reaction. Staff is right that it's not analysis (Rule 1: '3%' is decoration, 'so obviously' does the work). But my reaction reading isn't covered by any rule: the post reads as a heated response to the latest times. Rule 2 separates reaction from hot_take by 'about the writer vs about the world', and this one is about the world, so on reflection it's hot_take. Still, the taxonomy has no rule for a response to news that makes a general claim. I'm calling it a gap: reaction's definition ('an immediate response to something that just happened') fits it on its face.
>
> *Which pile:* (b) rule gap

**15.**
> *The post:* Marathon training plans are all the same plan with different fonts.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. An aphorism with no support. Whether plans 'could be checked' doesn't matter: the definition needs a checkable fact stated and used, and none is.
>
> *Which pile:* (a) applied loosely

**16.**
> *The post:* If you need a gel before 90 minutes you have a fuelling problem, not an energy problem.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. '90 minutes' is a threshold inside the claim, not evidence for it. It's a confident prescription with nothing behind it, which is hot_take.
>
> *Which pile:* (a) applied loosely

**17.**
> *The post:* Road racing peaked in about 2015 and everything since has been marketing.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. '2015' sets the claim's scope; it isn't evidence that racing peaked. Rule 1: a fact has to do work in the argument. I counted any date as a fact, which is the same mistake as on 16 and 18.
>
> *Which pile:* (a) applied loosely

**18.**
> *The post:* Track sessions are wasted on anyone running slower than 8 minute miles. You'd get more out of just running more.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. '8 minute miles' is a cutoff, not support, and 'you'd get more out of just running more' is a second unsupported claim.
>
> *Which pile:* (a) applied loosely

**19.**
> *The post:* Nobody actually enjoys the long run. They enjoy having done it, which is a completely different thing, and the sport would be more honest if it said so.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff says hot_take, I said analysis. Staff is right that no checkable fact appears. But the post does argue: it draws a distinction (enjoying vs having enjoyed) and reasons to a conclusion. The taxonomy only knows 'argued from a fact' (analysis) or 'not argued' (hot_take). It has no place for a post that reasons without facts. That's a gap: by the definitions I'd now say hot_take, because analysis needs a fact, but hot_take's 'it isn't argued' isn't true of this post either.
>
> *Which pile:* (b) rule gap

**20.**
> *The post:* Every injury thread on this forum is the same injury and the same three replies.
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. 'The same three replies' sounds countable, but no count is given and nothing is shown. Asserting something that could be checked isn't the same as offering a checkable fact.
>
> *Which pile:* (a) applied loosely

**21.**
> *The post:* Four minutes off. FOUR. I've been chasing that time for two years and I'm sat on the kerb outside the finish just grinning at nothing.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. 'Four minutes off' is the news, not an argument. Nothing is argued from it, and the post is about the writer, minutes after their race. Rule 3 only makes a recent post analysis if a fact is load-bearing, and here none is.
>
> *Which pile:* (a) applied loosely

**22.**
> *The post:* Got up at 5, drove ninety minutes, and it's cancelled. Standing in the car park in the rain reading the email.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. '5am' and 'ninety minutes' are details of what happened to the writer, with no claim attached. That's reaction. I counted any number as a fact, again.
>
> *Which pile:* (a) applied loosely

**23.**
> *The post:* First run back after eight weeks out. Two miles, slower than my warm-up used to be, and I don't care even slightly.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. 'Eight weeks' and 'two miles' describe the run; the point of the post is 'I don't care even slightly', a feeling about something that just happened.
>
> *Which pile:* (a) applied loosely

**24.**
> *The post:* Watching the last 400 of that and I had to stand up. Still standing up actually.
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff says reaction, I said hot_take. I'm defending my reading. The staff reaction definition says it's 'usually about the writer's own experience', but this post is about watching someone else's race, and standing up is a way of saying 'that was an incredible finish', which is Rule 2's own hot_take example ('That was the best race of the decade'). It's weak, because the claim is only implied, but the definition's 'usually' leaves room for it.
>
> *Which pile:* (c) defensible reading

**25.**
> *The post:* Blew up at 20 with the pace band still in my hand like it was going to help. Rough one.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff says reaction, I said analysis. Staff is right that nothing is argued from 'at 20'. But the rules never say what to do with a number that's just part of the story: Rule 1 covers decorative numbers on a conclusion, and this post has no conclusion at all. A one-line rule like 'a number with no claim attached is never analysis' would have stopped me here. Gap.
>
> *Which pile:* (b) rule gap

**26.**
> *The post:* Someone handed my kid an orange slice at mile 22 and I have been crying on and off since.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. 'Mile 22' is where it happened; the post is pure feeling. Same mistake as 21–23.
>
> *Which pile:* (a) applied loosely

**27.**
> *The post:* Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. 'About 20 degrees' describes the experience, not evidence for any claim. It's a report of the run just done.
>
> *Which pile:* (a) applied loosely

**28.**
> *The post:* Third DNF this year. I don't really want to talk about it, just wanted to put it somewhere.
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff says reaction (flagged hard), I said hot_take. Staff is right that it isn't a general claim. But the reaction definition centres on 'something that just happened… in the last few hours', and 'third DNF this year' is about a whole year. Staff's note says Rule 3 doesn't rescue it into analysis, which I agree with, but no rule says a post about the writer's own state over months is still reaction. Gap.
>
> *Which pile:* (b) rule gap

**29.**
> *The post:* Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size.
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. It's the writer's own realisation, now. Nothing is argued, so the possible wry point about shoe discourse is implied, not made.
>
> *Which pile:* (a) applied loosely

**30.**
> *The post:* Signed up. Card's charged, no going back, immediately regret everything.
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff says reaction, I said hot_take. I'm defending my reading. 'Immediately regret everything' is a confident, sweeping statement and the post offers nothing to support it. Rule 2 asks whether it's about a claim or about the writer, and the honest answer is that it's both. It's a joke. Again it's weak: the post is mostly about the writer's own moment, and Rule 4 (most words) would push it to reaction.
>
> *Which pile:* (c) defensible reading

**What the pattern in my disagreements tells me:**

19 of 25 are pile (a): the rule covered the post and I didn't apply it. The
pattern is one specific mistake made over and over. **I treated "contains a
number or a date" as the test for `analysis`**, so personal posts with
numbers in them (mile 22, 5am, four minutes) became `analysis`. Meanwhile I
called real fact-driven arguments (posts 4, 6, 7, 9, 10) `hot_take`, because
they *ended* on a confident conclusion. That's the reverse of the rule: the
question is whether the fact carries the argument, not whether a number
appears or whether the tone is confident. Only 2 of my 30 labels were
`reaction`, against 10 in the staff set, so I barely used the label for "what
just happened to me".

This is direct evidence about my own labelling. It matches my unit 5
spot-check (3/20 agreement with the rule-based labels, with the same kind of
error: a no-fact post called `analysis`, a stat-backed argument called
`reaction`). One caveat matters for the diagnosis below: 260 of my 276
training rows were pre-labelled by AI applying my written rules, and only
16 are my cold labels. So this report measures how *I* label. It tells me my
16 cold rows are unreliable, not that the whole training file is.

---

## The Improvement

**What I changed:** one training setting. `EPOCHS` went from 3 to 10 in
section 2 of the notebook. Everything else is identical: same `labels.csv`,
same taxonomy, same criteria, same learning rate (2e-5), batch size (16),
max length (128), same three seeds (42, 7, 2024, so the same three splits),
same device (`mps`). Results are in `results_three_seeds_after.json`
(`RUN_LABEL = "after"`), and `results_three_seeds_before.json` is untouched.

**Which diagnosis pointed at it:** the criteria 1 and 2 diagnosis. Training
loss ended near random (1.19–1.25 against ln 4 = 1.39), validation loss was
still falling at epoch 3 on every seed, and the model predicted the two small
labels only 6 times in 126 test posts. That's a model that stopped
before it learned, so the fix is to let it train longer. I did not relabel:
the agreement report showed my inconsistency is in my own 16 cold rows, while
the 260 AI-labelled rows follow the written rules.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.548 | 0.500 | 0.524 | MISSED |
| 2. Every label F1 (worst label shown) | ≥ 0.45 | 0.182 (`reaction`) | 0.154 (`reaction`) | 0.222 (`reaction`) | MISSED |
| 3. Every label 15–40% of `labels.csv` | 15%–40% | 17.8%–33.7% | 17.8%–33.7% | 17.8%–33.7% | MET |
| 4. Agreement with staff labels | ≥ 22/30 | 5/30 (unchanged, no relabelling) | — | — | MISSED |
| 5. Most-confident third minus least-confident third, accuracy | ≥ +0.20 | +0.357 (0.714 vs 0.357) | +0.571 (0.857 vs 0.286) | +0.357 (0.714 vs 0.357) | MET |

**Before vs after, side by side:**

| Measure | Before: 42 / 7 / 2024 | After: 42 / 7 / 2024 | Change in the 3-seed mean |
|---|---|---|---|
| Overall accuracy | 0.500 / 0.476 / 0.500 | 0.548 / 0.500 / 0.524 | 0.492 → 0.524 (+0.032) |
| Macro F1 | 0.371 / 0.294 / 0.378 | 0.477 / 0.451 / 0.453 | 0.348 → 0.460 (+0.113) |
| F1 — `analysis` | 0.683 / 0.824 / 0.727 | 0.800 / 0.720 / 0.690 | 0.745 → 0.737 (−0.008) |
| F1 — `hot_take` | 0.400 / 0.353 / 0.452 | 0.480 / 0.500 / 0.500 | 0.402 → 0.493 (+0.092) |
| F1 — `reaction` | 0.000 / 0.000 / 0.333 | 0.182 / 0.154 / 0.222 | 0.111 → 0.186 (+0.075) |
| F1 — `trash_talk` | 0.400 / 0.000 / 0.000 | 0.444 / 0.429 / 0.400 | 0.133 → 0.424 (+0.291) |
| `reaction`/`trash_talk` predictions (of 42) | 2 / 0 / 4 | 13 / 11 / 3 | 6 → 27 in total |

**Confusion matrix after, seed 42:**

| true \ predicted | analysis | hot_take | reaction | trash_talk |
|---|---|---|---|---|
| **analysis** | 12 | 2 | 0 | 0 |
| **hot_take** | 2 | 6 | 1 | 3 |
| **reaction** | 2 | 2 | 1 | 3 |
| **trash_talk** | 0 | 3 | 1 | 4 |

**Did it help, and how do I know:** Yes, partly, but no verdict changed.
The clearest gain is macro F1, up on every seed (mean 0.35 → 0.46). The model
now actually uses the small labels: `reaction`/`trash_talk` predictions went
from 6 to 27 across the three seeds, and `trash_talk` F1 went from
0.40 / 0.00 / 0.00 to 0.44 / 0.43 / 0.40, about 0.42 on every seed. The
one-way `hot_take` → `analysis` error on seed 42 went from 7 to 2, so the
analysis/hot_take boundary improved too. Overall accuracy rose only 3
points, which is about one post per seed: less than I'd call a real
change on 42 posts. Every miss is still a miss. Accuracy is 5–10 points
short, and `reaction` is still the worst label on every seed (≤ 0.22).

What the change revealed: once the model stopped falling back on the two
big labels, `reaction`'s errors spread out, mostly into `trash_talk` (3 of 8
on seed 42) and `hot_take`. Both are short, informal posts. So `reaction`'s
problem is no longer undertraining. It's a short-post boundary the model
can't draw from 38 training examples.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
